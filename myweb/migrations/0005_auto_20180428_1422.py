# Generated by Django 2.0.4 on 2018-04-28 06:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0004_auto_20180427_2007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bmap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_name', models.CharField(blank=True, max_length=20)),
                ('create_time', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('satelite', models.CharField(blank=True, max_length=20)),
                ('download_times', models.IntegerField(default=0)),
                ('desc', models.TextField(default='Describe This Image', max_length=500)),
                ('thumbnail_ftp', models.CharField(blank=True, max_length=50)),
                ('wholemap_ftp', models.CharField(blank=True, max_length=50)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='module',
            name='image',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
