# Generated by Django 2.0.4 on 2018-04-20 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0007_auto_20180413_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='fun',
            field=models.IntegerField(choices=[(1, 'Yes'), (0, 'No')]),
        ),
    ]
