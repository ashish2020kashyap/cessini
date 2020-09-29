import csv, io
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from .forms import CampaignForm,CreateUserForm,CustomerForm,EmailForm,EmailUpdateForm,CampUpdateForm
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate,login,logout
from .models import Profile,Invalidmail
from django.core.mail import send_mail,EmailMultiAlternatives,send_mass_mail
from django.core.mail import BadHeaderError,send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core import mail
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.contrib.auth.decorators import login_required
import re
from django.core.files.storage import default_storage
from django.core.mail import send_mail
import pandas as pd
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, CustomerSerializer,EmailSerializer,CampaignSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
# # Create your views here.


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]



class EmailViewSet(viewsets.ModelViewSet):

    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [permissions.IsAuthenticated]



class CampaignViewSet(viewsets.ModelViewSet):

    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]


















def basic(request):
    return render(request,'basic.html')

def index(request):
    template = "index.html"
    data = Profile.objects.all()
    invalid=Invalidmail.objects.all()
    if request.method == "GET":

        return render(request, template)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):

        messages.error(request,"This is not csv file,Please try again ")
        return redirect('/index')
      

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
  

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

        regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if(re.search(regex,column[0])):
            _, created = Profile.objects.update_or_create(email=column[0])
            
        else:
            _, created = Invalidmail.objects.update_or_create(email=column[0])
                
    context = {}
    messages.success(request,'Your Record Has Been Uploaded and Updated')
    return render(request,'index.html',context)
     
def about(request):

    return render(request,'about.html')


def emailslist(request):
    data = Invalidmail.objects.all()
    prompt = {'profiles': data }
    
   

   
    return render(request,'emails.html',prompt)


def sendmail(request):
    template="contact.html"

    if request.method=="POST" and  request.FILES['file'] and request.FILES['csv_files']:
        
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email=settings.EMAIL_HOST_USER
        csv = request.FILES['csv_files']
        csv_file_name = default_storage.save(csv.name, csv)

        csv_file = default_storage.open(csv_file_name)
        csv_file_url = default_storage.url(csv_file_name)
        print(csv_file_url)
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        connection = mail.get_connection()
        connection.open()

        df_file = pd.read_csv(csv_file)
        #print(df_file)

        df = pd.DataFrame(df_file)

        list = df['Email'].tolist()
        

        email= mail.EmailMessage(subject, message, from_email,bcc=list,connection=connection)

        file = default_storage.open(file_name)
        file_url = default_storage.url(file_name)
        email.attach(file_url, file.read())
        connection.send_messages([email])



        messages.success(request,"Email sent Successfully")
  
        connection.close()

    return render(request,'contact.html')



def valid(request):
    
    data = Profile.objects.all()
    prompt = {'profiles': data }
   
    return render(request,'validate.html',prompt)


def mailing(request):
    fields = ['Email']
    #df_file= pd.read_csv("/Users/ashishkumar/Desktop/email.csv",skipinitialspace=True, usecols=fields)
    df_file = pd.read_csv("/Users/ashishkumar/Desktop/email.csv")
    df=pd.DataFrame(df_file)

    list = df['Email'].tolist()

    context={'df':df_file.to_html,

             'list':list,

             }
    return render(request, 'mailing.html',context)


def dashboard(request,pk_test):
    customer = Customer.objects.all()
    campaign = Campaign.objects.all()
    email = Email.objects.all()
    customerss = Customer.objects.get(id=pk_test)


    context = {'campaign': campaign, 'email': email,'customer':customer,'customerss':customerss}

    return render(request, 'dashboard.html', context)



def profile(request,pk_test):
    users=User.objects.all()
    customer = Customer.objects.all()
    campaign = Campaign.objects.filter(my_customer=pk_test)
    current_user = request.user.id
    email = Email.objects.filter(my_customer=pk_test)



    context = {'campaign': campaign, 'email': email,'customer':customer,'current_user':current_user,'users':users}

    return render(request, 'profile.html', context)




def customer(request):
    customer = Customer.objects.all()
    campaign = Campaign.objects.all()
    email = Email.objects.all()
    current_user = request.user



    context = {'campaign': campaign, 'email': email,'customer':customer,'current_user':current_user}

    return render(request, 'customerhome.html', context)




