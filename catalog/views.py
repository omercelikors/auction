from django.shortcuts import render
from catalog.models import *
from django.http import JsonResponse
import json
from django.templatetags.static import static
from django.urls import reverse
from django.db.models import Q

# Create your views here.
def show_items(request):
	return render(request, 'show_items.html')

def api_get_items(request):
	if request.is_ajax and request.method == "GET":
		page_number = int(request.GET.get("pageNumber", 0))
		page_size = int(request.GET.get("pageSize", 10))
		start_number = ((page_number)-1) * page_size
		end_number = start_number + page_size
		prefix = 'https://' if request.is_secure() else 'http://'
		query = request.GET.get("query")
		if query:
			query_elements = query.split(' ')
			query = Q()
			for query_element in query_elements:
				query |= Q(name__icontains=query_element)
				query |= Q(description__icontains=query_element)
			total_item_number = Item.objects.filter(query).count()
			items = Item.objects.filter(query).order_by('-id')[start_number:end_number].values()
		else:
			total_item_number = Item.objects.all().count()
			items = Item.objects.order_by('-id')[start_number:end_number].values()
		
		
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
	
	return JsonResponse({"error": "any error is occured"}, status=400)

def show_item_detail(request, item_id):
	return render(request, 'show_item_detail.html', {'item_id':item_id})