from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, credentials
import pandas as pd
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import os

#Twilio access
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant



# Create your views here.

# Index
# TODO: Landing pgae, create templates and designs
def index (request):
    """Landing page"""
    return render(request, 'index.html')


#caller 

def caller(request):
    return render(request, 'caller.html')

class GetToken(APIView):
    """Returns Token to instantiate Twilio.Device"""

    def get(self, request, *args, **kwargs):
        identity = request.user.username
        # Create access token with credentials
        access_token = AccessToken(credentials.TWILIO_ACCOUNT_SID, credentials.TWILIO_API_KEY, credentials.TWILIO_API_SECRET, identity=identity)

        # Create a Voice grant and add to token
        voice_grant = VoiceGrant(
            outgoing_application_sid=credentials.TWIML_APPLICATION_SID,
            incoming_allow=True, # Optional: add to allow incoming calls
        )
        access_token.add_grant(voice_grant)

        token = access_token.to_jwt()

        data = {
            'token' : token,
        }
        return Response(data)
        

# CALL RESPONSE
class Call(APIView):
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """Returns TwiML instructions to Twilio's POST requests"""
        response = VoiceResponse()
        dial = response.dial(caller_id=credentials.TWILIO_NUMBER)

    
        dial.number('+15629914465')
        
        return HttpResponse(
            str(response), content_type='application/xml; charset=utf-8'
        )



def upload_DB(file_path):
    df = pd.read_csv(file_path,delimiter=',')
    list_of_csv = [list(row) for row in df.values]

    for l in list_of_csv:
        models.Record.objects.create(       

            first_name = l[0],
            last_name = l[1],
            address = l[2],
            city =  l[3],          
            zipcode = l[4],
            phone1 = l[5],
            phone2 = l[6],
            phone3 = l[7],

        )





# Delete Data Base Function
def delete_records(request):
    models.Record.objects.all().delete()
    return redirect('crm')

# Control Records Management
def crm(request):

    records = models.Record.objects.all()  

    if request.method == 'POST':
        file = request.FILES['file']
        obj = models.RecordsFile.objects.create(file = file)
        upload_DB(obj.file)
        return redirect('crm')



    


    return render(request, 'crm.html',{'records': records})


#Login
def login(request):
    if request.method == 'POST':
        username = request.POST ['username']
        password = request.POST ['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('crm')
        else:
            error_message = 'User or password incorrect'
            return render(request, 'login.html', {'error_message': error_message})
  
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST ['username']
        email = request.POST ['email']
        password1 = request.POST ['password1']
        password2 = request.POST ['password2']
        if password1 == password2:
            try:
                user = auth.models.User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return (redirect('crm'))
            except:
                error_message = 'Error creating account'
                    
        else:
            error_message = 'password dont match'
            return render(request, 'register.html', {'error_message': error_message})

    
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
