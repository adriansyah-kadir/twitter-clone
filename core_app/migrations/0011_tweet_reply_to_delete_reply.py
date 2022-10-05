# Generated by Django 4.1.1 on 2022-10-02 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0010_remove_profile_following_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core_app.tweet'),
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
