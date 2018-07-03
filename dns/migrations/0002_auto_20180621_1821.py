# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dns', '0001_initial'),
        ('hosts', '0002_auto_20180621_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dnsquery',
            name='src',
            field=models.ForeignKey(to='hosts.IpAddr'),
        ),
    ]
