# Generated by Django 4.0.5 on 2022-09-18 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('image', models.ImageField(upload_to='mainproj/images')),
            ],
        ),
    ]
