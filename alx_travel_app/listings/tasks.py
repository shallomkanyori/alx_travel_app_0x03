from celery import shared_task
from .models import Payment, Booking
from django.contrib.auth.models import User
from django.core.mail import send_mail

@shared_task
def send_payment_email(transaction_id):
    payment = Payment.objects.get(transaction_id=transaction_id)
    user = payment.booking_id.user_id
    send_mail(
        'Payment Confirmation',
        f'Your payment of {payment.amount} ETB has been received.',
        None,
        [user.email],
        fail_silently=False,
    )

@shared_task
def send_booking_email(booking_id):
    """
    Task to send an email notification when a booking is created
    """
    
    booking = Booking.objects.get(pk=booking_id)
    user = User.objects.get(pk=booking.user_id)
    
    send_mail(
        'Booking Confirmation',
        f'Hi {user.username},\n\n'
        f'This is a confirmation that your booking for {booking.listing.title} '
        f'from {booking.check_in} to {booking.check_out} has been received.\n\n'
        'Thank you for using Alx Travel!',
        None, # Use DEFAULT_FROM_EMAIL in settings.py
        [user.email],
        fail_silently=False
    )