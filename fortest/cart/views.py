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
        context['factors'] = FinalizedOrders.objects.filter(cart__id=2)  # must be change
        return context


def add_to_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    # cart_item = CartItems.objects.create(book=book, ordered=False, cart=Cart.objects.all()[1])
    cart_qs = CartItems.objects.filter(book=book, ordered='U', cart=Cart.objects.filter(id=2)[0])  # must be change
    # print(cart_item)
    if cart_qs.exists():
        cart_item = cart_qs[0]
        # if CartItems.obj.filter(book__slug=book.slug).exists():
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
    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, ordered='U', cart=Cart.objects.filter(id=2)[0])  # must be change
    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.book.stock == 0:
            cart_item.delete()
            return render(request, 'cart/unavailable.html', {'book': book})
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


def success(request):
    order_list = []
    if request.method == 'POST':
        address_id = request.POST.get('address_select')
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
                                                           ShippingAddress.objects.filter(id=address_id)[0])
            for item in order_items:  # بیا هر ایتم رو وضعیت سفارش رو به تمام شده تغییر بده.
                item.book.stock = item.book.stock - item.quantity  # موجودی کتاب به اندازه ی تعداد سفارش کم میشه
                item.book.save()
                item.ordered = 'F'
                item.save()
                finalized_obj.item.add(item)  # ایتم ها رو به فاکتور اضافه کن
            finalized_obj.save()
            return render(request, 'cart/success.html')

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


def calculate_price_coupon(request):
    total_price_noncoupon = 0
    total_price_with_coupon = 0
    if request.method == 'POST':
        code = request.POST['coupon']
        print(code)

        total_price_noncoupon = request.POST['price']
        total_price_noncoupon = int(float(total_price_noncoupon))
        print(type(total_price_noncoupon))
        coupons = CartCoupon.objects.filter(code=code)
        if coupons.exists():
            coupon = coupons[0]
            total_price_with_coupon = (int(total_price_noncoupon) * (100 - coupon.discount_percent)) / 100
        else:
            pass
    return render(request, 'cart/total_price_with_coupon.html',
                  {'total_price_with_coupon': total_price_with_coupon, 'total_price_noncoupon': total_price_noncoupon})
