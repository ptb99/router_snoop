# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostName',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='IpAddr',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField()),
            ],
        ),
        migrations.AlterField(
            model_name='binding',
            name='ip',
            field=models.ForeignKey(to='hosts.IpAddr'),
        ),
        migrations.AlterField(
            model_name='binding',
            name='name',
            field=models.ForeignKey(to='hosts.HostName'),
        ),
    ]
