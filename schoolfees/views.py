from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import School, Student, Payment
from .serializers import (
    SchoolSerializer,
    StudentSerializer,
    PaymentSerializer,
    PaymentReconcileSerializer,
)

class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]


class SchoolViewSet(ReadOnlyViewSet):
    serializer_class = SchoolSerializer

    def get_queryset(self):
        return School.objects.filter(administrator=self.request.user).order_by('id')


class StudentViewSet(ReadOnlyViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(school__administrator=self.request.user).select_related('school').order_by('id')


class PaymentViewSet(ReadOnlyViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(student__school__administrator=self.request.user).select_related('student').order_by('-created_at')

        

    @action(detail=True, methods=['post'], url_path='reconcile')
    def reconcile(self, request, pk=None):
        with transaction.atomic():
            payment = get_object_or_404(
                self.get_queryset().select_for_update(),
                pk=pk,
            )

            serializer = PaymentReconcileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if payment.status == Payment.Status.SUCCESS:
                return Response(
                    {'detail': 'Payment has already been reconciled.'},
                    status=status.HTTP_409_CONFLICT,
                )

            if payment.status == Payment.Status.FAILED:
                return Response(
                    {'detail': 'Failed payments cannot be reconciled.'},
                    status=status.HTTP_409_CONFLICT,
                )

            if payment.status != Payment.Status.PENDING:
                return Response(
                    {'detail': 'Only pending payments can be reconciled.'},
                    status=status.HTTP_409_CONFLICT,
                )

            verified_reference = serializer.validated_data['verified_reference']
            if verified_reference != payment.reference:
                return Response(
                    {'verified_reference': ['Reference does not match this payment.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payment.status = Payment.Status.SUCCESS
            payment.reconciled_at = timezone.now()
            payment.save(update_fields=['status', 'reconciled_at'])

        return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)

