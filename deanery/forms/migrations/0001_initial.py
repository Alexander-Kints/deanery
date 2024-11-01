# Generated by Django 5.1.2 on 2024-11-01 17:16

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChoicesListFieldType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
            ],
            options={
                'db_table': 'choices_list_field_type',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('patronymic', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='FormDataType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'form_data_type',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('patronymic', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='TextFieldType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
            ],
            options={
                'db_table': 'text_field_type',
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.employee')),
            ],
            options={
                'db_table': 'form',
            },
        ),
        migrations.CreateModel(
            name='ChoicesListField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('priority_on_form', models.IntegerField()),
                ('is_required', models.BooleanField()),
                ('content', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('choices_list_field_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.choiceslistfieldtype')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.form')),
                ('form_data_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.formdatatype')),
            ],
            options={
                'db_table': 'choices_list_field',
            },
        ),
        migrations.CreateModel(
            name='ChoicesListFieldResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('response', models.CharField(max_length=255)),
                ('choices_list_field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.choiceslistfield')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.student')),
            ],
            options={
                'db_table': 'choices_list_field_response',
            },
        ),
        migrations.CreateModel(
            name='TextField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('priority_on_form', models.IntegerField()),
                ('is_required', models.BooleanField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.form')),
                ('form_data_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.formdatatype')),
                ('text_field_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.textfieldtype')),
            ],
            options={
                'db_table': 'text_field',
            },
        ),
        migrations.CreateModel(
            name='TextFieldResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('response', models.CharField(max_length=255)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.student')),
                ('text_field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forms.textfield')),
            ],
            options={
                'db_table': 'text_field_response',
            },
        ),
    ]
