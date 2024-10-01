# Generated by Django 5.0.1 on 2024-02-27 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_status_alter_product_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(default=None, null=True, upload_to='products_thumbnail/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'New'), (2, 'Old'), (3, 'Refurbished')], default=1),
        ),
    ]