# Generated by Django 4.1.1 on 2022-09-30 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_created_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-last_modified']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='created_on',
        ),
    ]
