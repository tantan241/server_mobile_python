# Generated by Django 4.1.6 on 2023-03-06 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0002_alter_comment_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="image",
            field=models.FileField(max_length=254, upload_to=None),
        ),
    ]
