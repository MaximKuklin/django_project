# Generated by Django 3.0.7 on 2020-06-16 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_sicklist_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sicklist',
            old_name='author',
            new_name='doctor',
        ),
    ]
