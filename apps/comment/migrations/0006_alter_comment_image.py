# Generated by Django 4.1.6 on 2023-03-06 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0005_alter_comment_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="image",
            field=models.FileField(max_length=254, upload_to="uploads/comments"),
        ),
    ]