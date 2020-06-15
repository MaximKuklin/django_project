# Generated by Django 3.0.7 on 2020-06-15 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_auto_20200615_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation timestamp'),
        ),
        migrations.AlterField(
            model_name='record',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='update timestamp'),
        ),
        migrations.AlterField(
            model_name='sicklist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation timestamp'),
        ),
    ]
