# Generated by Django 3.1.11 on 2021-07-14 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0018_activity_tags'),
        ('events', '0007_consumereventfeedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='school_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.schoolactivitygroup'),
        ),
    ]
