# Generated by Django 4.0.4 on 2024-01-09 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_filemanager_file_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemanager',
            name='file_upload',
            field=models.FileField(upload_to='media/'),
        ),
    ]