# Generated by Django 4.1.3 on 2023-02-28 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='comment_author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='comment_content',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='profile_picture',
            new_name='comment_picture',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='comment_user',
        ),
    ]
