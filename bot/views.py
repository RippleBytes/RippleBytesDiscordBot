from django.shortcuts import render,redirect,HttpResponse
from rest_framework import viewsets,permissions
from rest_framework.views import APIView,View
from django.views.generic import UpdateView
from .models import LeaveRequest,TaskRecord,BreakRecord,CheckinRecord,Employee
from .serializers import LeaveSerializer,TaskSerializer,BreakSerializer,CheckinSerializer,EmployeeSerializer
from rest_framework.response import Response
from .forms import Leaveapprovalform,RegistrationForm,EmployeeInfoForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

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
                return redirect('leave')
            else:
                messages.success(request,"Invalid credentials")
                return redirect('login')
        except Exception as e:
            print(e)
            return HttpResponse(e)
        
class logoutuser(View):
    def get(self,request):
        logout(request)
        messages.success(request,'You have been logged out!!')
        return redirect('login')
        


class AllRecord(View):
    def get(self,request):
            if request.user.is_superuser :
                leave_obj=LeaveRequest.objects.all().order_by('start_date')
                serializer=LeaveSerializer(leave_obj,many=True)
                # return Response(serializer.data)
                return render(request,'home.html',{'Leavedata':serializer.data})
            if not request.user.is_superuser and request.user.is_authenticated:
                return redirect(f"personal_record/{request.user.id}")
            
            return render(request,'private_content.html')

    

class Leave(APIView):
    def get(self,request,pk):
        Leave_obj=LeaveRequest.objects.get(id=pk)
        form=Leaveapprovalform(instance=Leave_obj)       
        
        return render(request,'personal_record.html',{'form':form})
    

    def post(self,request,pk):
        Leave_obj=LeaveRequest.objects.get(id=pk)
        form=Leaveapprovalform(request.POST,instance=Leave_obj)
        
        if form.is_valid():
                try:
                    form.save()
                    return redirect('leave')
                except Exception as e:
                    return HttpResponse (e)
                
                
        else:
                return HttpResponse("Not Valid")
        




class Filter(APIView):
    def get(self,request,status):
        leave_obj=LeaveRequest.objects.filter(status=status)
        serilaizer=LeaveSerializer(leave_obj,many=True)
        return render(request,'home.html',{'Leavedata':serilaizer.data})


class Registeruser(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('leave')
        else:
            form=RegistrationForm()
            return render(request,'register.html',{'form':form})
    def post(self,request):
        print(123)
        form=RegistrationForm(request.POST)
        if form.is_valid():
                form.save()
                return redirect('employee_info')
        else:
                messages.success(request,'error in form')
                return redirect('register_admin')

    
class EmployeeInformation(View):
    def get(self,request):
        form=EmployeeInfoForm()
        return render(request,'GenericFormTemplate.html',{'form':form})
    def post(self,request):
        form=EmployeeInfoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,'Record added')
            return redirect('leave')
        
        return render(request,'GenericFormTemplate.html',{'form':form})


class PersonalRecord(APIView):
    def get(self,request,pk):
        try:
            object=Employee.objects.get(User_id=pk)
            serializer=EmployeeSerializer(object)
            return render(request,'personal_record.html',{'data':serializer.data})
        except Exception as e:
            messages.success(request,'User record not found') 
            return HttpResponse(e)