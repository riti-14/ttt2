from email import message
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import empleave_model
from django.contrib import messages
from .forms import empleave_form
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib.auth import login,authenticate
# from django.http import JsonResponse
from .models import myuser_model


# Create your views here.
def empregister_view(request):
    if request.method=='POST':
        name=request.POST['nm']
        email=request.POST['em']
        user_name=request.POST['unm']
        password=request.POST['pswd']
        confirm_password=request.POST['pswd2']

        #validation..

        if name and email and user_name and password and confirm_password == ' ':
            return HttpResponse ('all fields required..')
            
        if len(name)>10:
            messages.error(request,'username must be under 10 character')
            return redirect('empregister')

        if not name.isalpha():
            messages.error(request,'username should only contain 10 characters')
            return redirect('empregister')

        if password!=confirm_password:
            messages.error(request,'Confirm Password do not match with Password')
            return redirect('empregister')

        create_user=myuser_model.objects.create_user(user_name,email,password)
        create_user.first_name=name
        create_user.save()
        messages.success(request,'user registered successfully..')
        return redirect('emplogin')

    else:
        return render(request,'emp_register.html')


def emplogin_view(request):
    if request.method=='POST':
        username=request.POST['unm']
        password=request.POST['pswd']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser :    
                return redirect('displayadmin')
            else:
                return redirect('displayuser',request.user.id)  
                
    else:
        return render(request,'emp_login.html')


def displayuser_view(request,id):

        # import pdb; pdb.set_trace()
        getdata=myuser_model.objects.get(id=request.user.pk) 
        getstatus=myuser_model.objects.filter(username=request.user).values('status')[0]['status']
        print(getstatus)
        context={'getdata':getdata,'getstatus':getstatus}
        return render(request,'display_user.html',context)
    
        


def displayadmin_view(request):
    getuserdata =myuser_model.objects.all()
    getleavedata=empleave_model.objects.all()
    user_count = myuser_model.objects.filter(is_superuser=False).count()
    return render(request,'display_admin.html',{'getuserdata':getuserdata,'getleavedata':getleavedata,'user_count':user_count})
    # 


def approve_view(request,username,pk):
    try:
        user=myuser_model.objects.get(username=username)
    except:
        print('error')

    if request.method == 'POST':
        emp=myuser_model.objects.filter(username=username)[0]
        user.status = 'APPROVE'
        user.save()
        print(user)
        
        var=list(empleave_model.objects.filter(id=pk).values('email'))
        subject='LEAVE'
        msg="approved"
        to=var[0]['email']
        send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
        if send_mail:
            msg='sent mail successfully'
        else:
            msg='mail could not sent'
        
        return HttpResponse(msg)

         
    else:
        print('errror')



            
def home_view(request):
    return render(request,'home.html') 



def reject_view(request,username,pk):
    try:
        
        user=myuser_model.objects.get(username=username)
    except:
        print('error')

    if request.method == 'POST':
        emp=myuser_model.objects.filter(username=username)[0]
        user.status = 'REJECT'
        user.save()
        
        var=list(empleave_model.objects.filter(id=pk).values('email'))
        subject='LEAVE'
        msg="rejected"
        to=var[0]['email']
        send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
        
        if send_mail:
            msg='sent mail successfully'
        else:
            msg='mail could not sent'
        
        return HttpResponse(msg)
        # return JsonResponse(var,safe=False)
    else:
            return HttpResponse('error')   

     

def empleave_view(request):
    form=empleave_form
    if request.method=='POST':
        form=empleave_form(request.POST)
        if form.is_valid():
            name=request.POST['name']   
            form.save() 

            from_email=request.POST['email']
            print(from_email)

            
            subject='Applied For Leave'
            message=f"I'm {name}, applied for leave. can i take leave?"
            to='riitmehtaa@gmail.com'

            email=EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=[to],
                reply_to=[from_email]

            )
            
            email.send()
            # data = {
            #     'subject':subject,
            #     'message':message,
            #     'from_email':from_email,
            #     'to':to,
            
            # }
            
            # send_mail(data=data)
            # print(form['email'])
            # if send_mail:
            #     msg='sent mail successfully'
            # else:
            #     msg='mail could not sent'
            return HttpResponse('Applied for leave')
        else:
            print('error')     
    return render(request,'apply_empleave.html',{'f':form})
    
    

