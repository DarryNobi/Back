# Generated by Django 2.0.4 on 2018-04-27 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0003_auto_20180427_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buser',
            name='contact_usr',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='buser',
            name='department_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='buser',
            name='enterprise_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='buser',
            name='last_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='buser',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
