# Generated by Django 3.0.4 on 2020-03-09 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_auto_20200309_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2048, verbose_name='user comments')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.State')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StateChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_type', models.CharField(choices=[('service_change', 'Changed Service'), ('value_change', 'Changed State'), ('filed_at', 'Filed Time'), ('forecast', 'Update Forecast Changed')], max_length=128)),
                ('old_value', models.CharField(max_length=2048, verbose_name='the original value of the state property')),
                ('new_value', models.CharField(max_length=2048, verbose_name='the current value of the state property')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.State')),
            ],
        ),
    ]
