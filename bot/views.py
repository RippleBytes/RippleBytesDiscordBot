from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from rest_framework import viewsets,permissions
from rest_framework.views import APIView,View
from .models import LeaveRequest,TaskRecord,BreakRecord,CheckinRecord,Employee,BankDetails
from .serializers import LeaveSerializer,TaskSerializer,BreakSerializer,CheckinSerializer,EmployeeSerializer,UserSerializer
from rest_framework.response import Response
from .forms import LeaveApprovalForm,RegistrationForm,EmployeeBankDetailForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User 
from datetime import datetime
from .validators import validate_image,validate_pdf

def handle_uploaded_file(f):
    with open("documents/EmployeeCitizenship", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)




# Create your views here.
class LoginUser(View):
    def get(self,request):
        return render(request,'home.html')
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.success(request,"Invalid credentials")
                return redirect('login')
        except Exception as e:
            print(e)
            return HttpResponse(e)
              
class LogoutUser(View):
    def get(self,request):
        logout(request)
        return redirect('login')
        


class EmployeeRecord(View):
    def get(self,request):
            if request.user.is_superuser :
                leave_object=LeaveRequest.objects.all().order_by('start_date')
                serializer=LeaveSerializer(leave_object,many=True)
                # return Response(serializer.data)
                return render(request,'home.html',{'Leavedata':serializer.data})
            if not request.user.is_superuser and request.user.is_authenticated:
                print(request.user.id)
                return redirect(f"employee_record/{request.user.id}")
            
            return render(request,'private_content.html')

    

class LeaveApproval(View):
    def get(self,request,pk):
        
        leave_object=get_object_or_404(LeaveRequest,id=pk)
        form=LeaveApprovalForm(instance=leave_object)       
        return render(request,'Leaveapproval.html',{'form':form})
    

    def post(self,request,pk):
        leave_object=get_object_or_404(LeaveRequest,id=pk)
        form=LeaveApprovalForm(request.POST,instance=leave_object)
        if form.is_valid():
                try:
                    form.save()
                    return redirect('home')
                except Exception as e:
                    return HttpResponse (e)
        else:
                return HttpResponse("Not Valid")
        




class EmployeeLeaveStatusFilter(View):
    def get(self,request,status):
        leave_object=LeaveRequest.objects.filter(status=status)
        serilaizer=LeaveSerializer(leave_object,many=True)
        return render(request,'home.html',{'Leavedata':serilaizer.data,})


class RegisterUser(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            username=request.GET.get('discord_username')
            discord_id=int(request.GET.get('discord_user_id',0000000000))
            form=RegistrationForm()
            if username and discord_id:
                 form.fields['username'].initial=username
                 form.fields['discord_user_id'].initial=discord_id
            return render(request,'register.html',{'form':form})
    def post(self,request):
        form=RegistrationForm(request.POST,request.FILES)
        try:
            
            if form.is_valid():
                print("form valid")
                userDB= form.save()    
                Employee.objects.create(
                    user=userDB,
                    discord_user_id=request.POST.get('discord_user_id'),
                    job_title=request.POST.get('job_title'),
                    phone_number=request.POST.get('phone_number'),
                    date_of_birth=request.POST.get('date_of_birth'),
                    gender=request.POST.get('gender'),
                    employee_citizenship_number=request.POST.get('employee_citizenship_number'),
                    employee_citizenship_photo=request.FILES.get('employee_citizenship_photo'),
                    employee_resume_pdf=request.FILES.get('employee_resume_pdf'),
                    employee_pp_photo=request.FILES.get('employee_pp_photo')
                )
                return redirect('home')
            
            else:
                print(form.errors)
                return HttpResponse(form.errors.as_text)
                
        
        except Exception as e:
                print(e)
                return HttpResponse(e)

class PersonalRecord(View):
    def get(self,request,pk):
        try:
            employee_object=Employee.objects.get(user_id=pk)
            serializer=EmployeeSerializer(employee_object)
            return render(request,'personal_record.html',{'data':serializer.data})
        except Exception as e:
            print(e)
            return HttpResponse(e)
            messages.success(request,'User not found')
            return redirect('logout')
        

class UserRecord(View):
    def get(self,request,pk):
        try:
            user_object=get_object_or_404(User,id=pk)
            serializer=UserSerializer(user_object)
            return render(request,'user_info.html',{'data':serializer.data})
        except Exception as e:
            messages.success(request,'Error in retreiving record')
            return redirect('employee_record')
        
class EmployeeBankDetail(View):
    def get(self,request,pk):
        try:
            form=EmployeeBankDetailForm()
            user_object=Employee.objects.get(user_id=pk)
            form.fields['user'].disabled=True
            # form.fields['user']=user_object.ser_id
            return render(request,'bankdetailform.html',{'form':form})
        except Exception as e:
            return HttpResponse(e)

    def post(self,request,pk):
        try:
            user_object=Employee.objects.get(User_id=pk)
            form=EmployeeBankDetailForm(request.POST)

            form.fields['user']=request.user
            if form.is_valid():
                form.save()
                messages.success(request,'Bank details have been added!')
                return redirect('home')
            else:
                return HttpResponse(form.errors)
        except Exception as e:
            return HttpResponse(e)
            messages.success(request,'Unable to post data. Please try again')
            return redirect('user_record')