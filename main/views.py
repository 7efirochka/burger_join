from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Images
from django.contrib.auth import login

# Create your views here.
def view(request):
    image = Images.objects.all()
    return render(request, 'main/main_page.html', {'image': image})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/menu/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registrate.html', {'form': form})

