# Generated by Django 3.0.8 on 2020-08-31 09:33

import cards.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_auto_20200821_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(default=1, on_delete=models.SET(cards.models.get_sentinel_user), related_name='cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deck',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='decks', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='created_by',
            field=models.ForeignKey(on_delete=models.SET(cards.models.get_sentinel_user), related_name='created_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='deck',
            name='created_by',
            field=models.ForeignKey(on_delete=models.SET(cards.models.get_sentinel_user), related_name='created_decks', to=settings.AUTH_USER_MODEL),
        ),
    ]
