from rest_framework import views
from rest_framework import response
from django.db.models import ObjectDoesNotExist
from .serializers import FormSerializer
from .models import ShortTextField, ChoicesListField
from .models import Form

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
        short_text_fields = ShortTextField.objects.filter(form_id=form_id).select_related()
        choices_list_fields = ChoicesListField.objects.filter(form_id=form_id).select_related()
        if short_text_fields.exists():
            form_data['short_text_fields'] = [
                {**field.__dict__, "form_data_type": field.form_data_type.pk} for field in short_text_fields
            ]
        if choices_list_fields.exists():
            form_data['choices_list_fields'] = [
                {**field.__dict__, "form_data_type": field.form_data_type.pk} for field in choices_list_fields
            ]
        model_serializer = FormSerializer(data=form_data)
        model_serializer.is_valid(raise_exception=True)
        return response.Response(model_serializer.data)

