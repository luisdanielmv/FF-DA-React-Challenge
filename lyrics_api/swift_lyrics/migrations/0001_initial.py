# Generated by Django 3.2 on 2021-04-16 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True, help_text='Album name', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True, help_text='Song name', unique=True)),
                ('album', models.ForeignKey(help_text='Album', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='swift_lyrics.album')),
            ],
        ),
        migrations.CreateModel(
            name='Lyric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(db_index=True, help_text='Lyrics from a song/album')),
                ('votes', models.IntegerField(default=0)),
                ('song', models.ForeignKey(help_text='Song', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lyrics', to='swift_lyrics.song')),
            ],
        ),
    ]
