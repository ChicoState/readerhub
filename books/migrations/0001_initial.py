# Generated by Django 4.1.1 on 2022-12-07 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app1.activity')),
                ('book_id', models.CharField(max_length=100)),
                ('text_review', models.CharField(max_length=65536)),
                ('star_review', models.IntegerField()),
                ('book_title', models.CharField(max_length=100)),
                ('book_cover', models.CharField(max_length=100)),
            ],
            bases=('app1.activity',),
        ),
    ]
