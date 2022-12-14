# Generated by Django 4.1.1 on 2022-10-03 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0011_tweet_reply_to_delete_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='core_app.tweet'),
        ),
    ]
