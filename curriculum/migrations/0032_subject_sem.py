# Generated by Django 3.2 on 2023-02-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0031_alter_lesson_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='sem',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
