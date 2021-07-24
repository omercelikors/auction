from django.shortcuts import render
from catalog.models import *
from django.http import JsonResponse
import json
from django.templatetags.static import static
from django.urls import reverse
from django.db.models import Q, When, Case
import sys
from django.forms.models import model_to_dict

# Create your views here.
def show_items(request):
	return render(request, 'show_items.html')

def api_get_items(request):
	if request.is_ajax and request.method == "GET" and request.user.is_authenticated:
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
	if request.is_ajax and request.method == "GET" and request.user.is_authenticated:
		
		item_id = int(request.GET.get("item_id", None))
		item = Item.objects.values().get(pk=item_id)

		current_user = request.user
		item_user_auto_bid_case = ItemUserAutoBidCase.objects.filter(user=current_user, item=item['id']).exists()
		if item_user_auto_bid_case:
			item_user_auto_bid_case = ItemUserAutoBidCase.objects.filter(user=current_user, item=item['id']).first()
			auto_bidding_status = item_user_auto_bid_case.auto_bidding_status
		else:
			auto_bidding_status = 0
		
		item_bid_amounts = ItemUserBidAmount.objects.filter(item=item['id']).values()
		prefix = 'https://' if request.is_secure() else 'http://'
		item['image_path'] = prefix + request.get_host() + static(item['image_path'])
		item['auction_start_date_time'] = item['auction_start_date_time'].strftime("%Y-%m-%d %H:%M:%S")
		item['auction_finish_date_time'] = item['auction_finish_date_time'].strftime("%Y-%m-%d %H:%M:%S")
		item['auto_bidding_status'] = auto_bidding_status

		response_data = {}
		response_data['result'] = item
		response_data['message'] = "Get item is OK"
		return JsonResponse(response_data, status=200)
	else:
		return JsonResponse({"error": "error"}, status=400)
	# any error
	return JsonResponse({"error": "any error is occured"}, status=400)

def api_bid_now(request):
	if request.is_ajax and request.method == "GET" and request.user.is_authenticated:
		current_user = request.user
		current_user_config = UserConfig.objects.get(user_id=current_user.id)
		current_user_fund = current_user_config.fund
		current_user_max_bid_amount = current_user_config.max_bid_amount

		item_id = int(request.GET.get("item_id", None))
		item = Item.objects.get(id=item_id)
		item_last_price = item.last_auction_price if item.last_auction_price else item.min_price
		item_auction_finish_date_time = item.auction_finish_date_time

		item_user_bid_amount = ItemUserBidAmount.objects.filter(item_id=item_id).exists()
		if item_user_bid_amount:
			item_user_bid_amount = ItemUserBidAmount.objects.filter(item_id=item_id).last()
			last_bid_user_id = item_user_bid_amount.user_id
		else:
			last_bid_user_id = None

		response_data = {}
		response_data['result'] = None
		# time check
		if item_auction_finish_date_time < datetime.now():
			response_data['message'] = "Auction ended"
			return JsonResponse(response_data, status=400)
		# fund check
		if current_user_fund < item_last_price+1:
			response_data['message'] = "Insufficient balance"
			return JsonResponse(response_data, status=400)
		# last auctioneer check
		if last_bid_user_id == current_user.id:
			response_data['message'] = "The highest bid in the system belongs to you"
			return JsonResponse(response_data, status=400)
		# create item_user_bid_amount history
		item_user_bid_amount = ItemUserBidAmount(user=current_user, item=item, bid_amount=item_last_price + 1, is_auto_bidding=0)
		item_user_bid_amount.save()
		# update user fund on user_config table
		current_user_config.fund = current_user_fund - (item_last_price + 1)
		current_user_config.save()
		# update last_auction_price on item table
		item.last_auction_price = item_last_price + 1
		item.save()

		response_data['message'] = "Your bid has been received"
		return JsonResponse(response_data, status=200)

def api_auto_bidding(request):
	if request.is_ajax and request.method == "GET" and request.user.is_authenticated:
		item_id = int(request.GET.get("item_id", None))
		auto_bidding_status = int(request.GET.get("auto_bidding_status", None))
		item = Item.objects.get(pk=item_id)
		current_user = request.user
		item_user_auto_bid_case = ItemUserAutoBidCase.objects.filter(user=current_user, item=item).exists()
		if item_user_auto_bid_case:
			# update
			item_user_auto_bid_case = ItemUserAutoBidCase.objects.filter(user=current_user, item=item).first()
			item_user_auto_bid_case.auto_bidding_status = auto_bidding_status
			item_user_auto_bid_case.save()
		else:
			# create
			item_user_auto_bid_case = ItemUserAutoBidCase(user=current_user, item=item, auto_bidding_status=auto_bidding_status)
			item_user_auto_bid_case.save()
	
		response_data = {}
		response_data['result'] = True
		response_data['message'] = "Auto bid update is OK"
		return JsonResponse(response_data, status=200)