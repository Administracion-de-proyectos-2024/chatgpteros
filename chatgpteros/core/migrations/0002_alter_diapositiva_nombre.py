# Generated by Django 4.2.8 on 2024-04-26 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diapositiva',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]