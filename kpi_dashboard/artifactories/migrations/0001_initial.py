# Generated by Django 4.1.7 on 2023-12-21 00:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artifactories',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
                ('status', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
