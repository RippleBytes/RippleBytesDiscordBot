from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,get_list_or_404
from rest_framework import viewsets,permissions
from rest_framework.views import APIView,View
from .models import LeaveRequest,TaskRecord,BreakRecord,CheckinRecord,Employee,BankDetails
from .serializers import LeaveSerializer,TaskSerializer,BreakSerializer,CheckinSerializer,EmployeeSerializer,UserSerializer,BankDetailSerializer
from rest_framework.response import Response
from .forms import LeaveApprovalForm,RegistrationForm,EmployeeBankDetailForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User 
from .validators import validate_image,validate_pdf
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication



# Create your views here.
class LoginUser(View):
    permission_classes=[permissions.AllowAny]
    def get(self,request):
        return render(request,'admin_home.html')
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('admin_home')
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
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=(JWTAuthentication,)
    def get(self,request):
            if request.user.is_superuser :
                user_object=User.objects.all()
                serializer=UserSerializer(user_object,many=True)
                return render(request,'admin_home.html',{'data':serializer.data})

            if not request.user.is_superuser and request.user.is_authenticated:
                return redirect(f"employee_record/{request.user.id}")
            
            return render(request,'private_content.html')

    
class LeaveRecord(View):
        def get(self,request):
            leave_object=LeaveRequest.objects.all().order_by('start_date')
            serializer=LeaveSerializer(leave_object,many=True)
            return render(request,'leave_record.html',{'Leavedata':serializer.data})

class LeaveApproval(View):
    permission_classes=[permissions.IsAdminUser]
    authentication_classes=(JWTAuthentication,)
    def get(self,request,pk):
        
        leave_object=get_object_or_404(LeaveRequest,id=pk)
        form=LeaveApprovalForm(instance=leave_object)       
        return render(request,'leave_approval.html',{'form':form})
    

    def post(self,request,pk):
        leave_object=get_object_or_404(LeaveRequest,id=pk)
        form=LeaveApprovalForm(request.POST,instance=leave_object)
        if form.is_valid():
                try:
                    form.save()
                    return redirect('admin_home')
                except Exception as e:
                    return HttpResponse (e)
        else:
                return HttpResponse("Not Valid")
        
class EmployeeLeaveStatusFilter(View):
    permissions=[permissions.IsAdminUser]
    authentication_classes=(JWTAuthentication,)
    def get(self,request,status):
        leave_object=LeaveRequest.objects.filter(status=status)
        serilaizer=LeaveSerializer(leave_object,many=True)
        return render(request,'leave_record.html',{'Leavedata':serilaizer.data,})


class RegisterUser(View):
    permissions=[permissions.AllowAny]
    authentication_classes=(JWTAuthentication,)
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('admin_home')
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
                return redirect('admin_home')
            
            else:
                print(form.errors)
                return HttpResponse(form.errors.as_text)
                
        
        except Exception as e:
                print(e)
                return HttpResponse(e)

class PersonalWorkRecord(View):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=(JWTAuthentication,)
    def get(self,request,pk):
        try:
            employee_object=get_object_or_404(Employee,user=pk)
            if request.user ==employee_object.user:
                task_object=get_list_or_404(LeaveRequest,user_id=employee_object.discord_user_id)
                serializer=LeaveSerializer(task_object,many=True)
                # serializer=EmployeeSerializer(employee_object)
                return render(request,'employee_record.html',{'data':serializer.data})
            else:
                messages.success(request,'Unauthorized access')
                return redirect('admin_home')

        except Exception as e:
            return HttpResponse(e)



class PersonalProfileView(View):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=(JWTAuthentication,)
    def get(self,request,pk):
        try:
            
            employee_object=get_object_or_404(Employee,user=pk)
            user_object=get_object_or_404(User,id=pk)
            
            user_serializer=UserSerializer(user_object)
            employee_serializer=EmployeeSerializer(employee_object)
            return render(request,'personal_profile.html',{'employee_data':employee_serializer.data,'user_data':user_serializer})
            
        except Exception as e:
            # print(e)
            # return HttpResponse(e)
            messages.success(request,'User not found')
            return redirect('logout')
        
        
class EmployeeBankDetail(View):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=(JWTAuthentication,)

    def get(self,request,pk):
        
        try:
            bank_detail_object=get_object_or_404(BankDetails,user=pk)
            if request.user ==bank_detail_object.user:
                if bank_detail_object:
                    form=EmployeeBankDetailForm(instance=bank_detail_object)
                    return render(request,'bank_detail_form.html',{'form':form})
                else:
                    form=EmployeeBankDetailForm()
                    return render(request,'bank_detail_form.html',{'form':form})
            else:
                messages.success(request,'Unauthorized access')
                return redirect('admin_home')
        except Exception as e:
            return HttpResponse(e)

    def post(self,request,pk):
        try:
            bank_detail_object=get_object_or_404(BankDetails,user=pk)
            form=EmployeeBankDetailForm(request.POST,request.FILES,instance=bank_detail_object)
            if form.is_valid():
                bank=form.save(commit=False)
                bank.user=request.user
                bank.save()
                return redirect('admin_home')
            else:
                return HttpResponse(form.errors)
        except Exception as e:
            messages.success(request,'Unable to post data. Please try again')
            return redirect('user_record')
        
class MyTokenObtainPairView(TokenObtainPairView):
    @classmethod
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.user
        Refresh=RefreshToken.for_user(user)
        Access=AccessToken.for_user(user)
        data=serializer.data
        data['tokens']={"refresh":str(Refresh),"access":str(Access)}
        return Response(data)