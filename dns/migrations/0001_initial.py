# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DnsQuery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('src', models.GenericIPAddressField()),
                ('host', models.CharField(max_length=128)),
                ('start', models.DateTimeField(verbose_name='DNS query')),
            ],
        ),
    ]
