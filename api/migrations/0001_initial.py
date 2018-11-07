# Generated by Django 2.1.2 on 2018-10-30 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('businessCode', models.CharField(db_column='business_code', default='sit', max_length=255)),
                ('businessLine', models.CharField(db_column='business_line', max_length=255)),
                ('remark', models.CharField(db_column='remark', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='EcsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instanceId', models.CharField(db_column='instance_id', max_length=255)),
                ('instanceName', models.CharField(db_column='instance_name', max_length=255)),
                ('productCode', models.CharField(db_column='product_code', max_length=255)),
                ('businessLine', models.CharField(db_column='business_line', max_length=255)),
                ('env', models.CharField(db_column='env', max_length=255)),
                ('regionId', models.CharField(db_column='region_id', max_length=255)),
                ('status', models.CharField(db_column='status', max_length=255)),
                ('instanceNetworkType', models.CharField(db_column='instance_networktype', max_length=255)),
                ('publicIpAddress', models.CharField(db_column='public_ipaddress', max_length=255)),
                ('primaryIpAddress', models.CharField(db_column='primary_ipaddress', max_length=255)),
                ('cpuMemory', models.CharField(db_column='cpu_memory', max_length=255)),
                ('osType', models.CharField(db_column='os_type', max_length=255)),
                ('osName', models.CharField(db_column='os_name', max_length=255)),
                ('hostame', models.CharField(db_column='hostname', max_length=255)),
                ('yunDisk', models.CharField(db_column='yundisk', max_length=255)),
                ('creationTime', models.CharField(db_column='create_time', max_length=255)),
                ('expiredTime', models.CharField(db_column='expired_time', max_length=255)),
                ('remark', models.CharField(db_column='remark', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='KeyIdSecret',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyId', models.CharField(db_column='key_id', max_length=255)),
                ('keySecret', models.CharField(db_column='key_secret', max_length=255)),
                ('regionId', models.CharField(db_column='region_id', max_length=1024)),
                ('accountNumber', models.CharField(db_column='account_number', max_length=1024)),
                ('defaultEnv', models.CharField(db_column='default_env', max_length=255)),
                ('remark', models.CharField(db_column='remark', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='ProductName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productcode', models.CharField(max_length=255)),
                ('commodityname', models.CharField(max_length=255)),
                ('commoditycode', models.CharField(max_length=255)),
                ('remark', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(1, '普通用户'), (2, 'VIP'), (3, 'SVIP')], default=1)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.UserInfo')),
            ],
        ),
    ]
