from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from schoolfees.models import Payment, School, Student


class Command(BaseCommand):
    help = 'Seed wholly fictional Ghanaian schools, students, and test payments.'

    def handle(self, *args, **options):
        User = get_user_model()
        accounts = [
            ('accra_admin', 'AccraDemo2026!'),
            ('kumasi_admin', 'KumasiDemo2026!'),
            ('viewer', 'ViewerDemo2026!'),
        ]
        users = {}
        for username, password in accounts:
            user, _ = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.save(update_fields=['password'])
            users[username] = user

        school_data = [
            ('Harbour View Academy (Demo)', 'Greater Accra', 'Tema', users['accra_admin']),
            ('Asante Learning Centre (Demo)', 'Ashanti', 'Kumasi', users['kumasi_admin']),
        ]
        schools = []
        for name, region, town, admin_user in school_data:
            school, _ = School.objects.update_or_create(name=name, defaults={'region': region, 'town': town, 'administrator': admin_user})
            schools.append(school)

        student_data = [
            ('HV-2026-001', schools[0], 'Akosua Mensah', 'JHS 2', '950.00'),
            ('HV-2026-002', schools[0], 'Kwame Tetteh', 'JHS 3', '1200.00'),
            ('AL-2026-001', schools[1], 'Abena Owusu', 'JHS 1', '800.00'),
            ('AL-2026-002', schools[1], 'Kofi Asare', 'JHS 2', '900.00'),
        ]
        students = {}
        for code, school, name, class_name, due in student_data:
            student, _ = Student.objects.update_or_create(admission_number=code, defaults={'school': school, 'full_name': name, 'class_name': class_name, 'fee_due_ghs': Decimal(due)})
            students[code] = student

        payment_data = [
            ('GH-MOMO-260001', 'HV-2026-001', '250.00', Payment.Channel.MTN, Payment.Status.PENDING),
            ('GH-MOMO-260002', 'HV-2026-001', '100.00', Payment.Channel.TELECEL, Payment.Status.SUCCESS),
            ('GH-MOMO-260003', 'HV-2026-002', '300.00', Payment.Channel.AT, Payment.Status.FAILED),
            ('GH-BANK-260004', 'AL-2026-001', '400.00', Payment.Channel.BANK, Payment.Status.PENDING),
            ('GH-MOMO-260005', 'AL-2026-002', '200.00', Payment.Channel.MTN, Payment.Status.SUCCESS),
        ]
        for ref, student_code, amount, channel, status in payment_data:
            Payment.objects.update_or_create(reference=ref, defaults={'student': students[student_code], 'amount_ghs': Decimal(amount), 'channel': channel, 'status': status})

        self.stdout.write(self.style.SUCCESS('Seeded fictional Ghanaian demonstration data.'))
        self.stdout.write('Accounts: accra_admin / AccraDemo2026!; kumasi_admin / KumasiDemo2026!; viewer / ViewerDemo2026!')
