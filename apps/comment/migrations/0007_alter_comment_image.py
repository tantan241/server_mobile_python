# Generated by Django 4.1.6 on 2023-03-07 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0006_alter_comment_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="image",
            field=models.ImageField(max_length=254, upload_to="uploads/comments"),
        ),
    ]
