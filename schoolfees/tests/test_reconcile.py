from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from schoolfees.models import Payment, School, Student


class PaymentReconcileTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.accra = User.objects.create_user(username='accra', password='sample-pass')
        self.kumasi = User.objects.create_user(username='kumasi', password='sample-pass')
        self.viewer = User.objects.create_user(username='viewer', password='sample-pass')

        self.school_a = School.objects.create(
            name='Accra School',
            town='Accra',
            region='Greater Accra',
            administrator=self.accra,
        )
        self.school_b = School.objects.create(
            name='Kumasi School',
            town='Kumasi',
            region='Ashanti',
            administrator=self.kumasi,
        )

        self.student_a = Student.objects.create(
            school=self.school_a,
            full_name='Student A',
            admission_number='A001',
            class_name='JHS 1',
            fee_due_ghs=Decimal('1000.00'),
        )
        self.student_b = Student.objects.create(
            school=self.school_b,
            full_name='Student B',
            admission_number='B001',
            class_name='JHS 1',
            fee_due_ghs=Decimal('1000.00'),
        )

        self.pending_a = Payment.objects.create(
            student=self.student_a,
            reference='ACC-PENDING-001',
            amount_ghs=Decimal('250.00'),
            channel=Payment.Channel.MTN,
            status=Payment.Status.PENDING,
        )
        self.failed_a = Payment.objects.create(
            student=self.student_a,
            reference='ACC-FAILED-002',
            amount_ghs=Decimal('300.00'),
            channel=Payment.Channel.AT,
            status=Payment.Status.FAILED,
        )
        self.pending_b = Payment.objects.create(
            student=self.student_b,
            reference='KSI-PENDING-001',
            amount_ghs=Decimal('200.00'),
            channel=Payment.Channel.BANK,
            status=Payment.Status.PENDING,
        )
        self.client = APIClient()

    def test_unauthenticated_cannot_reconcile(self):
        response = self.client.post(
            f'/api/payments/{self.pending_a.id}/reconcile/',
            {'verified_reference': 'ACC-PENDING-001'},
            format='json',
        )
        self.assertIn(response.status_code, [401, 403])

    def test_other_school_admin_cannot_reconcile(self):
        self.client.force_authenticate(user=self.kumasi)
        response = self.client.post(
            f'/api/payments/{self.pending_a.id}/reconcile/',
            {'verified_reference': 'ACC-PENDING-001'},
            format='json',
        )
        self.assertEqual(response.status_code, 404)
        self.pending_a.refresh_from_db()
        self.assertEqual(self.pending_a.status, Payment.Status.PENDING)

    def test_viewer_without_school_cannot_reconcile(self):
        self.client.force_authenticate(user=self.viewer)
        response = self.client.post(
            f'/api/payments/{self.pending_a.id}/reconcile/',
            {'verified_reference': 'ACC-PENDING-001'},
            format='json',
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_verified_reference_payloads_rejected(self):
        self.client.force_authenticate(user=self.accra)
        invalid_payloads = [
            {},
            {'verified_reference': None},
            {'verified_reference': 12345},
            {'verified_reference': True},
            {'verified_reference': ''},
            {'verified_reference': '   '},
            {'verified_reference': ' ACC-PENDING-001 '},
            {'verified_reference': 'WRONG-REF'},
        ]
        for payload in invalid_payloads:
            response = self.client.post(
                f'/api/payments/{self.pending_a.id}/reconcile/',
                payload,
                format='json',
            )
            self.assertEqual(response.status_code, 400, msg=f'Failed for payload: {payload}')

        self.pending_a.refresh_from_db()
        self.assertEqual(self.pending_a.status, Payment.Status.PENDING)
        self.assertIsNone(self.pending_a.reconciled_at)

    def test_missing_or_non_numeric_payment_id_returns_404(self):
        self.client.force_authenticate(user=self.accra)
        for bad_id in ['99999', 'not-an-id']:
            response = self.client.post(
                f'/api/payments/{bad_id}/reconcile/',
                {'verified_reference': 'ACC-PENDING-001'},
                format='json',
            )
            self.assertEqual(response.status_code, 404)

    def test_pending_payment_reconciles_and_repeat_does_not_overwrite_timestamp(self):
        self.client.force_authenticate(user=self.accra)
        first = self.client.post(
            f'/api/payments/{self.pending_a.id}/reconcile/',
            {'verified_reference': 'ACC-PENDING-001'},
            format='json',
        )
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.data['status'], Payment.Status.SUCCESS)
        self.assertIsNotNone(first.data['reconciled_at'])

        self.pending_a.refresh_from_db()
        original_timestamp = self.pending_a.reconciled_at
        self.assertEqual(self.pending_a.status, Payment.Status.SUCCESS)
        self.assertIsNotNone(original_timestamp)

        second = self.client.post(
            f'/api/payments/{self.pending_a.id}/reconcile/',
            {'verified_reference': 'ACC-PENDING-001'},
            format='json',
        )
        self.assertEqual(second.status_code, 409)
        self.pending_a.refresh_from_db()
        self.assertEqual(self.pending_a.reconciled_at, original_timestamp)

    def test_failed_payment_cannot_be_reconciled(self):
        self.client.force_authenticate(user=self.accra)
        response = self.client.post(
            f'/api/payments/{self.failed_a.id}/reconcile/',
            {'verified_reference': 'ACC-FAILED-002'},
            format='json',
        )
        self.assertEqual(response.status_code, 409)
        self.failed_a.refresh_from_db()
        self.assertEqual(self.failed_a.status, Payment.Status.FAILED)
        self.assertIsNone(self.failed_a.reconciled_at)