# Generated by Django 3.1.6 on 2021-03-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoJnd', '0003_auto_20210309_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoobj',
            name='url',
        ),
        migrations.RemoveField(
            model_name='videoobj',
            name='video_name',
        ),
        migrations.AddField(
            model_name='videoobj',
            name='crf',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='videoobj',
            name='frame_rate',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='videoobj',
            name='source_video',
            field=models.CharField(default='', editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='videoobj',
            name='codec',
            field=models.CharField(default='', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='videoobj',
            name='count',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='videoobj',
            name='decisions',
            field=models.TextField(default='', editable=False, max_length=4096),
        ),
        migrations.AlterField(
            model_name='videoobj',
            name='exp',
            field=models.CharField(default='', editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='videoobj',
            name='ongoing',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='videoobj',
            name='rating',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='videoobj',
            name='user_record',
            field=models.TextField(default='', editable=False, max_length=4096),
        ),
    ]
