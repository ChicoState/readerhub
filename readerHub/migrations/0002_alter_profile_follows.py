# Generated by Django 4.1.1 on 2022-09-15 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readerHub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(null=True, to='readerHub.profile'),
        ),
    ]