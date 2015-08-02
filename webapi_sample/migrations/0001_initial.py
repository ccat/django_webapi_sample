# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idName', models.CharField(max_length=60)),
                ('hashed', models.CharField(max_length=60)),
                ('user', models.ForeignKey(related_name='webapi_credential', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
