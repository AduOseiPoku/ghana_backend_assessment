from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('region', models.CharField(max_length=80)),
                ('town', models.CharField(max_length=80)),
                ('administrator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='managed_schools', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_number', models.CharField(max_length=32, unique=True)),
                ('full_name', models.CharField(max_length=120)),
                ('class_name', models.CharField(max_length=30)),
                ('fee_due_ghs', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='schoolfees.school')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=64, unique=True)),
                ('amount_ghs', models.DecimalField(decimal_places=2, max_digits=10)),
                ('channel', models.CharField(choices=[('MTN_MOMO', 'MTN MoMo'), ('TELECEL_CASH', 'Telecel Cash'), ('AT_MONEY', 'AT Money'), ('BANK', 'Bank')], max_length=20)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], default='PENDING', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reconciled_at', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='schoolfees.student')),
            ],
        ),
    ]
