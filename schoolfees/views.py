from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import School, Student, Payment
from .serializers import SchoolSerializer, StudentSerializer, PaymentSerializer


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

    # EXERCISE: Implement POST /api/payments/<id>/reconcile/
    # See ASSIGNMENT.md for the required behaviour and permission rules.
