# payment link


from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import JsonResponse
from django.utils import timezone
import os
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY  # Use your secret key
# print("aaaaa", stripe.api_key)
DOMAIN_APP_URL = os.getenv("DOMAIN_APP_URL")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_one_time_payment_session(request):
    user = request.user

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=user.email,
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "One-Time Service",
                        },
                        "unit_amount": 1000,  # $10.00
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",  # 👈 One-time payment mode
            success_url=f"{DOMAIN_APP_URL}/payment-success",
            cancel_url=f"{DOMAIN_APP_URL}/payment-cancel",
        )
        return JsonResponse({"url": checkout_session.url})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_subscription_session(request):
    user = request.user

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=user.email,
            line_items=[
                {
                    "price": settings.STRIPE_SUBSCRIPTION_PRICE_ID,  # Predefined recurring price ID
                    "quantity": 1,
                }
            ],
            mode="subscription",  # 👈 Subscription mode
            success_url=f"{DOMAIN_APP_URL}/subscription-success",
            cancel_url=f"{DOMAIN_APP_URL}/subscription-cancel",
        )
        return JsonResponse({"url": checkout_session.url})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')

        # Optionally check session['mode'] == 'payment' or 'subscription'
        if session['mode'] == 'subscription':
            # Mark user as subscribed
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(email=customer_email)
                user.is_subscribed = True
                user.subscription_start = timezone.now()
                user.stripe_customer_id = session.get('customer')  # Optional: save customer ID
                user.subscription_type = "premium"  # Or derive from metadata or plan name
                user.save()
            except User.DoesNotExist:
                pass

        elif session['mode'] == 'payment':
            # Handle one-time payment logic (e.g., grant access to premium content)
            print(f"✅ One-time payment completed by {customer_email}")

    return HttpResponse(status=200)
