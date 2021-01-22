from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Blog, BlogType

class CreateBlogForm(forms.Form):

	password = forms.CharField(
		label='密码', max_length=10, widget=forms.PasswordInput(attrs={
			'class': 'form-control','placeholder': '密码'
		})
	)
	title = forms.CharField(
		label='标题', max_length=50, widget=forms.TextInput(attrs=
		{
			'class': 'form-control', 'placeholder': '标题', 'autofocus': ''
		})
	)
	content = forms.CharField(
		label='正文', widget=CKEditorWidget, error_messages={
			'required':'请输入正文!'
		}
	)
	blog_type = forms.ModelChoiceField(label='章节类型', queryset=BlogType.objects.all(), empty_label='请选择类型')
