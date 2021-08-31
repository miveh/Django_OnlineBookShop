from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect

from account.models import CustomUser
from book.models import Book
from cart.models import Cart, CartItems


@receiver(post_save, sender=CustomUser)
def create_user_cart(sender, instance, created, **kwargs):
    """
    :param sender: کاربر جدید
    :param instance: ابجکت از کاربر
    :param created: وقتی ساخته شد
    :param kwargs: -
    :return: یک سبد خرید برای هر کاربر
    """

    if created:
        Cart.objects.create(user=instance)


# @receiver(post_save, sender=CustomUser)
# def save_user_cart(sender, instance, **kwargs):
#     instance.cart.save()


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    print('horaaaaaaaa inja signal')
    book_obj_list = []

    try:
        book_list = request.session['books']
        for book_name in book_list:
            book_obj_qs = Book.objects.filter(name=book_name)
            if book_obj_qs.exists():
                book_obj = book_obj_qs[0]
                cart_qs = CartItems.objects.filter(book=book_obj, ordered='O', cart=Cart.objects.get(user=request.user))
                if cart_qs.exists():
                    cart_item = cart_qs[0]
                    if cart_item.book.stock <= cart_item.quantity:
                        pass
                    else:
                        cart_item.quantity += 1
                        cart_item.save()
                else:
                    cart_item = CartItems.objects.create(book=book_obj, ordered='O',
                                                         cart=Cart.objects.get(user=request.user))
                    cart_item.save()
            else:
                pass
            book_list.remove(book_name)
    except:
        pass


user_logged_in.connect(post_login)
"""
بیاد چک کنه دیوایس این کاربر لاگین شده با کاربر دیگه ای برابره یا نه که ایز ان انی موسش ترو باشه اگر بود 
اگر بود ایتم های های سبد اون ان انی موس رو بگیره و کارتشو با کارت کاربر لاگین شده جا به جا کنه 
بعد اون کاربر ان انی موس شده رو پاک کنه 
"""
