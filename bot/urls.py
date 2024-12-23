from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from .views import PersonalRecord,UserRecord,EmployeeRecord,LoginUser,LogoutUser,EmployeeLeaveStatusFilter,RegisterUser,LeaveApproval,EmployeeBankDetail
# from rest_framework.routers import DefaultRouter

# routers=DefaultRouter()
# routers.register(r'tasks',views.TaskViewset)


urlpatterns=[

    path("",EmployeeRecord.as_view(),name='home'),
    path("personal_leave/<int:pk>",LeaveApproval.as_view(),name='personal_leave'),
    path("filter/<str:status>",EmployeeLeaveStatusFilter.as_view(),name='Status_filter'),
    path("login/",LoginUser.as_view(),name='login'),
    path('logout/',LogoutUser.as_view(),name='logout'),
    path('register/',RegisterUser.as_view(),name='register_admin'),
    path('employee_record/<int:pk>',PersonalRecord.as_view(),name='employee_record'),
    path('user_record/<int:pk>',UserRecord.as_view(),name='user_record'),
    path('employee_bank_details/<int:pk>',EmployeeBankDetail.as_view(),name='bank_detail')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)