from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=600)
    image_path = models.CharField(max_length=600)
    min_price = models.FloatField(blank=False, null=False)
    last_auction_price = models.FloatField(blank=True, null=True)
    auction_start_date_time = models.DateTimeField(blank=True, null=True)
    auction_finish_date_time = models.DateTimeField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    user_bid_amounts = models.ManyToManyField(User, through='ItemUserBidAmount', related_name='item_bid_amounts')
    user_auto_bid_cases = models.ManyToManyField(User, through='ItemUserAutoBidCase', related_name='item_bid_cases')
    class Meta:
        managed = True
        db_table = 'item'

class UserConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='config')
    max_bid_amount = models.FloatField(blank=True, null=True)
    fund = models.FloatField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'user_config'

class ItemUserBidAmount(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    bid_amount = models.FloatField(blank=True, null=True)
    is_auto_bidding = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'item_user_bid_amounts'

class ItemUserAutoBidCase(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    auto_bidding_status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'item_user_auto_bid_cases'