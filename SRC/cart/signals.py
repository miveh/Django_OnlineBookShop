from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import CustomUser
from cart.models import Cart


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
