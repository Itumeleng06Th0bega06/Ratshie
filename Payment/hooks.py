from django.conf import settings
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn = sender

    # Only handle completed payments
    if ipn.payment_status != ST_PP_COMPLETED:
        return

    # Optional sanity check: received by our business email
    if getattr(ipn, 'receiver_email', None) != getattr(settings, 'PAYPAL_RECEIVER_EMAIL', None):
        return

    # Minimal output like in the tutorial
    print('PAYPAL IPN RECEIVED')
    print(f'Amount Paid: {getattr(ipn, "mc_gross", None)} Invoice: {getattr(ipn, "invoice", None)}')
