# payment link

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY  # Use your secret key
# print("aaaaa", stripe.api_key)

@api_view(["POST"])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can pay
def create_checkout_session(request):
    # Get authenticated user
    user = request.user  # This should be the authenticated user
    print(user)  # Debugging: Ensure this prints the logged-in user
    # print("settings.STRIPE_SECRET_KEY", settings.STRIPE_SECRET_KEY)

    # Additional authentication check (just in case)
    if not user.is_authenticated:
        return Response({'error': 'Unauthorized'}, status=401)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=user.email,  # Associate payment with the user
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Premium Subscription",
                        },
                        "unit_amount": 5000,  # $50.00
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:5173/success",
            cancel_url="http://localhost:5173/cancel",
        )
        return JsonResponse({"url": checkout_session.url}, safe=False)
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=400)
    except Exception:
        return Response({"error": "An unexpected error occurred"}, status=500)
    

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import stripe

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.headers.get("Stripe-Signature")
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except stripe.error.SignatureVerificationError as e:
#         return JsonResponse({"error": "Invalid signature"}, status=400)

#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]
#         print(f"Payment successful for {session['customer_email']}")

#     return JsonResponse({"status": "success"})


##########################################################################
# payments/views.py
# from django.shortcuts import render
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# from django.conf import settings
# import stripe
# stripe.api_key = settings.STRIPE_SECRET_KEY


# @api_view(["POST"])
# def create_checkout_session(request):
#     try:
#         session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             mode="payment",
#             success_url="http://localhost:3000/success",
#             cancel_url="http://localhost:3000/cancel",
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "product_data": {"name": "Test Product"},
#                         "unit_amount": 1000,  # Amount in cents ($10.00)
#                     },
#                     "quantity": 1,
#                 }
#             ],
#         )
#         return JsonResponse({"sessionId": session.id})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.headers.get("Stripe-Signature")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError:
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError:
#         return HttpResponse(status=400)

#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]
#         print("Payment was successful!", session)

#     return HttpResponse(status=200)


