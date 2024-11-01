from rest_framework import views
from rest_framework import response
from django.db.models import ObjectDoesNotExist
from rest_framework.generics import ListAPIView
from .serializers import FormSerializer, FormWithoutFieldsSerializer
from .models import TextField, ChoicesListField
from .models import Form, Employee, Student, FormDataType, TextFieldType, ChoicesListFieldType

class FormCreateAPIView(views.APIView):
    def post(self, request):
        model_serializer = FormSerializer(data=request.data)
        model_serializer.is_valid(raise_exception=True)
        pk = model_serializer.save().pk
        return response.Response({"message": "created", "id": pk})


class FormGetAPIView(views.APIView):
    def get(self, request, form_id):
        try:
            form = Form.objects.get(pk=form_id)
            form_data = {
                **form.__dict__,
                "employee": form.employee.pk,
            }
        except ObjectDoesNotExist:
            return response.Response({"error": "object does not exist"}, status=404)
        text_fields = TextField.objects.filter(form_id=form_id).select_related()
        choices_list_fields = ChoicesListField.objects.filter(form_id=form_id).select_related()
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
        model_serializer = FormSerializer(data=form_data)
        model_serializer.is_valid(raise_exception=True)
        return response.Response(model_serializer.data)


class FormListAPIView(ListAPIView):
    queryset = Form.objects.all()
    serializer_class = FormWithoutFieldsSerializer


class CreateTestDataAPIView(views.APIView):
    def post(self, request):
        Student.objects.create(name='Иван',patronymic='Иванович',surname='Петров')
        Student.objects.create(name='Игорь', patronymic='Петрович', surname='Колесников')
        Student.objects.create(name='Анна', patronymic='Александровна', surname='Шурова')
        Employee.objects.create(name='Антон', patronymic='Иванович', surname='Матросов')
        Employee.objects.create(name='Владимир', patronymic='Александрович', surname='Корыгин')
        Employee.objects.create(name='Андрей', patronymic='Владиславович', surname='Бирюзовский')
        FormDataType.objects.create(name='text field')
        FormDataType.objects.create(name='choices list')
        TextFieldType.objects.create(name='short text')
        TextFieldType.objects.create(name='long text')
        TextFieldType.objects.create(name='email')
        ChoicesListFieldType.objects.create(name='dropdown list')
        ChoicesListFieldType.objects.create(name='option buttons list')
        ChoicesListFieldType.objects.create(name='multiple choices list')
        return response.Response({"message": "Тестовые данные созданы"})
