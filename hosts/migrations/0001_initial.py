# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Binding',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('name', models.CharField(max_length=64)),
                ('start', models.DateTimeField(verbose_name='DHCP assigned')),
            ],
        ),
        migrations.CreateModel(
            name='MacAddr',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('mac', models.CharField(max_length=20)),
                ('vendor', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='binding',
            name='mac',
            field=models.ForeignKey(to='hosts.MacAddr'),
        ),
    ]
