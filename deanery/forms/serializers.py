from dataclasses import field

from rest_framework import serializers
from django.db import transaction
from .models import *


class FormDataTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = FormDataType
        fields = '__all__'


class ShortTextFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    form = serializers.IntegerField(required=False)

    class Meta:
        model = ShortTextField
        fields = '__all__'

    def to_internal_value(self, data):
        type_data = data.get('form_data_type')
        if isinstance(type_data, FormDataType):
            data['form_data_type'] = type_data.pk
        obj = super(ShortTextFieldSerializer, self).to_internal_value(data)
        return obj


class ChoicesListFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    form = serializers.IntegerField(required=False)

    class Meta:
        model = ChoicesListField
        fields = '__all__'

    def to_internal_value(self, data):
        type_data = data.get('form_data_type')
        if isinstance(type_data, FormDataType):
            data['form_data_type'] = type_data.pk
        obj = super(ChoicesListFieldSerializer, self).to_internal_value(data)
        return obj


class FormSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
    short_text_fields = ShortTextFieldSerializer(many=True, required=False)
    choices_list_fields = ChoicesListFieldSerializer(many=True, required=False)

    class Meta:
        model = Form
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        fields_dict = dict()
        if 'short_text_fields' in validated_data:
            fields_dict['short_text_fields'] = validated_data.pop('short_text_fields')
        if 'choices_list_fields' in validated_data:
            fields_dict['choices_list_fields'] = validated_data.pop('choices_list_fields')

        new_form = self.Meta.model.objects.create(**validated_data)

        if 'short_text_fields' in fields_dict:
            short_text_fields_data = fields_dict.pop('short_text_fields')
            for data in short_text_fields_data:
                short_text_field_serializer = ShortTextFieldSerializer(
                    data=data
                )
                if short_text_field_serializer.is_valid():
                    short_text_field_serializer.save(form=new_form)
                else:
                    raise serializers.ValidationError(short_text_field_serializer.errors)

        if 'choices_list_fields' in fields_dict:
            choices_list_fields_data = fields_dict.pop('choices_list_fields')
            for data in choices_list_fields_data:
                choices_list_fields_serializer = ChoicesListFieldSerializer(
                    data=data
                )
                if choices_list_fields_serializer.is_valid():
                    choices_list_fields_serializer.save(form=new_form)
                else:
                    raise serializers.ValidationError(choices_list_fields_serializer.errors)

        return new_form


class FormWithoutFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
