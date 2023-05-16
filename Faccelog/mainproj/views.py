from array import array
from email import message
from hmac import new
from multiprocessing import context
from pickle import TRUE
from urllib import request
from django.contrib import messages
from django.core.exceptions import *
from email.mime import image
from nturl2path import url2pathname
from unicodedata import name
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User_Info
import cv2,os
import face_recognition
# Create your views here.

#main function which compare the faces       
def compare(loc):
        
        cam = cv2.VideoCapture(0)   
        s, img = cam.read()
        if s:   
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,'mainproj')

                loc=(str(MEDIA_ROOT)+str(loc))
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
                # print(face_1_face_encoding)

                # capturing the image of the user in real time and encoding

                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encods = face_recognition.face_encodings(rgb_small_frame, face_locations)
                # print(face_encods)

                check=face_recognition.compare_faces(face_1_face_encoding, face_encods)
                

                # print(check)
                if check[0]:
                        return True

                else :
                        return False  
                    
                    
def facedect(loc):
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,'mainproj')

                loc=(str(MEDIA_ROOT)+str(loc))
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
                return face_1_face_encoding


def index(request):
    try:
        return (render(request, "index.html"))
    except BaseException as e:
            messages.error(request,repr(e))
            # messages.error(request,"Face is not detected. Please stay close to camera")
            return redirect("index")

    

def login(request):
    try:
        return (render(request, "login.html"))
    except BaseException as e:
            messages.error(request,repr(e))
            # messages.error(request,"Face is not detected. Please stay close to camera")
            return redirect("index")
        

def register(request):
    if request.method == 'POST':
        try:
            fn = request.POST.get("txt_fn")
            ln = request.POST.get("txt_ln")
            u_id = request.POST.get("txt_uid")
            email = request.POST.get("txt_email")
            name = fn + " " + ln
            image = request.FILES['image']
            #to check if the user_id already exists or not 
            if User_Info.objects.filter(user_id=u_id).exists():
                #User.objects.filter(username=self.cleaned_data['username']).exists():
                messages.error(request,"user already exists")
                return render(request, 'login.html') 
            else: 
                newaccount = User_Info()
                newaccount.user_name = name
                newaccount.user_id = u_id
                newaccount.email = email
                newaccount.image = image
                newaccount.save()
                #to check if the face is detected or not from the image uploaded by the user
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,'mainproj')
                loc = newaccount.image.url
                loc=(str(MEDIA_ROOT)+str(loc))
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
                messages.success(request, 'Account created succesfully. Now you can login.')
                return render(request, 'login.html')
        except IndexError:
            #This means that the face_recognition module couldn't find any faces i
            os.remove(newaccount.image.path)
            newaccount.delete()
            messages.error(request,"face is not detected in the provided image please provide correct image")
            return redirect("index")
        
def checkuser(request):
    try:
        if request.method == 'POST':
            try:
                u_id = request.POST.get("txt_uid")
                if User_Info.objects.filter(user_id=u_id).exists():
                    user = User_Info.objects.get(user_id=u_id)
                    # passing the url of the image
                    loc = user.image.url
                    #print(loc)
                    #checking if the user and the picture present in database matches or not 
                    if compare(loc):
                        request.session['name'] = u_id
                        # print(request.session.get('name'))
                        return redirect("welcome")
                    else:
                        return redirect("login")
                else:
                    messages.error(request,"User does not exists. Create a account or enter valid user id ")
                    return(redirect('index'))
            except IndexError as e:
                messages.error(request,"Face is not detected. Please stay close to camera")
                return redirect("login")
    except BaseException as e:
        messages.error(request,repr(e))
        return redirect("login")

def welcome(request):
    try:
        if (request.session.get('name'))!=None:
            # print(request.session.get('name'))
            u_id = request.session.get('name')
            user = User_Info.objects.get(user_id=u_id)
            context = {'user_info':user}
            return(render(request,"welcome.html",context))
    
        else:
            messages.info(request,"You need to login first")
            return (redirect("login"))
    except BaseException as e:
            messages.error(request,repr(e))
            return redirect("login")

def edit_profile(request):
    try:
        if (request.session.get('name'))!=None:
            u_id = request.session.get('name')
            user = User_Info.objects.get(user_id=u_id)
            context = {'user_info':user}
            return(render(request,"edit_profile.html",context))
        else:
            messages.info(request,"You need to login first")
            return (redirect("login"))
    except BaseException as e:
            messages.error(request,repr(e))
            return redirect("login")

def view_profile(request):
    try:
        if (request.session.get('name'))!=None:
            u_id = request.session.get('name')
            user = User_Info.objects.get(user_id=u_id)
            # print(user.user_name)
            context = {'user_info':user}
            return(render(request,"view_profile.html",context))
        else:
            messages.info(request,"You need to login first")
            return (redirect("login"))
    except BaseException as e:
            messages.error(request,repr(e))
            return redirect("login")
    

def log_out(request):
    try:
        del request.session['name']
        messages.success(request,"You are logged out.")
        return(redirect("login"))
    except BaseException as e:
            messages.error(request,repr(e))
            return redirect("login")
        
def update(request):
    if request.method == 'POST':
        try:
            if request.POST.get('Update'):
                new_name = request.POST.get("txt_name")
                new_email = request.POST.get("txt_email")
                u_id = request.session.get('name')
                userobject = User_Info.objects.get(pk=u_id) 
                if len(request.FILES) == 0:
                    # print(user.user_id)
                    #you can not change the primary key.
                    userobject.user_name = new_name
                    userobject.email = new_email
                    userobject.save()
                    messages.success(request,"Account updated sucssesfully.")
                    return(redirect("view_profile"))
                else: 
                    try:
                        new_uid = request.POST.get("txt_uid")
                        new_image = request.FILES['image']
                        newaccount = User_Info()
                        newaccount.user_name = new_name
                        newaccount.user_id = "temp"
                        newaccount.email = new_email
                        newaccount.image = new_image
                        newaccount.save()
                        #to check if the face is detected or not from the image uploaded by the user
                        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                        MEDIA_ROOT =os.path.join(BASE_DIR,'mainproj')
                        loc = newaccount.image.url
                        loc=(str(MEDIA_ROOT)+str(loc))
                        face_1_image = face_recognition.load_image_file(loc)
                        face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]
                        finalsaveuser = User_Info()
                        finalsaveuser.user_name = new_name
                        finalsaveuser.email = new_email
                        finalsaveuser.image = new_image
                        finalsaveuser.user_id= new_uid
                        finalsaveuser.save()
                        os.remove(userobject.image.path)
                        os.remove(newaccount.image.path)
                        newaccount.delete()
                        del request.session['name']
                        messages.success(request, 'Account updated sucessfully.')
                        return redirect("login")
                    except IndexError:
                        #This means that the face_recognition module couldn't find any faces i
                        os.remove(newaccount.image.path)
                        newaccount.delete()
                        messages.error(request,"face is not detected in the provided image please provide correct image")
                        return redirect("edit_profile")
            if request.POST.get('Delete'):
                u_id = request.session.get('name')
                userobject = User_Info.objects.get(pk=u_id)
                userobject.delete()
                del request.session['name']
                messages.success(request, 'Account deleted sucessfully.')
                return redirect("login")   
        except BaseException as e:
            messages.error(request,repr(e))
            return redirect("login")