# Generated by Django 4.2.7 on 2023-12-04 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_profile_pic1_alter_profile_pic2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic1',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic2',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic3',
            field=models.ImageField(upload_to=''),
        ),
    ]
