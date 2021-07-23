from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    item_user = models.ManyToManyField(User, through='ItemUser')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(User, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'item'

class UserConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    max_bid_amount = models.FloatField(blank=True, null=True)
    left_bid_amount = models.FloatField(blank=True, null=True)
    fund = models.FloatField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(User, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'user_config'

class ItemUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    bid_amount = models.FloatField(blank=True, null=True)
    auto_bidding_status = models.SmallIntegerField()
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(User, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'item_users'