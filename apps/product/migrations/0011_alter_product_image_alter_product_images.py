# Generated by Django 4.1.6 on 2023-03-08 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0010_alter_product_image_alter_product_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(max_length=255, upload_to="products"),
        ),
        migrations.AlterField(
            model_name="product",
            name="images",
            field=models.ImageField(max_length=255, upload_to="products"),
        ),
    ]
