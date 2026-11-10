import logging

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


class OrderNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


@require_http_methods(["GET"])
def get_order(request, order_id):
    try:
        order = fetch_order(order_id)

        return JsonResponse({
            'status': 'success',
            'data': order
        })

    except OrderNotFoundError:
        return JsonResponse({
            'message': 'Order not found'
        }, status=404)

    except InsufficientStockError:
        return JsonResponse({
            'message': 'Insufficient stock'
        }, status=400)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

        return JsonResponse({
            'message': 'Internal server error'
        }, status=500)


def fetch_order(order_id):
    orders = {
        '1': {'id': '1', 'item': 'Widget', 'qty': 5},
        '2': {'id': '2', 'item': 'Gadget', 'qty': 0}
    }

    if not order_id:
        raise OrderNotFoundError()

    if order_id not in orders:
        raise OrderNotFoundError()

    if orders[order_id]['qty'] == 0:
        raise InsufficientStockError()

    return orders[order_id]