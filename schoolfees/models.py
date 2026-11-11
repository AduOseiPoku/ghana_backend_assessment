from decimal import Decimal
from django.conf import settings
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=160)
    region = models.CharField(max_length=80)
    town = models.CharField(max_length=80)
    administrator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='managed_schools')

    def __str__(self):
        return self.name


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    admission_number = models.CharField(max_length=32, unique=True)
    full_name = models.CharField(max_length=120)
    class_name = models.CharField(max_length=30)
    fee_due_ghs = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f'{self.full_name} ({self.admission_number})'


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'

    class Channel(models.TextChoices):
        MTN = 'MTN_MOMO', 'MTN MoMo'
        TELECEL = 'TELECEL_CASH', 'Telecel Cash'
        AT = 'AT_MONEY', 'AT Money'
        BANK = 'BANK', 'Bank'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    reference = models.CharField(max_length=64, unique=True)
    amount_ghs = models.DecimalField(max_digits=10, decimal_places=2)
    channel = models.CharField(max_length=20, choices=Channel.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    reconciled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.reference
