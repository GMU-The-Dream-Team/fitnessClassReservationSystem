# Generated by Django 3.1.3 on 2021-01-02 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_auto_20210102_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wait', models.CharField(default=None, max_length=1)),
            ],
        ),
    ]
