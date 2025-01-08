from authentication.models import *
from app.models import*

def Counts(request):
    table_id = request.resolver_match.kwargs.get('id')  # Get `id` from the URL kwargs
    if table_id:
        table = TableModel.objects.filter(id=table_id).first()
        if table:
            cart_count = CartModel.objects.filter(table=table).count()
            return {
                'cart_count': cart_count,
                'table_id': table.id  # Pass the table_id to the context as well
            }
    return {
        'cart_count': 0,
    }
