from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart


"""
Creates an order to the database.
"""
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         game=item['game'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Clear the cart
            cart.clear()


            # Set the order in the session
            request.session['order_id'] = order.id
            # Redirect to the payment
            return redirect(reverse('payments:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})
