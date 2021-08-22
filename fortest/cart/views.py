from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView

from book.models import Book
from accounts.models import ShippingAddress
from cart.models import CartItems, Cart, FinalizedOrders
from coupon.models import CartCoupon


class CartView(ListView):
    model = CartItems
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        total_price_cart = 0
        for item in CartItems.objects.filter(cart__id=2, ordered='U'):  # must be change
            total_price_cart += item.total_price
        context = super().get_context_data(**kwargs)
        context['cart'] = CartItems.objects.filter(cart__id=2, ordered='U')  # must be change
        context['order'] = CartItems.objects.filter(cart__id=2, ordered='O')  # must be change
        context['total_price_cart'] = total_price_cart

        return context


class OrderedFromCartView(ListView):
    model = CartItems
    template_name = 'cart/ordered.html'

    # def post(self,request,*args, **kwargs):
    #     coupon = self.request.POST['coupon']
    #     print(coupon)
    #     return redirect('orderedcart', coupon)

    def get_context_data(self, **kwargs):
        total_price_ordered = 0
        for item in CartItems.objects.filter(cart__id=2, ordered='O'):  # must be change
            total_price_ordered += item.total_price
        # total_price_ordered -= coupon

        context = super().get_context_data(**kwargs)
        context['ordered'] = CartItems.objects.filter(cart__id=2, ordered='O')  # must be change
        context['addresses'] = ShippingAddress.objects.filter(user=2)  # must be change
        context['total_price_ordered'] = total_price_ordered
        return context


# def ordered_from_view(request):
#     total_price_ordered = 0
#     context = {}
#     if request.method == 'POST':
#         coupon = request.POST['coupon']
#         print(coupon)
#         for item in CartItems.objects.filter(cart__id=2, ordered='O'):  # must be change
#             total_price_ordered += item.total_price
#         total_price_ordered -= coupon
#     context['ordered'] = CartItems.objects.filter(cart__id=2, ordered='O')  # must be change
#     context['addresses'] = ShippingAddress.objects.filter(user=2)  # must be change
#     context['total_price_ordered'] = total_price_ordered
#
#     return render(request, 'cart/ordered.html', context)


class MyFactorsView(ListView):
    model = FinalizedOrders
    template_name = 'cart/factors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['factors'] = FinalizedOrders.objects.filter(cart__id=2, payment=True)  # must be change
        return context


def add_to_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    # cart_item = CartItems.objects.create(book=book, ordered=False, cart=Cart.objects.all()[1])
    cart_qs = CartItems.objects.filter(book=book, ordered='U', cart=Cart.objects.filter(id=2)[0])  # must be change
    # print(cart_item)
    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.book.stock <= cart_item.quantity:
            pass
        # if CartItems.obj.filter(book__slug=book.slug).exists():
        else:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item = CartItems.objects.create(book=book, ordered='U', cart=Cart.objects.filter(id=2)[0])
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, cart=Cart.objects.filter(id=2)[0])  # must be change
    if cart_qs.exists():
        cart_item = cart_qs[0]
        cart_item.delete()

    return redirect('cart')


def check_ordered(request, slug):
    allowed = False
    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, ordered='U', cart=Cart.objects.filter(id=2)[0])  # must be change
    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.book.stock == 0:
            allowed = True
            cart_item.delete()
            return render(request, 'cart/cart.html', {'book': book, 'allowed': allowed})

        else:
            is_ordered_item_qs = CartItems.objects.filter(book=book, ordered='O',
                                                          cart=Cart.objects.filter(id=2)[0])  # must be change
            if is_ordered_item_qs.exists():
                is_ordered_item = is_ordered_item_qs[0]
                is_ordered_item.quantity += cart_item.quantity
                is_ordered_item.save()
                cart_item.delete()
            else:
                cart_item.ordered = 'O'  # ordering
                cart_item.save()

    return redirect('orderedcart')


def check_unordered(request, slug):
    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, ordered='O', cart=Cart.objects.filter(id=2)[0])  # must be change
    if cart_qs.exists():
        cart_item = cart_qs[0]
        cart_item.ordered = 'U'  # un ordering
        cart_item.save()

    return redirect('orderedcart')


