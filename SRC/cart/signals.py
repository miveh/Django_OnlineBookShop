from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import CustomUser
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
    device = request.COOKIES['device']
    print(device)
    try:
        authenticated_user = request.user
        print(authenticated_user.email)
        anonymous_user = CustomUser.objects.filter(device=device, is_anonymous_user=True)[0]
        print('is anonumous user:'+ anonymous_user.email)
        if anonymous_user:
            anonymous_cart_items = CartItems.objects.filter(cart=Cart.objects.get(user__id=anonymous_user.id))
            print(anonymous_cart_items)
            if anonymous_cart_items.exists():

                for cart_item in anonymous_cart_items:
                    authenticated_user_cart = Cart.objects.get(user__id=authenticated_user.id)
                    print(authenticated_user_cart.id)
                    cart_item.cart = authenticated_user_cart
                    cart_item.save()

            anonymous_user.delete()
    except:
        pass


user_logged_in.connect(post_login)
"""
بیاد چک کنه دیوایس این کاربر لاگین شده با کاربر دیگه ای برابره یا نه که ایز ان انی موسش ترو باشه اگر بود 
اگر بود ایتم های های سبد اون ان انی موس رو بگیره و کارتشو با کارت کاربر لاگین شده جا به جا کنه 
بعد اون کاربر ان انی موس شده رو پاک کنه 
"""
