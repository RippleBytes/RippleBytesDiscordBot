from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import PersonalWorkRecord,EmployeeRecord,LoginUser,LogoutUser \
,EmployeeLeaveStatusFilter,LeaveApproval,EmployeeBankDetail,PersonalProfileView\
,LeaveRecord,AllTaskRecord,AllCheckinRecord,EditPersonalInfo,RegisterUser
# from rest_framework.routers import DefaultRouter

# routers=DefaultRouter()
# routers.register(r'tasks',views.TaskViewset)


urlpatterns=[

    path("",EmployeeRecord.as_view(),name='admin_home'),
    path("personal_leave/<int:pk>",LeaveApproval.as_view(),name='personal_leave'),
    path("employee_leave/",LeaveRecord.as_view(),name='employee_leave'),
    path("filter/<str:status>",EmployeeLeaveStatusFilter.as_view(),name='status_filter'),
    path("login/",LoginUser.as_view(),name='login'),
    path('logout/',LogoutUser.as_view(),name='logout'),
    path('register/',RegisterUser.as_view(),name='register_user'),
    path('personal_profile/<int:pk>',PersonalProfileView.as_view(),name='personal_profile'),
    path('employee_record/<int:pk>',PersonalWorkRecord.as_view(),name='employee_record'),
    path('employee_bank_details/<int:pk>',EmployeeBankDetail.as_view(),name='bank_detail'),
    path('task_record/',AllTaskRecord.as_view(),name='task_record'),
    path('checkin_record/',AllCheckinRecord.as_view(),name='all_checkin_record'),
    path('register/<int:pk>',EditPersonalInfo.as_view(),name='edit_personal_info'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)