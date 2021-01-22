from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Blog, BlogType
from . import forms
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm

def get_blog_list_common_data(request, blogs_all_list):
	paginator = Paginator(blogs_all_list, 8)
	page_num = request.GET.get('page', 1)
	page_of_blogs = paginator.get_page(page_num)

	blog_dates = Blog.objects.dates('created_time', 'month', order='ASC')
	blog_dates_dict = {}
	for blog_date in blog_dates:
		blog_count = Blog.objects.filter(created_time__year=blog_date.year,
										 created_time__month=blog_date.month).count()
		blog_dates_dict[blog_date] = blog_count

	context = {}
	context['blogs'] = page_of_blogs.object_list
	context['page_of_blogs'] = page_of_blogs
	context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
	context['blog_dates'] = blog_dates_dict

	return context

def blog_list(request):
	blogs_all_list = Blog.objects.all()
	context = get_blog_list_common_data(request, blogs_all_list)

	return render(request, 'blog_list.html', context)

def blog_detail(request, blog_id):
	blog = get_object_or_404(Blog, id=blog_id)
	read_cookie_key = read_statistics_once_read(request, blog)
	blog_content_type = ContentType.objects.get_for_model(blog)
	comments = Comment.objects.filter(
			content_type=blog_content_type, object_id=blog.id, parent=None
		)

	data = {
		'content_type':blog_content_type.model,
		'object_id':blog_id,
		'reply_comment_id':0
	}

	context = {}
	context['previous_blog'] = Blog.objects.filter(
			created_time__lt=blog.created_time
		).first()
	context['next_blog'] = Blog.objects.filter(
			created_time__gt=blog.created_time
		).last()

	context['blog'] = blog
	context['user'] = request.user
	context['comments'] = comments
	context['comment_form'] = CommentForm(initial=data)

	response = render(request, 'blog_detail.html', context)
	response.set_cookie(read_cookie_key, 'true', max_age=1800)

	return response

def blogs_with_type(request, blog_type_id):
	blog_type = get_object_or_404(BlogType, id=blog_type_id)
	blogs_all_list = Blog.objects.filter(blog_type=blog_type)

	context = get_blog_list_common_data(request, blogs_all_list)
	context['blog_type'] = blog_type

	return render(request, 'blogs_with_type.html', context)

def blogs_with_date(request, year, month):
	blogs_all_list = Blog.objects.filter(
			created_time__year=year, created_time__month=month
		)

	context = get_blog_list_common_data(request, blogs_all_list)
	context['blogs_with_date'] = f'{year}年{month}月'

	return render(request, 'blogs_with_date.html', context)

def blog_create(request):
	if request.method == 'POST':
		create_form = forms.CreateBlogForm(request.POST)
		if create_form.is_valid():
			cl_data = create_form.cleaned_data
			if cl_data['password'] == '9982':
				title = cl_data['title']
				content = cl_data['content']
				blog_type = cl_data['blog_type']
				author = User.objects.filter(username='调试员')[0]
				readed_num = 0

				blog = Blog()

				blog.title = title
				blog.content = content
				blog.blog_type = blog_type
				blog.author = author
				blog.readed_num = readed_num

				blog.save()

				return redirect('/blog/')

	else:
		create_form = forms.CreateBlogForm()

	return render(request, 'blog_create.html', locals())
