from rest_framework import serializers
from .models import School, Student, Payment


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'region', 'town']


class StudentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'school', 'school_name', 'admission_number', 'full_name', 'class_name', 'fee_due_ghs']
        read_only_fields = fields


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'student', 'reference', 'amount_ghs', 'channel', 'status', 'created_at', 'reconciled_at']
        read_only_fields = fields
