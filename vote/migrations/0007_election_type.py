# Generated by Django 4.2.6 on 2023-10-31 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_electeur_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='type',
            field=models.CharField(choices=[('Scrutin de liste', 'Scrutin De Liste'), ('Vote simple', 'Vote Simple')], default='Scrutin de liste', max_length=20),
        ),
    ]