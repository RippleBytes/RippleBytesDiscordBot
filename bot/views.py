from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,get_list_or_404
import csv,os
from rest_framework.renderers import JSONRenderer
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets,permissions
from rest_framework.views import APIView,View
from .models import LeaveRequest,TaskRecord,BreakRecord,CheckinRecord,BankDetail,User
from .serializers import LeaveSerializer,TaskSerializer,BreakSerializer,CheckinSerializer,UserSerializer,BankDetailSerializer
from rest_framework.response import Response
from .forms import LeaveApprovalForm,RegistrationForm,EmployeeBankDetailForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class LoginUser(View):
    
    permission_classes=[permissions.AllowAny]

    def get(self,request):
        #if users mannually type /login the url redirect it to authenticated page 
        if request.user.is_authenticated:
            messages.success(request,'You already have an active login')
            return redirect('admin_home')
        #render the page for the first time
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
            messages.success(request,e)
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
                user_object=User.objects.all().order_by('id')
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
                    return redirect('employee_leave')
                except Exception as e:
                    return HttpResponse (e)
        else:
                messages.success(request,form.errors)
                return redirect('employee_leave')

        
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
            username_field=form.fields['username']
            discord_user_id_field=form.fields['discord_user_id']
            username_field.widget=username_field.hidden_widget()
            discord_user_id_field.widget=discord_user_id_field.hidden_widget()

            if username and discord_id:
                username_field.initial=username
                discord_user_id_field.initial=discord_id
                username_field.label="'Username' sent through discord"
                discord_user_id_field.label=" 'Discord ID' sent through discord"
            else:
                username_field.label="Please user discord '/register command' "
                discord_user_id_field.label="Please user discord '/register command' "
            return render(request,'register.html',{'form':form})

    def post(self,request):
        form=RegistrationForm(request.POST,request.FILES)
        private_email=form['private_email'].value()
        print(private_email)
        try:
            if form.is_valid():
                form.save()
                return redirect('admin_home')
            else:
                print(form.error_messages)
                return render(request,'register.html',{'form':form})
        except Exception as e:
            messages.success(request,e)
            return render(request,'register.html',{'form':form})
                

class PersonalWorkRecord(View):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=(JWTAuthentication,)

    def get(self,request,pk):
            leave_serializer=None
            task_serializer=None
            employee_object=get_object_or_404(User,id=pk)
           
            try:
                leave_object=LeaveRequest.objects.filter(user=employee_object.id)
                
            except ObjectDoesNotExist:
                leave_object=None
        
            if leave_object:
                leave_serializer=LeaveSerializer(leave_object,many=True)
            
            task_object=TaskRecord.objects.filter(user=employee_object.id)
            task_serializer=TaskSerializer(task_object,many=True)
    
            if request.user ==employee_object:
                return render(request,'employee_record.html',{'json_data': leave_serializer.data if leave_serializer else None,
                'task_data': task_serializer.data if task_serializer else None,})
               
            else:
                messages.success(request,'Unauthorized access')
                return redirect('logout')

class PersonalProfileView(View):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=(JWTAuthentication,)
    def get(self,request,pk):
        try:
            user_object=get_object_or_404(User,id=pk)
            user_serializer=UserSerializer(user_object)
            return render(request,'personal_profile.html',{'user_data':user_serializer.data})
        except Exception as e:
            messages.success(request,'User not found')
            return redirect('admin_home')
        
        
class EmployeeBankDetail(View):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=(JWTAuthentication,)

    def get(self,request,pk):
        try:
            form=EmployeeBankDetailForm()
            bank_detail_object=BankDetail.objects.filter(user_id=pk).first()

            if not bank_detail_object:
                return render(request,'bank_detail_form.html',{'form':form}) 
            if request.user ==bank_detail_object.user:
                form=EmployeeBankDetailForm(instance=bank_detail_object)
                return render(request,'bank_detail_form.html',{'form':form})
            else:
                messages.success(request,'Unauthorized access')
                return redirect('admin_home')
        except Exception as e:
            return HttpResponse(e)

    def post(self,request,pk):
        try:
            bank_detail_object=BankDetail.objects.filter(user_id=pk).first()
            if not bank_detail_object:
                form=EmployeeBankDetailForm(request.POST,request.FILES)

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
        

