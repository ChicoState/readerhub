# Generated by Django 4.1.1 on 2022-12-07 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personalization', '0001_initial'),
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app1.activity')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('book_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personalization.favoritebooks')),
            ],
            options={
                'ordering': ['-last_modified'],
            },
            bases=('app1.activity',),
        ),
    ]
