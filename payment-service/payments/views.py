from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging

logger = logging.getLogger(__name__)

@api_view(["POST"],url="/api/v1/payments/initiate/")
def initiate_payment(request):
    """initiate payment"""
    
    payment = Payment.objects.create(
        order_id=request.data.get("order_id"),
        amount=request.data.get("amount"),
        currency=request.data.get("currency"),
        payment_method=request.data.get("payment_method"),
        status="PENDING",
    )
    
    return Response({
        "payment_id": str(payment.id),
        "status": payment.status,
        "amount": float(payment.amount),
        "currency": payment.currency,
        "payment_method": payment.payment_method,
        "created_at": payment.created_at,
        "updated_at": payment.updated_at,
        "message": "Payment initiated successfully"}, status=201)
