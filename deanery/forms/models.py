from django.db import models
from django.contrib.postgres.fields import ArrayField


class BaseUserProperties(models.Model):
    name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Employee(BaseUserProperties):
    class Meta:
        db_table = 'employee'


class Student(BaseUserProperties):
    class Meta:
        db_table = 'student'


class Form(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey('forms.Employee', on_delete=models.PROTECT)

    class Meta:
        db_table = 'form'


class FormDataType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'form_data_type'


class BaseFieldProperties(models.Model):
    title = models.CharField(max_length=255)
    priority_on_form = models.IntegerField()
    is_required = models.BooleanField()
    form = models.ForeignKey('Form', on_delete=models.PROTECT)
    form_data_type = models.ForeignKey('FormDataType', on_delete=models.PROTECT)

    class Meta:
        abstract = True


class BaseResponseProperties(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey('Student', on_delete=models.PROTECT)

    class Meta:
        abstract = True


class TextField(BaseFieldProperties):
    text_field_type = models.ForeignKey('TextFieldType', on_delete=models.PROTECT)

    class Meta:
        db_table = 'text_field'


class TextFieldType(models.Model):
    name = models.CharField(max_length=127)

    class Meta:
        db_table = 'text_field_type'


class TextFieldResponse(BaseResponseProperties):
    response = models.CharField(max_length=255)
    text_field = models.ForeignKey('TextField', on_delete=models.PROTECT)

    class Meta:
        db_table = 'text_field_response'


class ChoicesListField(BaseFieldProperties):
    content = ArrayField(models.CharField(max_length=255))
    choices_list_field_type = models.ForeignKey('ChoicesListFieldType', on_delete=models.PROTECT)

    class Meta:
        db_table = 'choices_list_field'


class ChoicesListFieldType(models.Model):
    name = models.CharField(max_length=127)

    class Meta:
        db_table = 'choices_list_field_type'


class ChoicesListFieldResponse(BaseResponseProperties):
    response = models.CharField(max_length=255)
    choices_list_field = models.ForeignKey('ChoicesListField', on_delete=models.PROTECT)

    class Meta:
        db_table = 'choices_list_field_response'
