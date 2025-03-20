from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_case, name='create_case'),
    # 其他 URL 配置...
]



