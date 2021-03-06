# Generated by Django 3.1.7 on 2021-04-08 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinchart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequence',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='sequence',
            unique_together={('pinchart', 'number')},
        ),
    ]
