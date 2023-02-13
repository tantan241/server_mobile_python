# Generated by Django 4.1.6 on 2023-02-12 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=155)),
                ('slug', models.CharField(default='', max_length=255)),
                ('price', models.FloatField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
                ('image', models.CharField(default='', max_length=255)),
                ('status', models.IntegerField(default=1)),
                ('brand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.brand')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('system', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('frontCamera', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('rearCamera', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('chip', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('ram', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('rom', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('sim', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('battery', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('image', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('typeProduct', models.IntegerField(default=1)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
