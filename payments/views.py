from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from orders.models import Order
from core.models import Player, Developer
from django.views.decorators.csrf import csrf_exempt
from hashlib import md5
from payments.forms import PaymentForm



@csrf_exempt
def payment_done(request):
    pid = request.GET['pid']
    order = get_object_or_404(Order, id=pid)
    order.paid = True
    order.save()
    items = order.items.all()
    uid = request.user.id
    player = get_object_or_404(Player, user_id=uid)
    for item in items:
        player.games.add(item.game)
    return render(request, 'payments/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payments/canceled.html')

def checksum(pid, sid, amount, token):
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, settings.SECRET_KEY)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()



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

    payment_details = {
        'pid':          pid,
        'sid':          sid,
        'amount':       amount,
        'success_url':  'http://{}{}'.format(host, reverse('payments:done')),
        'cancel_url':   'http://{}{}'.format(host, reverse('payments:canceled')),
        'error_url':    'http://{}{}'.format(host, reverse('payments:canceled')),
        'checksum':     checksum
    }
    form = PaymentForm(payment_details)
    return render(request, 'payments/process.html', {'order': order,
                                                    'form':form})
