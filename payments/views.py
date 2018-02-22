from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from orders.models import Order
from core.models import Player, Developer
from django.views.decorators.csrf import csrf_exempt
from hashlib import md5
from payments.forms import PaymentForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


"""
Renders the view for succesful payment and adds the game to the players inventory.
Also sends a confirmation email to the user of the completed purchase.
"""
@csrf_exempt
def payment_done(request):
    if request.GET['result'] == 'success':
        pid = request.GET['pid']
        order = get_object_or_404(Order, id=pid)
        order.paid = True
        order.save()
        items = order.items.all()
        uid = request.user.id
        player = get_object_or_404(Player, user_id=uid)
        games = []
        for item in items:
            player.games.add(item.game)
            item.game.times_bought += 1
            games.append(item.game)
            item.game.save()
        player.save()

        # The confirmation email.
        mail_subject = 'Thank you for your purchase!'
        message = render_to_string('payments/done_email.html', {
            'user': request.user,
            'first_name': order.first_name,
            'last_name': order.last_name,
            'email': order.email,
            'address': order.address,
            'postal_code': order.postal_code,
            'city': order.city,
            'games': games,
            'price': order.get_total_cost()})
        to_email = order.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return render(request, 'payments/done.html')
    else:
        return render(request, 'payments/canceled.html')


"""
Renders the canceled payment page.
"""
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payments/canceled.html')

"""
Renders the error -page when there is an error with the payment
"""
@csrf_exempt
def payment_error(request):
    return render(request, 'payments/error.html')


"""
Processes the payment of the order. Creates the values for the post message needed
for the mockup payment size.
"""
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    pid = order.id
    sid = 'thebestgamestore'
    amount = '%.2f' % order.get_total_cost().quantize(Decimal('.01'))
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, settings.SECRET_KEY)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()

    # Inputs for the POST -message.
    payment_details = {
        'pid':          pid,
        'sid':          sid,
        'amount':       amount,
        'success_url':  'http://{}{}'.format(host, reverse('payments:done')),
        'cancel_url':   'http://{}{}'.format(host, reverse('payments:canceled')),
        'error_url':    'http://{}{}'.format(host, reverse('payments:error')),
        'checksum':     checksum
    }
    form = PaymentForm(payment_details)
    return render(request, 'payments/process.html', {'order': order,
                                                    'form':form})
