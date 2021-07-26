from django.urls import path
from catalog import views

urlpatterns = [
    path('show/items', views.show_items, name='show_items'),
    path('api/get/items', views.api_get_items, name='api_get_items'),
    path('show/item/detail/<int:item_id>', views.show_item_detail, name='show_item_detail'),
    path('api/get/item', views.api_get_item, name='api_get_item'),
    path('api/bid/now', views.api_bid_now, name='api_bid_now'),
    path('api/auto/bidding', views.api_auto_bidding, name='api_auto_bidding'),
    path('api/get/bid/history', views.api_get_bid_history, name='api_get_bid_history'),
    path('show/config/<int:user_id>', views.show_config, name='show_config'),
    path('api/get/config', views.api_get_config, name='api_get_config'),
    path('api/update/config', views.api_update_config, name='api_update_config'),
]
