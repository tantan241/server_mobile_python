# Generated by Django 4.1.6 on 2023-03-29 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0015_alter_product_specifications"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="type_accessory",
            field=models.IntegerField(default=0),
        ),
    ]
