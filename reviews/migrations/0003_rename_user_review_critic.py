# Generated by Django 4.0.5 on 2022-06-28 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_review_recommendation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='critic',
        ),
    ]
