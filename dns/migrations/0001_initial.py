# Generated by Django 4.0.2 on 2023-02-28 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DnsQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=128)),
                ('start', models.DateTimeField(verbose_name='DNS query')),
                ('src', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.ipaddr')),
            ],
        ),
    ]
