# Generated by Django 4.0 on 2022-03-04 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=10)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=10)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_details', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.month')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.year')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_details', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.month')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.year')),
            ],
        ),
    ]