# Generated by Django 4.2.7 on 2023-11-24 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={},
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Name'),
        ),
    ]
