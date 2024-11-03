from rest_framework import serializers
from django.db import transaction
from django.db.models import ObjectDoesNotExist
from .models import *


class TextFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    form = serializers.IntegerField(required=False)

    class Meta:
        model = TextField
        fields = '__all__'

    def to_internal_value(self, data):
        type_data = data.get('form_data_type')
        text_type_data = data.get('text_field_type')
        if isinstance(type_data, FormDataType) and isinstance(text_type_data, TextFieldType):
            data['form_data_type'] = type_data.pk
            data['text_field_type'] = text_type_data.pk
        obj = super(TextFieldSerializer, self).to_internal_value(data)
        return obj


class ChoicesListFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    form = serializers.IntegerField(required=False)

    class Meta:
        model = ChoicesListField
        fields = '__all__'

    def to_internal_value(self, data):
        type_data = data.get('form_data_type')
        field_type_data = data.get('choices_list_field_type')
        if isinstance(type_data, FormDataType) and isinstance(field_type_data, ChoicesListFieldType):
            data['form_data_type'] = type_data.pk
            data['choices_list_field_type'] = field_type_data.pk
        obj = super(ChoicesListFieldSerializer, self).to_internal_value(data)
        return obj


class FormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    text_fields = TextFieldSerializer(many=True, required=False)
    choices_list_fields = ChoicesListFieldSerializer(many=True, required=False)

    class Meta:
        model = Form
        fields = '__all__'

    def __tx_create_objects(self, field_name: str, fields_dict: dict,
                            model_serializer, form) -> None:
        if field_name in fields_dict:
            fields_data = fields_dict.pop(field_name)
            for data in fields_data:
                field_serializer = model_serializer(
                    data=data
                )
                if field_serializer.is_valid():
                    field_serializer.save(form=form)
                else:
                    raise serializers.ValidationError(field_serializer.errors)

    @transaction.atomic
    def create(self, validated_data):
        fields_dict = dict()
        if 'text_fields' in validated_data:
            fields_dict['text_fields'] = validated_data.pop('text_fields')
        if 'choices_list_fields' in validated_data:
            fields_dict['choices_list_fields'] = validated_data.pop('choices_list_fields')
        new_form = self.Meta.model.objects.create(**validated_data)
        self.__tx_create_objects('text_fields', fields_dict, TextFieldSerializer, new_form)
        self.__tx_create_objects('choices_list_fields', fields_dict, ChoicesListFieldSerializer, new_form)
        return new_form

    @staticmethod
    def get_form_data_by_pk(pk: int) -> dict:
        try:
            form = Form.objects.get(pk=pk)
            form_data = {
                **form.__dict__,
                "employee": form.employee.pk,
            }
        except ObjectDoesNotExist:
            raise serializers.ValidationError("object does not exist")
        text_fields = TextField.objects.filter(form_id=pk).select_related()
        choices_list_fields = ChoicesListField.objects.filter(form_id=pk).select_related()
        if text_fields.exists():
            form_data['text_fields'] = [
                {**field.__dict__, "form_data_type": field.form_data_type.pk,
                 "text_field_type": field.text_field_type.pk} for field in text_fields
            ]
        if choices_list_fields.exists():
            form_data['choices_list_fields'] = [
                {**field.__dict__, "form_data_type": field.form_data_type.pk,
                 "choices_list_field_type": field.choices_list_field_type.pk} for field in choices_list_fields
            ]
        return form_data

class FormWithoutFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
