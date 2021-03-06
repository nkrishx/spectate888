# Generated by Django 3.1.3 on 2020-11-23 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Markets',
            },
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('odds', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Selections',
            },
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Sports',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('start_time', models.DateTimeField()),
                ('markets', models.ManyToManyField(to='core.Market')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sport')),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.AddField(
            model_name='market',
            name='selections',
            field=models.ManyToManyField(related_name='markets', to='core.Selection'),
        ),
    ]
