# Generated by Django 5.0.6 on 2024-08-11 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_alter_reviews_options_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='reviewdetails',
            index=models.Index(fields=['review', 'item'], name='reviews_rev_review__0c0df6_idx'),
        ),
    ]
