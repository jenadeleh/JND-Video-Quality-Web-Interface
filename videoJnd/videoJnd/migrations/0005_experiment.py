# Generated by Django 3.1.6 on 2021-03-09 14:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('videoJnd', '0004_auto_20210309_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=20)),
                ('source_video', models.TextField(default='', max_length=4096)),
                ('rating', models.IntegerField(default=0, editable=False)),
                ('pub_date', models.DateTimeField()),
            ],
        ),
    ]
