# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choose_me', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=75)),
                ('token', models.CharField(max_length=11)),
            ],
        ),
    ]
