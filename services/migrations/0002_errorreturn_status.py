# Generated by Django 4.2.7 on 2024-01-07 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='errorreturn',
            name='status',
            field=models.CharField(choices=[('nc', 'uncheck'), ('s', 'servicing'), ('c', 'checked'), ('y', 'approved'), ('n', 'deny'), ('d', 'done')], default='uncheck', max_length=30),
        ),
    ]
