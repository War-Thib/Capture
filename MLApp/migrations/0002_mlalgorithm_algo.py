# Generated by Django 4.0.2 on 2022-02-15 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MLApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlalgorithm',
            name='algo',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
