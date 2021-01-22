import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from blog.models import Blog

def read_statistics_once_read(request, obj):
	ct = ContentType.objects.get_for_model(obj)
	key = '{}_{}_read'.format(ct.model, obj.id)

	if not request.COOKIES.get(key):
		readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)
		readnum.read_num += 1
		readnum.save()

		date = timezone.now().date()

		read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=date)
		read_detail.read_num += 1
		read_detail.save()

	return key

def get_week_read_data(content_type):
	today = timezone.now().date()
	dates = []

	read_nums = []
	for i in range(6, -1, -1):
		date = today - datetime.timedelta(days=i)
		dates.append(date.strftime('%m/%d'))

		read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
		result = read_details.aggregate(read_num_sum=Sum('read_num'))
		read_nums.append(result['read_num_sum'] or 0)

	return dates, read_nums

def get_today_hot_data(content_type):
	today = timezone.now().date()
	read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')

	return read_details[ :4]

def get_yesterday_hot_data(content_type):
	today = timezone.now().date()
	yesterday = today - datetime.timedelta(days=1)
	read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')

	return read_details[ :4]

def get_week_hot_data():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=7)

	blogs = Blog.objects \
				.filter(read_details__date__lte=today, read_details__date__gt=date) \
				.values('id', 'title') \
				.annotate(read_num_sum=Sum('read_details__read_num')) \
				.order_by('-read_num_sum')

	return blogs[ :4]

def get_month_hot_data():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=30)

	blogs = Blog.objects \
				.filter(read_details__date__lte=today, read_details__date__gt=date) \
				.values('id', 'title') \
				.annotate(read_num_sum=Sum('read_details__read_num')) \
				.order_by('-read_num_sum')

	return blogs[ :4]
