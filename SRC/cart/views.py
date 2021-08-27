from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from book.models import Book
from cart.models import CartItems, Cart


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


@login_required
def add_to_cart(request, slug):
    """
    :param request: 😐
    :param slug: اسلاگ کتاب انتخاب شده
    :return: سرجاش میمونه
    """

    book = get_object_or_404(Book, slug=slug)
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


def add_to_next_cart(request, slug):
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
