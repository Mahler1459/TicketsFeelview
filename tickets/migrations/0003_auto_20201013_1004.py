# Generated by Django 3.1.2 on 2020-10-13 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_ticket_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='Activo',
        ),
        migrations.AddField(
            model_name='ticket',
            name='Status',
            field=models.CharField(default='SIN_STATUS', max_length=20),
        ),
    ]
