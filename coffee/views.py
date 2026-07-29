from django.shortcuts import render
from django.conf import settings
from .models import CoffeeOrder
import razorpay


# Home Page
def home(request):
    return render(request, "home.html")


# Buy Now
def payment(request):

    amount = 199  # Amount in Rupees 
    amount_paise = amount * 100 

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    order = CoffeeOrder.objects.create(
        customer_name="Guest",
        email="guest@gmail.com",
        coffee_name="Cappuccino",
        amount=amount,
        razorpay_order_id=payment["id"],
        payment_status="Pending"
    )

    context = {
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount_paise
    }

    return render(request, "payment.html", context)


# Payment Success
def success(request):

    if request.method == "POST":

        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID,
                  settings.RAZORPAY_KEY_SECRET) 
        )

        try:

            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })

            order = CoffeeOrder.objects.get(
                razorpay_order_id=order_id
            )

            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.payment_status = "Success"
            order.save()

            return render(request, "success.html")

        except:

            return render(request, "failed.html")

    return render(request, "failed.html")