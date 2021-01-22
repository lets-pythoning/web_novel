from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from read_statistics.utils import get_week_read_data, \
								  get_today_hot_data, \
								  get_yesterday_hot_data, \
								  get_week_hot_data, \
								  get_month_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm

def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_week_read_data(blog_content_type)

	hot_blog_for_week = cache.get('hot_blog_for_week')
	if not hot_blog_for_week:
		hot_blog_for_week = get_week_hot_data()
		cache.set('hot_blog_for_week', hot_blog_for_week, 1800)

	context = {}
	context['dates'] = dates
	context['read_nums'] = read_nums
	context['today_hot_data'] = get_today_hot_data(blog_content_type)
	context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
	context['week_hot_data'] = hot_blog_for_week
	context['month_hot_data'] = get_month_hot_data()

	return render(request, 'home.html', context)

def login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request, user)

			return redirect(request.GET.get('from', reverse('home')))

	else:
		login_form = LoginForm()

	context = {}
	context['login_form'] = login_form

	return render(request, 'login.html', context)

def register(request):
	if request.method == 'POST':
		reg_form = RegForm(request.POST)
		if reg_form.is_valid():
			username = reg_form.cleaned_data['username']
			password = reg_form.cleaned_data['password']

			user = User.objects.create_user(username=username, password=password)
			user.save()

			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)

			return redirect(request.GET.get('from', reverse('home')))

	else:
		reg_form = RegForm()

	context = {}
	context['reg_form'] = reg_form

	return render(request, 'register.html', context)
