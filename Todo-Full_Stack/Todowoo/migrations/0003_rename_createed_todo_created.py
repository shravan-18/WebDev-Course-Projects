# Generated by Django 4.2.7 on 2023-11-21 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Todowoo', '0002_alter_todo_date_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='createed',
            new_name='created',
        ),
    ]
