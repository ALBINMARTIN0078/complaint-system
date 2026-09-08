from django.shortcuts import render, redirect

from .models import Complaint,User
from .forms import ComplaintForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/complaints/login/')
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()

    return render(request, 'submit_complaint.html', {'form': form})

def complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'complaint_list.html', {'complaints': complaints})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('login')

    return render(request, 'signup.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('submit_complaint')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')