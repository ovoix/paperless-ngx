# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 12:21
from __future__ import unicode_literals

from django.db import migrations, models
from django.template.defaultfilters import slugify

import django.db.models.deletion


DOCUMENT_SENDER_MAP = {}


def move_sender_strings_to_sender_model(apps, schema_editor):

    sender_model = apps.get_model("documents", "Sender")
    document_model = apps.get_model("documents", "Document")

    # Create the sender and log the relationship with the document
    for document in document_model.objects.all():
        if document.sender:
            DOCUMENT_SENDER_MAP[document.pk], created = sender_model.objects.get_or_create(
                name=document.sender,
                defaults={"slug": slugify(document.sender)}
            )


def realign_senders(apps, schema_editor):
    document_model = apps.get_model("documents", "Document")
    for pk, sender in DOCUMENT_SENDER_MAP.items():
        document_model.objects.filter(pk=pk).update(sender=sender)


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0002_auto_20151226_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.RunPython(move_sender_strings_to_sender_model),
        migrations.RemoveField(
            model_name='document',
            name='sender',
        ),
        migrations.AddField(
            model_name='document',
            name='sender',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='documents.Sender'),
        ),
        migrations.RunPython(realign_senders),
    ]
