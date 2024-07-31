# Generated by Django 5.0.7 on 2024-07-26 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0006_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='contact_details',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='organisation_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='quantities',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]