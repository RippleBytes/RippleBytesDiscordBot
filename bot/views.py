from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from rest_framework import viewsets,permissions
from rest_framework.views import APIView,View
from .models import LeaveRequest,TaskRecord,BreakRecord,CheckinRecord,Employee
from .serializers import LeaveSerializer,TaskSerializer,BreakSerializer,CheckinSerializer,EmployeeSerializer,UserSerializer
from rest_framework.response import Response
from .forms import LeaveApprovalForm,RegistrationForm,EmployeeInfoForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User 

# Create your views here.
class LoginUser(View):
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
        form=RegistrationForm(request.POST)

        # print({form.data}, {form2.data})
        try:
            if form.is_valid():
                print("form valid")
                userDB: User = form.save()
                print(userDB)
                Employee.objects.create(
                    User= userDB,
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
            leave_object=get_object_or_404(Employee,User_id=pk)

            serializer=EmployeeSerializer(leave_object)
            return render(request,'personal_record.html',{'data':serializer.data})
        except Exception as e:
            messages.success(request,'User not found')
            return redirect('logout')
        

class UserRecord(APIView):
    def get(self,request,pk):
        try:
            user_object=get_object_or_404(User,id=pk)
            serializer=UserSerializer(user_object)
            return Response(serializer.data)
        except Exception as e:
            messages.success(request,'Error in retreiving record')
            return redirect('employee_record')
        