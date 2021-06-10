# Generated by Django 3.2 on 2021-06-09 22:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('swift_lyrics', '0006_alter_vote_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='year',
            field=models.IntegerField(help_text="Vote state - it's whether the Lyric has been upvoted(1)/downvoted(-1) by the user", null=True, validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2021)]),
        ),
        migrations.AlterField(
            model_name='vote',
            name='state',
            field=models.IntegerField(default=0, help_text="Vote state - it's whether the Lyric has been upvoted(1)/downvoted(-1) by the user", validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('user', 'lyric')},
        ),
    ]
