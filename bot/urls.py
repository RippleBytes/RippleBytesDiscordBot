from django.urls import path,include
from .views import AllRecord,Leave,Filter,loginuser,logoutuser,Registeradmin
# from rest_framework.routers import DefaultRouter

# routers=DefaultRouter()
# routers.register(r'tasks',views.TaskViewset)


urlpatterns=[

    path("",AllRecord.as_view(),name='leave'),
    path("personal_leave/<int:pk>",Leave.as_view(),name='personal_leave'),
    path("filter/<str:status>",Filter.as_view(),name='Status_filter'),
    path("login/",loginuser.as_view(),name='login'),
    path('logout/',logoutuser.as_view(),name='logout'),
    path('register/',Registeradmin.as_view(),name='register_admin')
]