# Generated by Django 5.0.3 on 2024-03-27 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_department_institute_department_institutionid_policy_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institute',
            name='departmentId',
        ),
    ]
