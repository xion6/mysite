# Generated by Django 5.0.6 on 2024-08-11 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_alter_reviewdetail_table_comment_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Corporations',
            new_name='Corporation',
        ),
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
        migrations.RenameModel(
            old_name='Staffs',
            new_name='Staff',
        ),
        migrations.AlterModelTableComment(
            name='reviewitem',
            table_comment='口コミのレビュー項目',
        ),
    ]
