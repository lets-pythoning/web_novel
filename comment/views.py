from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm

def update_comment(request):
	comment_form = CommentForm(request.POST, user=request.user)
	data = {}
	if comment_form.is_valid():
		comment = Comment()
		comment.user = comment_form.cleaned_data['user']
		comment.text = comment_form.cleaned_data['text']
		comment.content_object = comment_form.cleaned_data['content_object']

		parent = comment_form.cleaned_data['parent']
		if parent is not None:
			comment.root = parent if parent.root is None else parent.root
			comment.parent = parent
			comment.reply_to = parent.user

		comment.save()

		data['status'] = 'SUCCESS'
		data['username'] = comment.user.username
		data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
		data['text'] = comment.text

		if parent is not None:
			data['reply_to'] = comment.reply_to.username
		else:
			data['reply_to'] = ''

		data['id'] = comment.id
		data['root_id'] = '' if comment.root is None else comment.parent.root.id

	else:
		data['status'] = 'ERROR'
		data['message'] = list(comment_form.errors.values())[0][0]

	return JsonResponse(data)