def create_factor(request):
    context = {}
    order_list = []
    if request.method == 'POST':
        address_id = request.POST.get('address_select')
        price = request.POST.get('price')
        price = float(price)
        price = int(price)
        print(price, type(price))
        order_items = CartItems.objects.filter(cart__id=2,
                                               ordered='O')  # must be change ... ایتم های انتخاب شده برای خرید قطعی
        for order in order_items:
            if order.book.stock == 0:  # بررسی موجودی هر کتابی که انتخاب شده
                order_list.append(order)  # اضافه کردن کتابهایی که ناموجودن
            else:
                pass

        if len(order_list) == 0:  # اگر همه کتابها موجود بودن
            # بیا فاکتور خرید و صادر کن
            finalized_obj = FinalizedOrders.objects.create(cart=Cart.objects.filter(id=2)[0]
                                                           , shipping_address=
                                                           ShippingAddress.objects.filter(id=address_id)[0],
                                                           price=price)
            for item in order_items:  # بیا هر ایتم رو وضعیت سفارش رو به تمام شده تغییر بده.
                # item.book.stock = item.book.stock - item.quantity  # موجودی کتاب به اندازه ی تعداد سفارش کم میشه
                # item.book.save()
                # item.ordered = 'F'
                # item.save()
                finalized_obj.item.add(item)  # ایتم ها رو به فاکتور اضافه کن
            finalized_obj.save()
            finalized_obj_id = finalized_obj.id
            context['price'] = price
            context['finalized_obj_id'] = finalized_obj_id
            context['finalized_obj'] = finalized_obj
            print(context)
            return render(request, 'cart/coupon.html', context)

        elif len(order_list) > 0:  # اگر کتابی ناموجود بود
            for order in order_list:
                order.delete()
            return render(request, 'cart/unavailable.html', {'order_list': order_list})


def plus_quantity(request, slug):
    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, ordered='U', cart=Cart.objects.filter(id=2)[0])  # must be change
    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.quantity >= cart_item.book.stock:
            pass
        else:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart')


def minus_quantity(request, slug):
    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, ordered='U', cart=Cart.objects.filter(id=2)[0])  # must be change
    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.quantity <= 1:
            pass
        else:
            cart_item.quantity -= 1
            cart_item.save()

    return redirect('cart')


def save_coupon_to_factor(request):
    context = {}
    finalized_obj = None
    if request.method == 'POST':
        coupon_code = request.POST['coupon']
        finalized_obj_id = request.POST['finalized_obj_id']
        finalized_obj_id = int(finalized_obj_id)
        finalized_obj_qs = FinalizedOrders.objects.filter(id=finalized_obj_id)
        if finalized_obj_qs.exists():
            finalized_obj = finalized_obj_qs[0]
        coupon_qs = CartCoupon.objects.filter(code=coupon_code)
        if coupon_qs.exists():
            coupon = coupon_qs[0]
            if finalized_obj.discount == 0:  # چک میکنه کد تخفیف نداشته باشه
                finalized_obj.discount = coupon.discount_percent
                finalized_obj.save()
                context['finalized_obj'] = finalized_obj
                context['finalized_obj_id'] = finalized_obj_id
            else:
                context['finalized_obj'] = finalized_obj
                context['finalized_obj_id'] = finalized_obj_id
        else:
            context['finalized_obj'] = finalized_obj
            context['finalized_obj_id'] = finalized_obj_id

    return render(request, 'cart/coupon.html', context)


def success(request):
    finalized_obj = None
    if request.method == 'POST':
        finalized_obj_id = request.POST['finalized_obj_id']
        finalized_obj_id = int(finalized_obj_id)
        finalized_obj_qs = FinalizedOrders.objects.filter(id=finalized_obj_id)
        if finalized_obj_qs.exists():
            finalized_obj = finalized_obj_qs[0]
            finalized_obj.payment = True
            finalized_obj.save()
            for item in finalized_obj.item.all():  # بیا هر ایتم رو وضعیت سفارش رو به تمام شده تغییر بده.
                item.book.stock = item.book.stock - item.quantity  # موجودی کتاب به اندازه ی تعداد سفارش کم میشه
                item.book.save()
                item.ordered = 'F'
                item.save()
    return render(request, 'cart/success.html')

