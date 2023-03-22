import json
import string

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views import View

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("solid-solstice-297612-29966102b7e1.json", scope)
client = gspread.authorize(credentials)


chars = tuple(string.punctuation + string.digits + "¨" + "´" + "`")

# validacion del nombre
class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        firstname = data['first_name']
        if any((c in chars) for c in firstname):
            return JsonResponse({'username_error': True}, status=400)

        return JsonResponse({'username_valid': True})


# validacion del apellido
class LastnameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        lastname = data['last_name']
        if any((c in chars) for c in lastname):
            return JsonResponse({'lastname_error': True}, status=400)

        return JsonResponse({'lastname_valid': True})

def update_counters(sheet):
    sinco_counter = 0
    veget_counter = 0
    vegan_counter = 0
    celia_counter = 0
    for i in sheet.col_values(2):
        if i == "Sin Condicion":
            sinco_counter += 1
        elif i == "Vegetariano":
            veget_counter += 1
        elif i == "Vegano":
            vegan_counter += 1
        elif i == "Celiaco":
            celia_counter += 1

    sheet.update('D1', [["Total de Invitados"]])
    sheet.update('D2', [["Sin Condicion", sinco_counter]])
    sheet.update('D3', [["Vegetariano", veget_counter]])
    sheet.update('D4', [["Vegano", vegan_counter]])
    sheet.update('D5', [["Celiaco", celia_counter]])

# validacion y registro de usuario en la base de datos
class RegistrationView(View):
    
    
    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        
        first_name = request.POST.get('first_name').title()
        last_name = request.POST.get('last_name').title()
        menu = request.POST.get('menu')

        # context = {
        #     'fieldValues': request.POST
        # }

        nombre_completo = last_name + " " + first_name

        if len(first_name) == 0 or len(last_name) == 0 or menu == 'none':
            return JsonResponse({'username_error': 'FILL BLANK FIELDS!'}, status=400)
        elif User.objects.filter(username=nombre_completo).exists():
            return JsonResponse({'username_error': 'A GUEST WITH THAT NAME ALREADY EXISTS'}, status=400)
        else:
            sheet = client.open("test").sheet1

            data = {'first_name': first_name, 'last_name': last_name, 'menu':menu, 'username_success': 'CONFIRMED SUCCESSFULLY'}
            user = User.objects.create_user(username=nombre_completo, first_name=first_name, last_name=last_name, email=menu)
    
            next_row = len(sheet.col_values(1)) + 1
            sheet.update('A{}'.format(next_row), [[nombre_completo, menu]])

            update_counters(sheet)

            user.set_unusable_password()
            user.is_active = False
            user.save()

            return JsonResponse(data, safe=False)


        return render(request, 'main/index.html')