from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from book.models import Book
from cart.models import CartItems, Cart


class CartView(ListView):
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
        queryset = queryset.get(user=self.request.user).cartitems_set.all()
        return queryset


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
