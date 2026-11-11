from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from schoolfees.models import School, Student, Payment
from decimal import Decimal


class ExistingApiTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.accra = User.objects.create_user(username='accra', password='sample-pass')
        self.kumasi = User.objects.create_user(username='kumasi', password='sample-pass')
        self.school_a = School.objects.create(name='Accra School', town='Accra', region='Greater Accra', administrator=self.accra)
        self.school_b = School.objects.create(name='Kumasi School', town='Kumasi', region='Ashanti', administrator=self.kumasi)
        self.student_a = Student.objects.create(school=self.school_a, full_name='Student A', admission_number='A001', class_name='JHS 1', fee_due_ghs=Decimal('1000.00'))
        self.student_b = Student.objects.create(school=self.school_b, full_name='Student B', admission_number='B001', class_name='JHS 1', fee_due_ghs=Decimal('1000.00'))
        self.payment_a = Payment.objects.create(student=self.student_a, reference='ACC-001', amount_ghs=Decimal('100.00'), channel=Payment.Channel.MTN)
        self.payment_b = Payment.objects.create(student=self.student_b, reference='KSI-001', amount_ghs=Decimal('200.00'), channel=Payment.Channel.MTN)
        self.client = APIClient()

    def test_unauthenticated_user_cannot_list_students(self):
        response = self.client.get('/api/students/')
        self.assertIn(response.status_code, [401, 403])

    def test_school_admin_sees_only_own_students(self):
        self.client.force_authenticate(user=self.accra)
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        ids = [item['id'] for item in response.data]
        self.assertEqual(ids, [self.student_a.id])

    def test_school_admin_sees_only_own_payments(self):
        self.client.force_authenticate(user=self.kumasi)
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, 200)
        ids = [item['id'] for item in response.data]
        self.assertEqual(ids, [self.payment_b.id])
