# Generated by Django 3.2.7 on 2021-09-14 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdto',
            name='currency',
            field=models.CharField(default='USD', max_length=5),
            preserve_default=False,
        ),
    ]