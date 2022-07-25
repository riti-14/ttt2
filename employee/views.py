
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import empleave_model
# ,status_model
# from django.contrib.auth.models import User
from django.contrib import messages
from .forms import empleave_form
from django.core.mail import send_mail  
from django.conf import settings
from django.contrib.auth import login,authenticate
# from django.http import JsonResponse
from .models import myuser_model


# def empregister_view(request):
    
#     if request.method == 'POST':
#         myuserform=myuser_form(request.POST)
#         if myuserform.is_valid():
#             myuserform.save()
#             return redirect('home')
#     else:
#             myuserform=myuser_form()

#     # context={} 
#     return render(request,'emp_register.html',{'myuserform':myuserform})


# def home_view(request):
#     return render(request,'home.html') 














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
            # return redirect('empregister')

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
                # messages.success(request,'you have successfully logged in...')
                return redirect('displayuser',request.user.id)  
                # request.user.id
    else:
        return render(request,'emp_login.html')


def displayuser_view(request,id):

    
        getdata=myuser_model.objects.get(id=request.user.pk) 
        getstatus=myuser_model.objects.filter(id=id).values('status')
        context={'getdata':getdata,'getstatus':getstatus}
        
        return render(request,'display_user.html',context)
    
        


def displayadmin_view(request):
    getuserdata =myuser_model.objects.all()
    getleavedata=empleave_model.objects.all()
    # user_count = User.objects.count()
    return render(request,'display_admin.html',{'getuserdata':getuserdata,'getleavedata':getleavedata})
    # ,'user_count':user_count


def approve_view(request,id):
    # import pdb; pdb.set_trace()     
    user=myuser_model.objects.get(id=id)
    if request.method == 'POST':
        # import pdb; pdb.set_trace()    
        print('*****************************')
        request.user.status = True
        print('*****************************')       
        user.save()
        print('*****************************')
        print(user)
        return redirect('home')
        #
        # request.user_status==True
       
        # new_value=myuser_model(status=request.POST['approve_btn'])
        # new_value.save() 
        # print(new_value)
        # var=list(empleave_model.objects.filter(id=pk).values('email'))
        # subject='LEAVE'
        # msg="approved"
        # to=var[0]['email']
        # res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
        # if (res==1):
        #     msg='sent mail successfully'
        # else:
        #     msg='mail could not sent'
        # # return render(request,'display_user.html',{'new_value':new_value})
        # return HttpResponse(msg)

        # else:
        #     return HttpResponse('error')    
    else:
        print('errror')
            
            
def home_view(request):
    return render(request,'home.html') 


def reject_view(request,id):
    if request.method == 'POST':
        if request.POST['reject_btn'] == "Reject":
            
            
            new_value=myuser_model(status=request.POST['reject_btn'])  
            new_value.save()  
            var=list(empleave_model.objects.filter(id=id).values('email'))
            subject='LEAVE'
            msg="rejected"
            to=var[0]['email']
            res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
            new_value.save()
            if (res==1):
                msg='sent mail successfully'
            else:
                msg='mail could not sent'
            # return render(request,'display_user.html',{'new_value':new_value})
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
            subject='Applied For Leave'
            msg=f"I'm {name}, applied for leave. can i take leave?"
            to='mehtariti82@gmail.com'
            res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
            if (res==1):
                msg='sent mail successfully'
            else:
                msg='mail could not sent'
            return HttpResponse('Applied for leave')
        else:
            print('error')     
    return render(request,'apply_empleave.html',{'f':form})
    
    

