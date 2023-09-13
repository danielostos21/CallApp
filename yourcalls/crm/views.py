from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from . import models
import pandas as pd

#Twilio access


# Create your views here.
from twilio.rest import Client
import os

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC99315eae5eb0c27cb6dc3ad41223e7ae'
auth_token = '42be11397b0b82ae2486e7d66c6575e8'
client = Client(account_sid, auth_token)

# Index
# TODO: Landing pgae, create templates and designs
def index (request):

    # call = client.calls.create(
    #     twiml='<Response><Dial><Conference>Test Call</Conference></Dial></Response>',
    #     to='+14699273179',
    #     from_='+18335371120'
    # )

    # print(call.sid)
    return render(request, 'index.html')



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







# Control Records Management
def crm(request):

    records = models.Record.objects.all()  

    if request.method == 'POST':
        file = request.FILES['file']
        obj = models.RecordsFile.objects.create(file = file)
        upload_DB(obj.file)






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