def campaign(request):

    current_user = request.user.id
    print(current_user)
    customer = Customer.objects.get(id=current_user)

    emails = Email.objects.filter(my_customer=current_user)
    file_names=""

    if request.method == 'POST':
        name = request.POST.get('name', '')
        sender_name = request.POST.get('sender_name', '')
        sender_email = request.POST.get('sender_email', '')
        email_subject = request.POST.get('email_subject', '')
        mails = request.POST.get('mail')
        mailings = Email.objects.get(id=mails)
        for f in Email.objects.filter(id=mails):
            file_names=f.upload_file
        contact= Campaign(my_customer=customer,name=name,sender_name=sender_name,sender_email=sender_email,email_subject=email_subject,camp_emails=mailings)
        contact.save()
        form = CampaignForm(request.POST)
        print(request.POST)

        if form.is_valid():
            form.save()
            print("working")
            return redirect('/customer')


        print("working")
        return redirect('/customer')


    else:
        fm = CampaignForm()
        print("form is not valid")

        context = {'form':fm,'emails':emails}
        return render(request, 'addcampaign.html', context)






def email(request):
    form = EmailForm()
    current_user = request.user.id
    print(current_user)
    customer = Customer.objects.get(id=current_user)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        upload_file = request.FILES['upload_file']

        contact= Email(my_customer=customer,name=name,upload_file=upload_file)
        contact.save()
        return redirect('/customer')


    context = {'form':form}

    return render(request, 'addemail.html', context)





def handleSign(request):
    form = CreateUserForm()
    if request.method == 'POST':
        job = request.POST['job']
        print(job)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            if job=="Customer":
                group = Group.objects.get(name='Customer')
                user.groups.add(group)
                Customer.objects.create(
                    user=user,
                    name=user.username,
                )

            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/')
        else:
            print("wrong credentials")
    context = {'form': form}
    return render(request, 'signup.html', context)





def handleLog(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'Customer':

                return redirect('Customer')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def updatecamp(request):
    current_user = request.user
    form = CampUpdateForm()
    pi = Customer.objects.get(pk=current_user.id)
    fm = CampUpdateForm(instance=pi)
    print(fm)

    if request.method == 'POST':

        print(request.POST)
        fm = CampUpdateForm(request.POST,instance=pi)
        fm.save()

        print("working")
        return redirect('/customer')

    else:
        fm = CampUpdateForm(instance=pi)
        return render(request, 'updatecamp.html', {'form':fm})


    context = {'current_user ':current_user ,'fm':fm,'form':form}
    return render(request, 'updatecamp.html', context)



def updateemail(request):
    #form=CustomerForm()
    current_user = request.user

    pi = Customer.objects.get(pk=current_user.id)
    fm = EmailUpdateForm(instance=pi)

    if request.method == 'POST':

        print(request.POST)
        fm = EmailUpdateForm(request.POST,instance=pi)
        fm.save()

        #contact= Customer(user=current_user)
        #contact.save()

        print("working")
        return redirect('/customer')

    context = {'current_user ':current_user ,'form':fm}
    return render(request, 'updateemail.html', context)



def sending(request,pk_test):
    users = User.objects.all()
    customer = Customer.objects.all()
    campaign = Campaign.objects.all()
    email = Email.objects.all()
    campaigns = Campaign.objects.filter(my_customer=pk_test)
    emails = Email.objects.filter(my_customer=pk_test)



    current_user = request.user
    pi = Customer.objects.get(pk=current_user.id)

    if request.method == "POST" and  request.FILES['file']:

        job = request.POST.get('job')
        mails = request.POST.get('mail')
        message= request.POST.get('message')
        subject=""
        file_names=""

        for e in Campaign.objects.filter(id=job):
            subject=e.email_subject

        for f in Email.objects.filter(id=mails):
            file_names=f.upload_file


        from_email = settings.EMAIL_HOST_USER
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        df_file = pd.read_csv(file_names)
        #print(df_file)
        connection = mail.get_connection()
        connection.open()


        df = pd.DataFrame(df_file)

        list = df['Email'].tolist()

        email = mail.EmailMessage(subject, message, from_email, bcc=list, connection=connection)

        file = default_storage.open(file_name)
        file_url = default_storage.url(file_name)
        email.attach(file_url, file.read())
        connection.send_messages([email])

        messages.success(request, "Email sent Successfully")

        connection.close()


    context = {'campaign': campaign, 'email': email,'customer':customer,'current_user':current_user,'campaigns': campaigns, 'emails': emails,}
    return render(request, 'sending.html', context)



def manytomany(request,pk_test):
    campmail = CampMail.objects.all()

    current_user = request.user.id
    print(current_user)
    customer = Customer.objects.get(id=current_user)
    form= CampaignForm()


    if request.method == 'GET':
        name = request.GET.get('name', '')
        sender_name = request.GET.get('sender_name', '')
        sender_email = request.GET.get('sender_email', '')
        email_subject = request.GET.get('email_subject', '')
        check = request.GET.get('check', '')
        contact= Campaign(my_customer=customer,name=name,sender_name=sender_name,sender_email=sender_email,email_subject=email_subject)
        #contact.save()
        print(contact)
        print(check)
        form = CampaignForm(request.GET)
        print(request.GET)

        if form.is_valid():
            #form.save()
            print("working")

        print("working")

    else:
        fm = CampaignForm()
        print("form is not valid")

        context = {'form':fm}
        return render(request, 'manytomany.html', context)

    context={'form':form,'campmail':campmail}

    return render(request, 'manytomany.html',context)


import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import CampaignForm, CreateUserForm, CustomerForm, EmailForm, EmailUpdateForm, CampUpdateForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Invalidmail
from django.core.mail import send_mail, EmailMultiAlternatives, send_mass_mail
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core import mail
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.contrib.auth.decorators import login_required
import re
from django.core.files.storage import default_storage
from django.core.mail import send_mail
import pandas as pd


# # Create your views here.
def basic(request):
    return render(request, 'basic.html')


def index(request):
    template = "index.html"
    data = Profile.objects.all()
    invalid = Invalidmail.objects.all()
    if request.method == "GET":
        return render(request, template)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This is not csv file,Please try again ")
        return redirect('/index')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):

        regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if (re.search(regex, column[0])):
            _, created = Profile.objects.update_or_create(email=column[0])

        else:
            _, created = Invalidmail.objects.update_or_create(email=column[0])

    context = {}
    messages.success(request, 'Your Record Has Been Uploaded and Updated')
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def emailslist(request):
    data = Invalidmail.objects.all()
    prompt = {'profiles': data}

    return render(request, 'emails.html', prompt)


