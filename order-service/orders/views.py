import Requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging

logger = logging.getLogger(__name__)

@api_view(["POST"])
def create_order(request):
    """create new order"""

    order = Order.objects.create(
        user_id=request.META.get("HTTP_X_USER_ID"),
        user_email=request.META.get("HTTP_X_USER_EMAIL"),
        total_amount=request.data.get("total"),
        status="PENDING",
    )

    for item in request.data.get("items"):
        OrderItem.objects.create(
            order=order,
            product_id=item.get("product_id"),
            product_name=item.get("product_name"),
            product_sku=item.get("product_sku"),
            quantity=item.get("quantity"),
            unit_price=item.get("unit_price"),
        )

    try:
        payment_response = Requests.post(
            "http://payment-service:8001/api/v1/payments/initiate/",
            json={
                "order_id": str(order.id),
                "amount": float(order.total_amount),
                "currency": "USD",
                "payment_method": "credit_card",
            },
            headers={
                "Authorization": request.headers.get("Authorization"),
            },
        )
        if payment_response.status_code == 201:
            order.status = "PROCESSING"
            order.save()
    except requests.exceptions.Timeout:
        logger.error("Payment service timeout")
    except requests.exceptions.ConnectionError:
        logger.error("Payment service connection error")

    return Response({
        "order_id": str(order.id),
        "status": order.status,
        "total_amount": float(order.total_amount),
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "message": "Order created successfully"}, status=201)
    
    
        
        