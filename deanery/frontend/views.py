from django.shortcuts import render

def show_form(request, form_id):
    return render(request, template_name='show_form.html')


def create_form(request):
    return render(request, template_name='create_form.html')

def form_list(request):
    return render(request, template_name='index.html')