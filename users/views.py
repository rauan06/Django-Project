from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def logout_view(request):
    """Logout"""
    logout(request)
    return render(request, 'learning_logs/index.html')

def register(request):
    """Register a new user"""
    if request.method != 'POST':
        # Display registration form
        form = UserCreationForm()
    else:
        """Form was filled"""
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and rediret to home page
            auth_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, auth_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form' : form}
    return render(request, 'users/register.html', context)