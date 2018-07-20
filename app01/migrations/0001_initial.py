# Generated by Django 2.0.7 on 2018-07-20 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('email', models.CharField(max_length=32, verbose_name='邮箱')),
                ('m2m', models.ManyToManyField(to='app01.Role', verbose_name='角色')),
                ('ug', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.UserGroup', verbose_name='用户组')),
            ],
        ),
    ]
