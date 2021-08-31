import datetime
import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from account.models import ShippingAddress, CustomUser
from book.models import Book
from cart.models import CartItems, Cart, FinalizedOrders
from coupon.models import CartCoupon


class CartView(LoginRequiredMixin, ListView):
    """
    سبد خرید
    """

    model = Cart
    template_name = 'cart/cart.html'
    context_object_name = 'my_items'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        :param object_list: -
        :param kwargs: -
        :return: قیمت نهایی فاکتور خرید
        """

        total_price_factor = 0
        for item in CartItems.objects.filter(cart=Cart.objects.get(user=self.request.user), ordered='O'):
            total_price_factor += item.total_price

        context = super().get_context_data(**kwargs)
        context['total_price_factor'] = total_price_factor
        context['addresses'] = ShippingAddress.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        """
        :return: سفارشات درون سبد خرید کاربر
        """

        queryset = super(CartView, self).get_queryset()
        queryset = queryset.get(user=self.request.user).cartitems_set.filter(ordered='O')
        return queryset


class NextCartView(LoginRequiredMixin, ListView):
    """
    سبد خرید بعدی
    """

    model = Cart
    template_name = 'cart/next_cart.html'
    context_object_name = 'my_items'

    def get_queryset(self):
        """
        :return: سفارشات درون سبد خرید کاربر
        """

        queryset = super(NextCartView, self).get_queryset()
        queryset = queryset.get(user=self.request.user).cartitems_set.filter(ordered='U')
        return queryset


class HistoryListView(LoginRequiredMixin, ListView):
    """
    نمتایش خلاصه ای از تمام خرید های کاربر
    """

    model = FinalizedOrders
    template_name = 'cart/history.html'
    context_object_name = 'factors'

    def get_queryset(self):
        """
        :return: فاکتور خرید های کاربر
        """

        queryset = super(HistoryListView, self).get_queryset()
        queryset = queryset.filter(cart=Cart.objects.get(user=self.request.user))
        return queryset


class FactorsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    تمام فاکتور خریدها در پنل کارمند
    """

    model = FinalizedOrders
    context_object_name = 'factors'
    template_name = 'staff/factors.html'
    queryset = FinalizedOrders.objects.all()
    permission_required = 'book.add_book'


class OrdersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    تمام سفارشات در پنل کارمند
    """

    model = FinalizedOrders
    context_object_name = 'orders'
    template_name = 'staff/orders.html'
    queryset = CartItems.objects.all()
    permission_required = 'book.add_book'


def add_to_cart(request, slug):
    """
    :param request: 😐
    :param slug: اسلاگ کتاب انتخاب شده
    :return: سرجاش میمونه
    """

    book = get_object_or_404(Book, slug=slug)
    device = request.COOKIES['device']
    cart_qs = CartItems.objects.filter(book=book, ordered='O',
                                       cart=Cart.objects.get(user=request.user))
    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.book.stock <= cart_item.quantity:
            pass
        else:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item = CartItems.objects.create(book=book, ordered='O', cart=Cart.objects.get(user=request.user))
        cart_item.save()

    return redirect('book_detail', slug=slug)


@login_required
def add_to_next_cart(request, slug):
    """
    آیتم انتخابی در سبد خرید را میگیرد و در لیست خرید بعدی قرار می دهد.
    :param request: -
    :param slug: -
    :return: صفحه ی لیست خرید
    """

    allowed = False
    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, ordered='O', cart=Cart.objects.get(user=request.user))
    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.book.stock == 0:
            allowed = True
            cart_item.delete()
            return render(request, 'cart/cart.html', {'book': book, 'allowed': allowed})

        else:
            is_ordered_item_qs = CartItems.objects.filter(book=book, ordered='U',
                                                          cart=Cart.objects.get(user=request.user))
            if is_ordered_item_qs.exists():
                is_ordered_item = is_ordered_item_qs[0]
                is_ordered_item.quantity += cart_item.quantity
                is_ordered_item.save()
                cart_item.delete()
            else:
                cart_item.ordered = 'U'
                cart_item.save()

    return redirect('cart')


@login_required
def return_to_cart(request, slug):
    """
    :param request: 😐
    :param slug: اسلاگ کتاب انتخاب شده
    :return: سرجاش میمونه
    """

    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, ordered='U',
                                       cart=Cart.objects.get(user=request.user))

    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.book.stock < cart_item.quantity:
            pass
        else:
            cart_item.ordered = 'O'
            cart_item.save()
    else:
        cart_item = CartItems.objects.create(book=book, ordered='O', cart=Cart.objects.get(user=request.user))
        cart_item.save()

    return redirect('next_cart')


@login_required()
def return_all_to_cart(request):
    """
    بازگردانی همه ی لیست خرید بعدی به سبد خرید
    :param request: -
    :return: -
    """

    next_cart_item = CartItems.objects.filter(ordered='U', cart=Cart.objects.get(user=request.user))
    if next_cart_item.exists():
        for item in next_cart_item:
            item.ordered = 'O'
            item.save()

    return redirect('next_cart')


@login_required()
def remove_from_cart(request, slug):
    """
    :param request: 😑
    :param slug: اسلاگ کتاب
    :return: سرجاش توی سبد خرید بمونه
    """

    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, cart=Cart.objects.get(user=request.user))
    if cart_qs.exists():
        cart_item = cart_qs[0]
        cart_item.delete()

    return redirect('cart')


@login_required()
def remove_from_next_cart(request, slug):
    """
    :param request: 😑
    :param slug: اسلاگ کتاب
    :return: سرجاش توی سبد خرید بعدی بمونه
    """

    book = get_object_or_404(Book, slug=slug)
    cart_qs = CartItems.objects.filter(book=book, cart=Cart.objects.get(user=request.user))
    if cart_qs.exists():
        cart_item = cart_qs[0]
        cart_item.delete()

    return redirect('next_cart')


@login_required()
def quantity(request, slug):
    """
    افزایش تعداد دلخواه از کتاب در سبد خرید به شرط داشتن موجودی کافی از کتاب کاهش تعداد دلخواه از کتاب در سبد خرید تا رسیدن به تعداد 1
    :param request: -
    :param slug: -
    :return: سرجاش میمونه
    """

    if request.method == 'POST' and 'plus_quantity' in request.POST:
        book = get_object_or_404(Book, slug=slug)
        cart_qs = CartItems.objects.filter(book=book, ordered='O', cart=Cart.objects.get(user=request.user))
        if cart_qs.exists():
            cart_item = cart_qs[0]
            if cart_item.quantity >= cart_item.book.stock:
                pass
            else:
                cart_item.quantity += 1
                cart_item.save()

    elif request.method == 'POST' and 'minus_quantity' in request.POST:
        book = get_object_or_404(Book, slug=slug)
        cart_qs = CartItems.objects.filter(book=book, ordered='O', cart=Cart.objects.get(user=request.user))
        if cart_qs.exists():
            cart_item = cart_qs[0]
            if cart_item.quantity <= 1:
                pass
            else:
                cart_item.quantity -= 1
                cart_item.save()

    return redirect('cart')


@login_required()
def quantity_next_cart(request, slug):
    """
    افزایش تعداد دلخواه از کتاب در سبد خرید به شرط داشتن موجودی کافی از کتاب کاهش تعداد دلخواه از کتاب در سبد خرید تا رسیدن به تعداد 1
    :param request: -
    :param slug: -
    :return: سرجاش میمونه
    """

    if request.method == 'POST' and 'plus_quantity' in request.POST:
        book = get_object_or_404(Book, slug=slug)
        cart_qs = CartItems.objects.filter(book=book, ordered='U', cart=Cart.objects.get(user=request.user))
        if cart_qs.exists():
            cart_item = cart_qs[0]
            if cart_item.quantity >= cart_item.book.stock:
                pass
            else:
                cart_item.quantity += 1
                cart_item.save()

    elif request.method == 'POST' and 'minus_quantity' in request.POST:
        book = get_object_or_404(Book, slug=slug)
        cart_qs = CartItems.objects.filter(book=book, ordered='U', cart=Cart.objects.get(user=request.user))
        if cart_qs.exists():
            cart_item = cart_qs[0]
            if cart_item.quantity <= 1:
                pass
            else:
                cart_item.quantity -= 1
                cart_item.save()

    return redirect('cart')


@login_required()
def create_factor(request):
    """
    ایجاد یک فاکتور خرید از سبد کاربر با ادرس
    :param request: -
    :return: انتقال به پرداخت و کد تخفیف
    """

    no_stock = False
    context = {}
    order_list = []

    if request.method == 'POST':
        address_id = request.POST.get('address_select')
        price = str(request.POST.get('price'))
        price = float(price)
        price = int(price)
        order_items = CartItems.objects.filter(cart=Cart.objects.get(user=request.user),
                                               ordered='O')  # must be change ... ایتم های انتخاب شده برای خرید قطعی
        for order in order_items:
            if order.book.stock == 0:  # بررسی موجودی هر کتابی که انتخاب شده
                order_list.append(order)  # اضافه کردن کتابهایی که ناموجودن
            else:
                pass

        if len(order_list) == 0:  # اگر همه کتابها موجود بودن
            # بیا فاکتور خرید و صادر کن
            finalized_obj = FinalizedOrders.objects.create(price=price, payment=False,
                                                           cart=Cart.objects.get(user=request.user),
                                                           shipping_address=ShippingAddress.objects.get(id=address_id))
            for item in order_items:  # بیا هر ایتم رو وضعیت سفارش رو به تمام شده تغییر بده.
                finalized_obj.item.add(item)  # ایتم ها رو به فاکتور اضافه کن
            finalized_obj.save()
            context['finalized_obj'] = finalized_obj
            return render(request, 'cart/payment.html', context)

        elif len(order_list) > 0:  # اگر کتابی ناموجود بود
            for order in order_list:
                order.delete()
            return redirect('cart')


@login_required()
def save_coupon_to_factor(request):
    """
    اعمال کد تخفیف
    :param request: -
    :return: -
    """

    context = {}
    finalized_obj = None
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon', False)
        finalized_obj_id = request.POST['finalized_obj_id']
        finalized_obj_id = int(finalized_obj_id)
        finalized_obj_qs = FinalizedOrders.objects.filter(id=finalized_obj_id)
        if finalized_obj_qs.exists():
            finalized_obj = finalized_obj_qs[0]
        coupon_qs = CartCoupon.objects.filter(code=coupon_code)
        if coupon_qs.exists():
            coupon = coupon_qs[0]
            # تاریخ و اعتبارش چک بشه
            if coupon.is_active:
                now = datetime.datetime.now()
                if (now > coupon.valid_from.replace(tzinfo=None)) and (
                        now < coupon.valid_to.replace(tzinfo=None)):  # چک می کنه کد تخفیف اعتبار داشته باشه
                    if finalized_obj.discount == 0:  # چک میکنه سبد کد تخفیف نداشته باشه
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
            else:
                context['finalized_obj'] = finalized_obj
                context['finalized_obj_id'] = finalized_obj_id
        else:
            context['finalized_obj'] = finalized_obj
            context['finalized_obj_id'] = finalized_obj_id

    return render(request, 'cart/payment.html', context)


@login_required()
def success(request):
    """
    پرداخت
    :param request: -
    :return: -
    """

    finalized_obj = None
    if request.method == 'POST':
        finalized_obj_id = request.POST.get('finalized_obj_id')
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


def add_to_session(request, slug):
    """
    افزودن کتاب در سبد خرید کاربری که لاگین نکرده است.
    :param request: -
    :param slug: -
    :return: ماندن در صفحه ی کتاب مورد نظر
    """

    book = get_object_or_404(Book, slug=slug)

    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    else:
        request.session.set_test_cookie()
        messages.error(request, 'Please enable cookie')

    if not 'books' in request.session or not request.session['books']:
        request.session['books'] = []
    book_list = request.session['books']

    if book.name in book_list:
        pass
    else:
        book_list.append(book.name)
        print(request.session['books'])

    return redirect('book_detail', slug=slug)


def anonymous_cart(request):
    """
    سبد خرید فرد ناشناس
    :param request: -
    :return: سبد خرید فرد لاگین نکرده
    """

    context = {}
    book_obj_list = []

    if 'books' not in request.session or not request.session['books']:
        context['my_items'] = False
    else:
        book_list = request.session['books']
        for book_name in book_list:
            book_obj_qs = Book.objects.filter(name=book_name)
            if book_obj_qs.exists():
                book_obj = book_obj_qs[0]
                book_obj_list.append(book_obj)

        context['my_items'] = book_obj_list

    return render(request, 'cart/anonymous_cart.html', context)


def anonymous_cart_remove(request, slug):
    """
    حذف سفارش از سبد خرید فرد ناشناس
    :param request: -
    :param slug: -
    :return: -
    """

    book = get_object_or_404(Book, slug=slug)
    book_list = request.session['books']

    for item in book_list:
        if item == book.name:
            book_list.remove(item)
            break
    request.session['books'] = book_list

    return redirect('anonymous_cart')


def report(request):
    """
    :param request: -
    :return: صفحه ی گزارش سایت
    """

    return render(request, 'staff/report.html')
