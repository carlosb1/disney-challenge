# Generated by Django 4.1.13 on 2024-02-02 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='images/', verbose_name='original_image')),
                ('generated_image', models.ImageField(upload_to='generated/', verbose_name='generated_image')),
                ('status', models.CharField(choices=[('C', 'COMPLETED'), ('R', 'READY'), ('E', 'ERROR')], default='R', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='image')),
            ],
        ),
    ]
