# Generated by Django 4.2.8 on 2024-04-26 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_diapositiva_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='diapositiva',
            name='subtitulo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
