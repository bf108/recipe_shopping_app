# Generated by Django 3.1.6 on 2021-03-04 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_ingredient_food_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='food_type',
            field=models.CharField(choices=[('VEG', 'Vegetable'), ('FRUIT', 'Fruit'), ('MEAT', 'Meat'), ('DAIRY', 'Dairy'), ('OTHER', 'Other')], default='OTHER', max_length=15, null=True),
        ),
    ]
