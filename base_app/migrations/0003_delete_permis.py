# Generated by Django 5.1 on 2024-09-14 03:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0002_rename_permissions_permis'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Permis',
        ),
    ]
