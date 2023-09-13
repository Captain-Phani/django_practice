from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Room,Topic
from .forms import RoomForm #inbuilt roomform
from django.db.models import Q # This module enables us to filter data based on different criterias based on logical operators
from django.contrib.auth import authenticate,login,logout
rooms=[
    {'id':1,'name':"Learning Python"},
    {'id':2,'name':"Learning Django"},
    {'id':3,'name':"Learning SQL"},
]
def home(request):
    #rooms=Room.objects.all() #Room-(created model) objects-(objects exist in Room model). all()-method to get all objects
    #topics=Topic.objects.all()
    q=request.GET.get('q') if(request.GET.get('q'))!= None else ''  #inline if condition
    #if the parameter 'q' is not  equal to none then fetch that parameter else keep that as an empty string
    rooms=Room.objects.filter(Q(topic__topic__icontains=q) |
                              Q(name__icontains=q) |
                              Q(description__icontains=q)
                              )
    print(rooms)
    #1st topic is a column of field in db and second topic  is a field associated to column and icontains is used to ignore case sensitive issues.
    topics=Topic.objects.all()

    roomsCount=rooms.count()
    context={'rooms':rooms,'topics':topics,'roomsCount':roomsCount}
    return render(request,'app1/home.html',context)
# return render(request,'app1/home.html',{'rooms':rooms}) Instead of mentioning dictionary like this code we can use context

# def room(request,pk): #Throw error if I haven't mentioned requrest object as paramenter
#     room=None #initially we assigned room value as None#     for tasks in rooms:  #for loop is used to get the id and filter with dynamic url id
  #      if(tasks['id']==int(pk)):
#             room=tasks
#     context={'room':room}
#     return render(request,"app1/room.html",context)
# render is a function which takes two paramenters (request,template name)


# def home(request):
#     return render(request,'app1/home.html')

def loginPage(request):
    if(request.method=="POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"username or password does not match")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid user")

    context={}
    return render(request,'app1/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def room(request,pk):

    room=Room.objects.get(id=pk)
    print(type(pk))
    # room=None
    # for i in rooms:
    #     if(i['id']==int(pk)):
    #         room=i


    return render(request,'app1/room.html',{'room':room})

#To create a room below fun is written
def create_room(request):
    form=RoomForm() # we are creating an empty instance and later we will send parameters to that instance
    if request.method=="POST":
        form=RoomForm(request.POST)
        #The code RoomForm(request.POST) creates an instance of the RoomForm class and initializes it with the data from request.
        # POST. This essentially binds the form to the data submitted in the POST request.
        #The RoomForm class defines the structure and validation rules for the form fields. It specifies
        # things like field types, required fields, and validation logic.
        # By passing request.POST as an argument, the form is populated with the data submitted by the
        # user, allowing you to work with and validate this data.

        if form.is_valid(): #After creating the instance the post details will be stored in form and we can validate the details exist in form.
            form.save() #if all the validations are satisfied the form will be saved.

            return redirect('home') # page will be redirected to home (home-urlname)

    context={'form': form}
    print(form)
    return render(request,'app1/room_form.html',context)
#After writing create_room use modal forms(converts model fields into forms) by creating a python file in app

#Request.Post:This is a dictionary-like object within the request object, which contains the data submitted via an
#             HTTP POST request. Specifically, it contains the form data submitted by the user when they interact with a web page.
#             Each key in request.POST corresponds to the name attribute of an HTML form field, and the values are the data entered by the user.

def update_room(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room) #we are prefilling the form with the details we fetched with the help of id
    if request.method=="POST":
        form=RoomForm(request.POST,instance=room) # The fetched details(request.Post) replaces aldready exisitng filled details
        if(form.is_valid()):
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'app1/room_form.html',context)

def delete_room (request,pk):
    room=Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,'app1/delete_room.html',{'obj':room})
