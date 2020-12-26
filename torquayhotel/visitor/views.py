from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView, View, FormView, ListView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Profile, Room, Reservation, Request
from .forms import MyUserCreationForm, AvailabilityForm
from .models import Request
from .request import RequestForm
from django.views.decorators.csrf import csrf_exempt
import os
from visitor.booking_functions.availability import check_availability




class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')     


class Register(View):

    def get(self, request):
        form = MyUserCreationForm()
        return render(request, 'registration/register.html', {"form": form})

    def post(self, request):

        form = MyUserCreationForm(request.POST)
        picture = request.POST['picture']
        nickname = request.POST['nickname']
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, picture=picture, nickname=nickname)
            # Authentication should always be done before login....
            # In this case, we just created the user successfully, so obviously the authenticate will work.
            user = authenticate(request, username= form.cleaned_data['username'], password= form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('homepage')

        return render(request, 'registration/register.html', {"form": form})




class RoomList(ListView):
    model = Room



class BookingList(ListView):
    model = Reservation


class RoomDetailView(View):

    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)
    
        if len(room_list) >0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context ={
                'room_category': room_category,
                'form': form
            }
            return render(request, 'detail.html', context)
        else:
            return HttpResponse('Category does not exist')



    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=['room_category'])
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms)>0:
            room = available_rooms[0]
            booking = Reservation.objects.create(
                user = self.request.profile,
                room = room,
                check_in =  data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked, try another one')




class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(category=data['room_category'])
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms)>0:
            room = available_rooms[0]
            booking = Reservation.objects.create(
                user = self.request.profile,
                room = room,
                check_in =  data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked, try another one')







def request(request):
    if request.method == "POST":
        form = RequestForm(request.POST).save()
        return redirect('homepage')
    else:
        form = RequestForm()
    return render(request, 'request.html', {'form' : form})




# # @csrf_exempt  
# def asyncdemo(request):
#     data = json.loads(request.body)
#     print("User is typing...", data['text'])

#     data2 = {
#         "uppertext": data['text'].upper(),
#     }

#     return HttpResponse(json.dumps(data2))



# def asyncadduser(request):
#     data = json.loads(request.body)
#     print("Data Received.", "Username:", data['text'])
#     try:
#         user = User.objects.create_user(username=data['text'], password=data['text']) 
#         print("Success")
#         return HttpResponse(json.dumps({'status':'success', 'message':'User created'}))
#     except:
#         print("Error")
#         return HttpResponse(json.dumps({'status':'error', 'message':'User could not be created'}))



def homepage(request):
    return render(request, 'homepage.html')


def booking(request):
    return render(request, 'bookinglist.html')

def review(request):
    return render(request, 'review.html')

def gallery(request):
    return render(request, 'gallery.html')

def moreinfo(request):
    return render(request, 'moreinfo.html')


