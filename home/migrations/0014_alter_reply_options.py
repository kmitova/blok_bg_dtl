# Generated by Django 4.1.3 on 2022-12-09 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_announcement_user_alter_comment_post_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ['publication_date'], 'verbose_name': 'Replies'},
        ),
    ]