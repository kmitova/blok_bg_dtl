# Generated by Django 4.1.3 on 2022-11-29 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_post_publication_date_postcomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['publication_date']},
        ),
        migrations.RenameField(
            model_name='postcomment',
            old_name='publication_date_and_time',
            new_name='publication_date',
        ),
    ]
