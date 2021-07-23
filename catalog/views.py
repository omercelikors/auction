from django.shortcuts import render
from catalog.models import *
from django.http import JsonResponse
import json
from django.templatetags.static import static
from django.urls import reverse
from django.db.models import F, Q, When, Case, Value
import sys
from django.core.serializers import serialize
from django.http import HttpResponse
from django.forms.models import model_to_dict

# Create your views here.
def show_items(request):
	return render(request, 'show_items.html')

def api_get_items(request):
	if request.is_ajax and request.method == "GET":
		page_number = int(request.GET.get("pageNumber", 1))
		page_size = int(request.GET.get("pageSize", 10))
		query = request.GET.get("query",'')
		order_type = request.GET.get("order_type",1)

		start_number = ((page_number)-1) * page_size
		end_number = start_number + page_size
		prefix = 'https://' if request.is_secure() else 'http://'

		query_elements = query.split(' ')
		query = Q()
		for query_element in query_elements:
			query |= Q(name__icontains=query_element)
			query |= Q(description__icontains=query_element)
		total_item_number = Item.objects.filter(query).filter(status=1).count()
		if order_type == '1':
			items = Item.objects.filter(query).filter(status=1).order_by('-id')[start_number:end_number].values()
		elif order_type == '2':
			items = Item.objects.filter(query).filter(status=1).annotate(
																		sort_order_price=Case(
																		When(last_auction_price=None, then=('min_price')),
																			default=('last_auction_price')
																		)
																		).order_by(
																			'-sort_order_price',
																			'-id'
																		)[start_number:end_number].values()
		elif order_type == '3':
			items = Item.objects.filter(query).filter(status=1).annotate(
																		sort_order_price=Case(
																		When(last_auction_price=None, then=('min_price')),
																			default=('last_auction_price')
																		)
																		).order_by(
																			'sort_order_price',
																			'-id'
																		)[start_number:end_number].values()

		for item in items:
			item['image_path'] = prefix + request.get_host() + static(item['image_path'])
			item['url'] = prefix + request.get_host() + reverse('show_item_detail', args=(item['id'],))
			if item['last_auction_price']:
				item['auction_badge'] = 'Bidden'
				item['auction_badge_color'] = 'badge-danger'
				item['last_price'] = item['last_auction_price']
			else:
				item['auction_badge'] = 'Not bidden'
				item['auction_badge_color'] = 'badge-primary'
				item['last_price'] = item['min_price']

		response_data = {}
		response_data['results'] = list(items)
		response_data['total_item_number'] = total_item_number
		#response_data['message'] = image_url
		return JsonResponse(response_data, status=200, safe=False)
	else:
		return JsonResponse({"error": "error"}, status=400)
	# any error
	return JsonResponse({"error": "any error is occured"}, status=400)

def show_item_detail(request, item_id):
	return render(request, 'show_item_detail.html', {'item_id':item_id})

def api_get_item(request):
	if request.is_ajax and request.method == "GET":
		
		item_id = int(request.GET.get("item_id", None))
		item = Item.objects.get(pk=item_id)
		
		prefix = 'https://' if request.is_secure() else 'http://'
		item.image_path = prefix + request.get_host() + static(item.image_path)
		item.auction_start_date_time = item.auction_start_date_time.strftime("%Y-%m-%d %H:%M:%S")
		item.auction_finish_date_time = item.auction_finish_date_time.strftime("%Y-%m-%d %H:%M:%S")

		response_data = {}
		response_data['result'] = model_to_dict(item)
		response_data['message'] = "Get item is OK"
		return JsonResponse(response_data, status=200)
	else:
		return JsonResponse({"error": "error"}, status=400)
	# any error
	return JsonResponse({"error": "any error is occured"}, status=400)