# Generated by Django 5.0.6 on 2024-08-10 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_reviewrevisions_options_alter_reviews_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='レビュー回答日時'),
        ),
    ]
