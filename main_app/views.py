from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ride

# Create your views here.
def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

@login_required
def rides_index(request):
    rides = Ride.objects.filter(user=request.user)
    return render(request, 'main_app/rides/index.html', {'rides':rides})

def rides_detail(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    return render(request, 'main_app/rides/detail.html',{'ride': ride})

def signup(request):
    error_message=''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('')
        else:
            error_message = 'Invalid Sign Up - Try Again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class RideCreate(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['route', 'date', 'distance', 'elevation', 'duration', 'avg_speed', 'description']
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RideUpdate(LoginRequiredMixin, UpdateView):
    model = Ride
    fields = ['route', 'date', 'distance', 'elevation', 'duration', 'avg_speed', 'description']
    
class RideDelete(LoginRequiredMixin, DeleteView):
    model = Ride
    success_url = '/rides/'