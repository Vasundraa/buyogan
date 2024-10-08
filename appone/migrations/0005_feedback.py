# Generated by Django 5.0.7 on 2024-07-26 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0004_alter_wasterequest_request_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(max_length=200, verbose_name='Subject')),
                ('message', models.TextField(verbose_name='Message')),
                ('submitted_at', models.DateTimeField(auto_now_add=True, verbose_name='Submitted At')),
            ],
        ),
    ]
