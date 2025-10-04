from django.conf import settings
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn = sender

