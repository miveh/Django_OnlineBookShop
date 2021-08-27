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
    cart_qs = CartItems.objects.filter(book=book, ordered='U',
                                       cart=Cart.objects.get(user=request.user))

    if cart_qs.exists():
        cart_item = cart_qs[0]
        if cart_item.book.stock <= cart_item.quantity:
            pass
        else:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item = CartItems.objects.create(book=book, ordered='U', cart=Cart.objects.get(user=request.user))
        cart_item.save()

    return redirect('book_detail', slug=slug)
