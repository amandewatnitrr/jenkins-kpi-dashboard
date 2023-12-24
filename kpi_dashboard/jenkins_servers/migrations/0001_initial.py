# Generated by Django 4.1.7 on 2023-12-24 02:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='jenkins_servers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('server_url', models.CharField(max_length=200)),
                ('server_up_time', models.CharField(max_length=200)),
                ('response_time', models.CharField(max_length=200)),
                ('network_latency', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
            ],
        ),
    ]