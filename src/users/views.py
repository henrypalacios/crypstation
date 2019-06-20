from django.contrib import messages, auth
from django.http import HttpResponse
from django.shortcuts import render, redirect


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'users/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('')


def home(request):
      #user_accounts = Account.objects.all()
      #
      # context = {
      #   'contacts': user_contacts
      # }

      #return HttpResponse('Juee')
      return render(request, 'app.html')