def sendmail(request):
    template = "contact.html"

    if request.method == "POST" and request.FILES['file'] and request.FILES['csv_files']:
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email = settings.EMAIL_HOST_USER
        csv = request.FILES['csv_files']
        csv_file_name = default_storage.save(csv.name, csv)

        csv_file = default_storage.open(csv_file_name)
        csv_file_url = default_storage.url(csv_file_name)
        print(csv_file_url)
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        connection = mail.get_connection()
        connection.open()

        df_file = pd.read_csv(csv_file)
        # print(df_file)

        df = pd.DataFrame(df_file)

        list = df['Email'].tolist()

        email = mail.EmailMessage(subject, message, from_email, bcc=list, connection=connection)

        file = default_storage.open(file_name)
        file_url = default_storage.url(file_name)
        email.attach(file_url, file.read())
        connection.send_messages([email])

        messages.success(request, "Email sent Successfully")

        connection.close()

    return render(request, 'contact.html')


def valid(request):
    data = Profile.objects.all()
    prompt = {'profiles': data}

    return render(request, 'validate.html', prompt)


def mailing(request):
    fields = ['Email']
    # df_file= pd.read_csv("/Users/ashishkumar/Desktop/email.csv",skipinitialspace=True, usecols=fields)
    df_file = pd.read_csv("/Users/ashishkumar/Desktop/email.csv")
    df = pd.DataFrame(df_file)

    list = df['Email'].tolist()

    context = {'df': df_file.to_html,

               'list': list,

               }
    return render(request, 'mailing.html', context)


def dashboard(request, pk_test):
    customer = Customer.objects.all()
    campaign = Campaign.objects.all()
    email = Email.objects.all()
    customerss = Customer.objects.get(id=pk_test)

    context = {'campaign': campaign, 'email': email, 'customer': customer, 'customerss': customerss}

    return render(request, 'dashboard.html', context)


def profile(request, pk_test):
    users = User.objects.all()
    customer = Customer.objects.all()
    campaign = Campaign.objects.filter(my_customer=pk_test)
    current_user = request.user.id
    email = Email.objects.filter(my_customer=pk_test)

    context = {'campaign': campaign, 'email': email, 'customer': customer, 'current_user': current_user, 'users': users}

    return render(request, 'profile.html', context)


def customer(request):
    customer = Customer.objects.all()
    campaign = Campaign.objects.all()
    email = Email.objects.all()
    current_user = request.user

    context = {'campaign': campaign, 'email': email, 'customer': customer, 'current_user': current_user}

    return render(request, 'customerhome.html', context)


