from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.forms import ValidationError
from Shop.models import Product
from django.dispatch import receiver
import datetime



# Create your models here.
# Payment models
class ShippingAddress(models.Model):
    # Explicit primary key helps static type checkers (Pylance/Pyright) recognize the attribute
    # Django will create this implicitly if omitted, but declaring it removes "unknown attribute 'id'" warnings.
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.TextField(max_length=300)
    shipping_address2 = models.TextField(max_length=300, null=True, blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f"Shipping Address - {str(self.id)}" 


# default user profile when register

def Create_Shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()


# automate profile
post_save.connect(Create_Shipping, sender=User)


# Create Oder Model
class Order(models.Model):
    # Explicit primary key to satisfy static analyzers (Django would create this implicitly)
    id = models.AutoField(primary_key=True)
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)
    invoice_id = models.CharField(max_length=130, blank=True,default=" ")

    def __str__(self):
        if self.amount_paid <= 0:
            raise ValidationError({"amount_paid": "Amount Must Be Positive"})
        return f'Oder - {str(self.id)}' 

    # Auto add dates
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now


class OrderItem(models.Model):
    # Explicit primary key to satisfy static analyzers
    id = models.AutoField(primary_key=True)
    # foreign keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Oder Item - {str(self.id)}'
