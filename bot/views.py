from django.shortcuts import render,redirect,HttpResponse
from rest_framework import viewsets,permissions
from rest_framework.views import APIView,View
from django.views.generic import UpdateView
from .models import LeaveRequest,TaskRecord,BreakRecord,CheckinRecord
from .serializers import LeaveSerializer,TaskSerializer,BreakSerializer,CheckinSerializer
from rest_framework.response import Response
from .forms import Leaveapprovalform,RegistrationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate

# Create your views here.
class loginuser(View):
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
                return redirect('leave')
        except Exception as e:
            print(e)
            return HttpResponse(e)
        
class logoutuser(View):
    def get(self,request):
        logout(request)
        messages.success(request,'You have been logged out!!')
        return redirect('leave')
        

class AllRecord(APIView):
    def get(self,request):
        
        leave_obj=LeaveRequest.objects.all()
        serializer=LeaveSerializer(leave_obj,many=True)
        

        # return Response(serializer.data)
        return render(request,'home.html',{'Leavedata':serializer.data})
    

class Leave(APIView):
    def get(self,request,pk):
        Leave_obj=LeaveRequest.objects.get(id=pk)
        form=Leaveapprovalform(instance=Leave_obj)       
        
        return render(request,'Leaveapproval.html',{'form':form})
    

    def post(self,request,pk):
        Leave_obj=LeaveRequest.objects.get(id=pk)
        form=Leaveapprovalform(request.POST,instance=Leave_obj)
        if request.method=='POST':
            if form.is_valid():
                try:
                    form.save()
                    return redirect('leave')
                except Exception as e:
                    return HttpResponse (e)
                
                
            else:
                return HttpResponse("Not Valid")
        return render(request,'Leaveapproval.html',{'form':form})




class Filter(APIView):
    def get(self,request,status):
        leave_obj=LeaveRequest.objects.filter(status=status)
        serilaizer=LeaveSerializer(leave_obj,many=True)
        return render(request,'home.html',{'Leavedata':serilaizer.data})


class Registeradmin(View):
    def get(self,request):
        if request.user.is_authenticated:
            pass
        else:

            form=RegistrationForm()
            return render(request,'register.html',{'form':form})
    def post(self,request):
        form=RegistrationForm()
        # if form.is_valid():
        #     form.save()
        #     username=form.cleaned_data['username']
        #     password=form.cleaned_data['password']

        return render(request,'register.html',{'form':form})