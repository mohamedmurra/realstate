# Generated by Django 4.0.2 on 2022-03-08 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='catagory',
        ),
        migrations.DeleteModel(
            name='blog_catagory',
        ),
    ]