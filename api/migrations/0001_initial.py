# Generated by Django 4.0 on 2022-01-17 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMembersT',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('pokemon_id', models.IntegerField()),
            ],
            options={
                'db_table': 'team_members_t',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TeamsDataT',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('creation_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'teams_data_t',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TrainersDataT',
            fields=[
                ('trainer_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('alias', models.CharField(max_length=45)),
                ('age', models.IntegerField()),
                ('creation_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'trainers_data_t',
                'managed': False,
            },
        ),
    ]