# Generated by Django 2.1.3 on 2018-12-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('accuracy', models.IntegerField()),
                ('file', models.FileField(upload_to='models/%Y/%m/%d')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(default='Annonymous', max_length=120)),
            ],
        ),
    ]
