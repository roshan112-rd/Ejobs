# Generated by Django 3.0.7 on 2021-04-06 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_appliedjobs_usercv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_category',
            field=models.CharField(choices=[('finance', 'Finance'), ('marketing', 'Marketing'), ('webdesign', 'Webdesign'), ('accountant', 'Accountant'), ('management', 'Management'), ('technology', 'Technology'), ('hardware', 'hardware'), ('others', 'Others')], default='others', max_length=250),
        ),
    ]
