# Generated by Django 5.0.6 on 2024-08-11 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_alter_reviewdetails__review_text_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviews',
            options={'verbose_name_plural': '口コミ'},
        ),
        migrations.AddIndex(
            model_name='reviews',
            index=models.Index(fields=['source', 'synergy_id'], name='reviews_rev_source__497c0c_idx'),
        ),
    ]