class AllTaskRecord(View):
    permission_classes=[permissions.IsAdminUser]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        try:
            task_object=TaskRecord.objects.all().order_by('checkin_id')
            serializer=TaskSerializer(task_object,many=True)

            if not request.user.is_superuser :
                messages.success(request,'No access!!')
                return redirect('admin_home')
            return render(request,'task_record.html',{'task_data':serializer.data})
        except Exception as e:
            messages.success(request,e)
            return redirect('admin_home')
        

class AllCheckinRecord(View):
    permission_classes=[permissions.IsAdminUser]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        try:
            checkin_object=CheckinRecord.objects.all().order_by('checkin_time')
            serializer=CheckinSerializer(checkin_object,many=True)
            
            return render(request,'checkin.html',{'checkin_record':serializer.data})
        except Exception as e:
            messages.success(request,e)
            return redirect('admin_home')
        
class EditPersonalInfo(View):
    permission_classes=[permissions.IsAdminUser]
    authentication_classes=[JWTAuthentication]
    def get(self,request,pk):
        try:
            user_object=get_object_or_404(User,id=pk)
            if request.user==user_object:
               
                form=RegistrationForm(instance=user_object)

                
                #Hide from fields when editing
                username_field=form.fields['username']
                username_field.widget=username_field.hidden_widget()
                

                discord_UID_field=form.fields['discord_user_id']
                discord_UID_field.widget=discord_UID_field.hidden_widget()

                job_title_field=form.fields['job_title']
                job_title_field.widget=job_title_field.hidden_widget()

                employee_CN_field=form.fields['employee_citizenship_number']
                employee_CN_field.widget=employee_CN_field.hidden_widget()

                citizenship_photo=form.fields['employee_citizenship_photo']
                citizenship_photo.widget=citizenship_photo.hidden_widget()
                
                employee_resume_pdf=form.fields['employee_resume_pdf']
                employee_resume_pdf.widget=employee_resume_pdf.hidden_widget()
                
                employe_pp_photo=form.fields['employee_pp_photo']
                employe_pp_photo.widget=employe_pp_photo.hidden_widget()
                


                
                form.initial['phone_number']=user_object.phone_number
                form.initial['gender']=user_object.gender
                form.initial['date_of_birth']=user_object.date_of_birth

                return render(request,'register.html',{'form':form})
            else:
                return render('admin_home')
        except Exception as e:
            messages.success(request,e)
            return redirect('admin_home')
            
    def post(self,request,pk):
        try:
            user_object=get_object_or_404(User,id=pk)
            form=RegistrationForm(request.POST,request.FILES,instance=user_object)

            
           

            DUID=user_object.discord_user_id
            JT=user_object.job_title
            ECN=user_object.employee_citizenship_number
            ER=user_object.employee_resume_pdf
            ECP=user_object.employee_citizenship_photo
            EPP=user_object.employee_pp_photo
            
           
            username_field=form.fields['username']
            username_field.required=False
            username_field.disabled=True

            form.fields['discord_user_id'].required=False
            form.fields['job_title'].required=False
            form.fields['employee_citizenship_number'].required=False
            form.fields['employee_citizenship_photo'].required=False
            form.fields['employee_resume_pdf'].required=False
            form.fields['employee_pp_photo'].required=False


            
            if form.is_valid():
                with transaction.atomic():
                    
                    userDb=form.save(commit=False)
                    userDb.id= pk
                    
                    userDb.save()
                    userDb.first_name = request.POST.get('first_name', userDb.first_name)
                    userDb.last_name = request.POST.get('last_name', userDb.last_name)
            
                    user_object.discord_user_id=DUID
                    user_object.job_title=JT
                    user_object.phone_number=request.POST.get('phone_number')
                    user_object.date_of_birth=request.POST.get('date_of_birth')
                    user_object.gender=request.POST.get('gender')
                    user_object.employee_citizenship_number=ECN
                    user_object.employee_citizenship_photo=ECP
                    user_object.employee_resume_pdf=ER
                    user_object.employee_pp_photo=EPP
                    user_object.save()    
                    form.save()

                messages.success(request,'Profile updated')
                return redirect('admin_home')
            else:
                messages.success(request,form.errors)
                return redirect('admin_home')
        except Exception as e:
        
            messages.success(request,e)
            return redirect('admin_home')            

    

