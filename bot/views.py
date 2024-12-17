from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from rest_framework import viewsets,permissions
from rest_framework.views import APIView,View
from django.views.generic import UpdateView
from .models import LeaveRequest,TaskRecord,BreakRecord,CheckinRecord,Employee
from .serializers import LeaveSerializer,TaskSerializer,BreakSerializer,CheckinSerializer,EmployeeSerializer,UserSerializer
from rest_framework.response import Response
from .forms import Leaveapprovalform,RegistrationForm,EmployeeInfoForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

# Create your views here.
class loginuser(View):
    def get(self,request):
        return render(request,'home.html')
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
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
              
class logoutuser(View):
    def get(self,request):
        logout(request)

        return redirect('login')
        


class AllRecord(View):
    def get(self,request):
            if request.user.is_superuser :
                leave_obj=LeaveRequest.objects.all().order_by('start_date')
                serializer=LeaveSerializer(leave_obj,many=True)
                # return Response(serializer.data)
                return render(request,'home.html',{'Leavedata':serializer.data})
            if not request.user.is_superuser and request.user.is_authenticated:
                return redirect(f"employee_record/{request.user.id}")
            
            return render(request,'private_content.html')

    

class Leave(View):
    def get(self,request,pk):
        
        Leave_obj=get_object_or_404(LeaveRequest,id=pk)
        form=Leaveapprovalform(instance=Leave_obj)       
        return render(request,'Leaveapproval.html',{'form':form})
    

    def post(self,request,pk):
        Leave_obj=get_object_or_404(LeaveRequest,id=pk)
        form=Leaveapprovalform(request.POST,instance=Leave_obj)
        if form.is_valid():
                try:
                    form.save()
                    return redirect('home')
                except Exception as e:
                    return HttpResponse (e)
        else:
                return HttpResponse("Not Valid")
        




class Filter(View):
    def get(self,request,status):
        Leave_obj=LeaveRequest.objects.filter(status=status)
        serilaizer=LeaveSerializer(Leave_obj,many=True)
        return render(request,'home.html',{'Leavedata':serilaizer.data})


class Registeruser(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            name=request.GET.get('discord_username')
            id=int(request.GET.get('discord_user_id',000000000))
            form=RegistrationForm()
            if name and id:
                 form.fields['username'].initial=name
                 form.fields['discord_user_id'].initial=id
            return render(request,'register.html',{'form':form})
    def post(self,request):
        form=RegistrationForm(request.POST)

        # print({form.data}, {form2.data})
        try:
            if form.is_valid():
                print("form valid")
                userDb: User = form.save()
                print(userDb)
                Employee.objects.create(
                    User= userDb,
                    discord_user_id=request.POST['discord_user_id'],
                    post=request.POST['post'],
                    phone_number=request.POST['phone_number']
                )
               
                return redirect('home')
            
            else:
                return HttpResponse(form.errors)
                
        
        except Exception as e:
                return HttpResponse(e)

class PersonalRecord(View):
    def get(self,request,pk):
        try:
            Leave_obj=get_object_or_404(Employee,User_id=pk)

            serializer=EmployeeSerializer(Leave_obj)
            return render(request,'personal_record.html',{'data':serializer.data})
        except Exception as e:
            messages.success(request,'User not found')
            return redirect('logout')
        

class UserRecord(APIView):
    def get(self,request,pk):
        try:
            User_object=get_object_or_404(User,id=pk)
            serializer=UserSerializer(User_object)
            return Response(serializer.data)
        except Exception as e:
            messages.success(request,'Error in retreiving record')
            return redirect('employee_record')
        