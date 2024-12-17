from django.urls import path,re_path
from .views import AllRecord,Leave,Filter,loginuser,logoutuser,Registeruser,PersonalRecord,UserRecord
# from rest_framework.routers import DefaultRouter

# routers=DefaultRouter()
# routers.register(r'tasks',views.TaskViewset)


urlpatterns=[

    path("",AllRecord.as_view(),name='home'),
    path("personal_leave/<int:pk>",Leave.as_view(),name='personal_leave'),
    path("filter/<str:status>",Filter.as_view(),name='Status_filter'),
    path("login/",loginuser.as_view(),name='login'),
    path('logout/',logoutuser.as_view(),name='logout'),
    path('register/',Registeruser.as_view(),name='register_admin'),
    path('employee_record/<int:pk>',PersonalRecord.as_view(),name='employee_record'),
    path('user_record/<int:pk>',UserRecord.as_view(),name='user_record')
]