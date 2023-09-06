from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

# Index
# TODO: Landing pgae, create templates and designs
def index (request):
    return render(request, 'index.html')


def crm(request):
    return render('crm.html')


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
