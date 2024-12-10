from django.shortcuts import render,redirect,HttpResponse
from rest_framework import viewsets,permissions
from rest_framework.views import APIView
from django.views.generic import UpdateView
from .models import LeaveRequest,TaskRecord,BreakRecord,CheckinRecord
from .serializers import LeaveSerializer,TaskSerializer,BreakSerializer,CheckinSerializer
from rest_framework.response import Response
from .forms import Leaveapprovalform
from django.contrib import messages

# Create your views here.

class AllRecord(APIView):
    def get(self,request):
        leave_obj=LeaveRequest.objects.all()
        serializer=LeaveSerializer(leave_obj,many=True)
        

        # return Response(serializer.data)
        return render(request,'home.html',{'user':serializer.data})



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
        return render(request,'home.html',{'user':serilaizer.data})
