# Generated by Django 4.1.6 on 2023-03-01 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0008_delete_productdetail"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="discount",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="product",
            name="images",
            field=models.TextField(default="[]"),
        ),
        migrations.AddField(
            model_name="product",
            name="price",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="slug",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="product",
            name="specifications",
            field=models.TextField(default=""),
        ),
        migrations.DeleteModel(
            name="ProductVariant",
        ),
    ]
