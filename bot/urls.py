from django.urls import path,include
from .views import AllRecord,Leave,Filter
from rest_framework.routers import DefaultRouter

# routers=DefaultRouter()
# routers.register(r'tasks',views.TaskViewset)


urlpatterns=[

    path("",AllRecord.as_view(),name='leave'),
    path("personal_leave/<int:pk>",Leave.as_view(),name='personal_leave'),
    path("filter/<str:status>",Filter.as_view(),name='Status_filter')
]