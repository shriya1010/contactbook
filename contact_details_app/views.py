from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json

from contact_details_app.models import Contact_Book
from contact_details_app.serializers import ContactBookSerializer
from rest_framework.decorators import api_view

from django.core.mail import send_mail
from Contact_Book_Details import settings
from django.http import HttpResponse

from twilio.rest import Client
from django.conf import settings

def login(request):
    return render(request,'contact_details_app/login.html')

def index(request):
    return render(request,'contact_details_app/list_of_contacts.html')

def signup(request):
    return render(request,'contact_details_app/signup.html')

def signup2(request):
    return render(request,'contact_details_app/login.html',{"signup":"Signup successfully! Please login with those credentials."})

def home(request):
    Contacts = Contact_Book.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(Contacts, 10)
    try:
        contacts_per_page = paginator.page(page)
    except PageNotAnInteger:
        contacts_per_page = paginator.page(1)
    except EmptyPage:
        contacts_per_page = paginator.page(paginator.num_pages)
    return render(request,'contact_details_app/list_of_contacts.html',{"contacts":contacts_per_page})

def add(request):
    if request.method=="POST":
        if request.POST["typed_name"]=="":
            return render(request,'contact_details_app/addcontact.html',{"error":"name cannot be empty!"})
        elif request.POST["email"]=="":
            return render(request,'contact_details_app/addcontact.html',{"error":"email cannot be empty!"})
        elif request.POST["contact"]=="":
            return render(request,'contact_details_app/addcontact.html',{"error":"contact number cannot be empty!"})
        elif request.POST["email"]:
            existing_email=Contact_Book.objects.filter(email=request.POST["email"])
            if existing_email.count()==1:
                return render(request,'contact_details_app/addcontact.html',{"error":"email already exists!"})
        new_contact=Contact_Book(name=request.POST["typed_name"],email=request.POST['email'],contact_number=request.POST['contact'])
        new_contact.save()
        return render(request,'contact_details_app/list_of_contacts.html',{"success":"contact added successfully!"})

def addcontact(request):
    return render(request,"contact_details_app/addcontact.html")

def delete(request,pk):
    record=Contact_Book.objects.get(id=pk)
    record.delete()
    return render(request,'contact_details_app/list_of_contacts.html',{"delete":"contact deleted successfully!"})
 
def mail(request,pk):
    record=Contact_Book.objects.get(id=pk)
    subject = request.POST["subject"]
    message = request.POST["message"]
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [record.email, ]
    send_mail( subject, message, email_from, recipient_list )

    return render(request,'contact_details_app/list_of_contacts.html',{"mail":"mail send successfully!"})
 
def send(request,pk):
    record=Contact_Book.objects.get(id=pk)
    a="+"
    b=record.contact_number    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.api.account.messages.create( to=a+b, from_="+18509902205", body=request.POST["msg"])
    
    #response = client.messages.create(body='Hello testing twilio in Django',  to=to, from_=settings.TWILIO_PHONE_NUMBER)
    return render(request,'contact_details_app/list_of_contacts.html',{"send":"sms send successfully!"})
 


def update(request,pk):
    record=Contact_Book.objects.get(id=pk)
    return render(request,"contact_details_app/updatecontact.html",{"record":record})

def update_contact(request,pk):
    record=Contact_Book.objects.get(id=pk) 
    if request.method=="POST":
        if request.POST["typed_name"]=="":
            return render(request,'contact_details_app/updatecontact.html',{"error":"name cannot be empty!"})
        elif request.POST["email"]=="":
            return render(request,'contact_details_app/updatecontact.html',{"error":"email cannot be empty!"})
        elif request.POST["contact"]=="":
            return render(request,'contact_details_app/updatecontact.html',{"error":"contact number cannot be empty!"})
        elif request.POST["email"] and record.email!=request.POST["email"]:
            existing_email=Contact_Book.objects.filter(email=request.POST["email"])
            if existing_email.count()==1:
                return render(request,'contact_details_app/updatecontact.html',{"error":"email already exists!","record":record})
        record.name=request.POST["typed_name"]
        record.email=request.POST['email']
        record.contact_number=request.POST['contact']
        record.save()
        return render(request,'contact_details_app/list_of_contacts.html',{"success":"contact updated successfully!"})

def searchfilter(request):
    if request.method=="POST":
        if request.POST['search_name']:
            Contacts=Contact_Book.objects.filter(name__icontains=request.POST['search_name'])
            if Contacts.count()==0:
                return render(request,'contact_details_app/list_of_contacts.html',{'error':"Contact does not exist with the name "+"\""+request.POST['search_name']+"\""})
            return render(request,'contact_details_app/list_of_contacts.html',{'filter_contacts':Contacts})
        elif request.POST['search_email']:
            Contacts=Contact_Book.objects.filter(email__icontains=request.POST['search_email'])
            if Contacts.count()==0:
                return render(request,'contact_details_app/list_of_contacts.html',{'error':"Contact does not exist with an email "+"\""+request.POST['search_email']+"\""})
            return render(request,'contact_details_app/list_of_contacts.html',{'filter_contacts':Contacts})

@api_view(['GET', 'POST'])
def contacts(request):
    if request.method == 'GET':
        Contacts = Contact_Book.objects.all()
        contact_serializer = ContactBookSerializer(Contacts, many=True)
        return JsonResponse(contact_serializer.data, safe=False)
    elif request.method == 'POST':
        Contact = JSONParser().parse(request)
        contact_serializer = ContactBookSerializer(data=Contact)
        if contact_serializer.is_valid():
            existing_contact=Contact_Book.objects.filter(email=Contact["email"])
            print(existing_contact)
            if existing_contact.count()==0:
                contact_serializer.save()
                return JsonResponse(contact_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({'message': 'entered email address already exists.'}, status=status.HTTP_208_ALREADY_REPORTED)
        return JsonResponse(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def contact(request,pk):
    try:
        Contact = Contact_Book.objects.get(pk=pk)
    except Contact_Book.DoesNotExist:
        return JsonResponse({'message': 'The contact does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        contact_serializer = ContactBookSerializer(Contact)
        return JsonResponse(contact_serializer.data)
    elif request.method == 'PUT':
        Contact_updated = JSONParser().parse(request)
        contact_serializer = ContactBookSerializer(Contact, data=Contact_updated)
        if contact_serializer.is_valid():
            contact_serializer.save()
            return JsonResponse(contact_serializer.data)
        return JsonResponse(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        Contact.delete()
        return JsonResponse({'message': 'contact was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
