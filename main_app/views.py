from re import X
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from plotly.offline import plot
from plotly.graph_objs import Scatter
from .models import Ride

# Create your views here.
def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

@login_required
def rides_index(request):
    rides = Ride.objects.filter(user=request.user)
    date_data = []
    distance_data = []
    for ride in rides:
        date_data.append(ride.date)
        distance_data.append(ride.distance)
    plot_div = (plot([Scatter(x = date_data, y = distance_data,
                                name='rides', mode='markers',
                                opacity=0.8, marker_color='green', marker_size=10,
                                marker_line = dict(color='black', width=1))],
                    output_type='div'))

    return render(request, 'main_app/rides/index.html', {'rides':rides, 'plot_div':plot_div}) 

@login_required
def dashboard(request):
    rides = Ride.objects.filter(user=request.user)
    distance_sum = 0
    elevation_sum = 0 
    for ride in rides:
        distance_sum += ride.distance
        elevation_sum += ride.elevation
    date_data = []
    distance_data = []
    for ride in rides:
        date_data.append(ride.date)

        distance_data.append(ride.distance)
    plot_div = (plot([Scatter(x = date_data, y = distance_data,
                                name='rides', mode='markers',
                                opacity=0.8, marker_color='green', marker_size=10,
                                marker_line = dict(color='black', width=1))],
                    output_type='div'))
    return render(request, 'main_app/dashboard.html', {'distance_sum':distance_sum, 'elevation_sum':elevation_sum, 'plot_div':plot_div})

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
            return redirect('dashboard')
        else:
            error_message = 'Invalid Sign Up - Try Again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class RideCreate(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['route', 'date', 'distance', 'elevation', 'duration', 'avg_speed', 'description']
    success_url = '/dashboard'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RideUpdate(LoginRequiredMixin, UpdateView):
    model = Ride
    fields = ['route', 'date', 'distance', 'elevation', 'duration', 'avg_speed', 'description']
    
class RideDelete(LoginRequiredMixin, DeleteView):
    model = Ride
    success_url = '/rides/'