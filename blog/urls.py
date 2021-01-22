from django.urls import path
from . import views

urlpatterns = [
	path('', views.blog_list, name='blog_list'),
	path('detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
	path('type/<int:blog_type_id>', views.blogs_with_type, name='blogs_with_type'),
	path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
	path('create/', views.blog_create, name='blog_create'),
]