def campaign(request):
    current_user = request.user.id
    print(current_user)
    customer = Customer.objects.get(id=current_user)

    emails = Email.objects.filter(my_customer=current_user)
    file_names = ""

    if request.method == 'POST':
        name = request.POST.get('name', '')
        sender_name = request.POST.get('sender_name', '')
        sender_email = request.POST.get('sender_email', '')
        email_subject = request.POST.get('email_subject', '')
        mails = request.POST.get('mail')
        mailings = Email.objects.get(id=mails)
        for f in Email.objects.filter(id=mails):
            file_names = f.upload_file
        contact = Campaign(my_customer=customer, name=name, sender_name=sender_name, sender_email=sender_email,
                           email_subject=email_subject, camp_emails=mailings)
        contact.save()
        form = CampaignForm(request.POST)
        print(request.POST)

        if form.is_valid():
            form.save()
            print("working")
            #return redirect('/customer')

            return redirect('/sendmail')

        print("working")
        #return redirect('/customer')
        return redirect('/sendmail')


    else:
        fm = CampaignForm()
        print("form is not valid")

        context = {'form': fm, 'emails': emails}
        return render(request, 'addcampaign.html', context)


def email(request):
    form = EmailForm()
    current_user = request.user.id
    print(current_user)
    customer = Customer.objects.get(id=current_user)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        upload_file = request.FILES['upload_file']

        contact = Email(my_customer=customer, name=name, upload_file=upload_file)
        contact.save()
        return redirect('/customer')

    context = {'form': form}

    return render(request, 'addemail.html', context)


def handleSign(request):
    form = CreateUserForm()
    if request.method == 'POST':
        job = request.POST['job']
        print(job)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if job == "Customer":
                group = Group.objects.get(name='Customer')
                user.groups.add(group)
                Customer.objects.create(
                    user=user,
                    name=user.username,
                )

            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/')
        else:
            print("wrong credentials")
    context = {'form': form}
    return render(request, 'signup.html', context)


def handleLog(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'Customer':
                return redirect('Customer')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def updatecamp(request):
    current_user = request.user
    form = CampUpdateForm()
    pi = Customer.objects.get(pk=current_user.id)
    fm = CampUpdateForm(instance=pi)
    print(fm)

    if request.method == 'POST':

        print(request.POST)
        fm = CampUpdateForm(request.POST, instance=pi)
        fm.save()

        print("working")
        return redirect('/customer')

    else:
        fm = CampUpdateForm(instance=pi)
        return render(request, 'updatecamp.html', {'form': fm})

    context = {'current_user ': current_user, 'fm': fm, 'form': form}
    return render(request, 'updatecamp.html', context)


def updateemail(request):
    # form=CustomerForm()
    current_user = request.user

    pi = Customer.objects.get(pk=current_user.id)
    fm = EmailUpdateForm(instance=pi)

    if request.method == 'POST':
        print(request.POST)
        fm = EmailUpdateForm(request.POST, instance=pi)
        fm.save()

        # contact= Customer(user=current_user)
        # contact.save()

        print("working")
        return redirect('/customer')

    context = {'current_user ': current_user, 'form': fm}
    return render(request, 'updateemail.html', context)


def sendmail(request):
    current_user = request.user
    users = User.objects.all()
    customer = Customer.objects.all()
    campaign = Campaign.objects.all()
    email = Email.objects.all()
    campaigns = Campaign.objects.filter(my_customer=current_user.id)
    campmaildata = Campaign.objects.filter(camp_emails=current_user.id)
    emails = Email.objects.filter(my_customer=current_user.id)
    print(campmaildata)

    pi = Customer.objects.get(pk=current_user.id)

    if request.method == "POST" and request.FILES['file']:

        job = request.POST.get('job')
        message = request.POST.get('message')
        subject = ""
        file_names = ""
        getid = ""

        for e in Campaign.objects.filter(id=job):
            subject = e.email_subject
            getid=e.camp_emails.id

        print(getid)

        for f in Email.objects.filter(id=getid):
            file_names=f.upload_file


        from_email = settings.EMAIL_HOST_USER
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        df_file = pd.read_csv(file_names)
        # print(df_file)
        connection = mail.get_connection()
        connection.open()

        df = pd.DataFrame(df_file)

        list = df['Email'].tolist()

        email = mail.EmailMessage(subject, message, from_email, bcc=list, connection=connection)

        file = default_storage.open(file_name)
        file_url = default_storage.url(file_name)
        email.attach(file_url, file.read())
        connection.send_messages([email])

        messages.success(request, "Email sent Successfully")


        connection.close()
        return redirect('/customer')


    context = {'campaign': campaign, 'email': email, 'customer': customer, 'current_user': current_user,
               'campaigns': campaigns, 'emails': emails, }
    return render(request, 'sendmail.html', context)


