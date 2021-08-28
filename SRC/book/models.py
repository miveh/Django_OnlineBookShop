import random
from django.db import models
from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    """
    ایجاد یک کلاس برای ساخت جدولی از دسته بندی کتابها
    """

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    category = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        هنگام ذخیره ی هر شی اسلاگ آن را بررسی و بهتر می کند.
        """
        to_slug = self.slug
        if to_slug == "":
            to_slug = slugify(str(self.category) + " " + "category")
            qs = Category.objects.filter(slug=to_slug).exists()
            while qs:
                to_slug = slugify(to_slug + " " + str(random.randint(1, 500)))
                qs = Category.objects.filter(slug=to_slug).exists()
        self.slug = to_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('categorydetail', kwargs={'slug': self.slug})


class Book(models.Model):
    """
    برای ساخت جدولی برای ذخیره ی کالا یا همان کتاب
    """

    class Meta:
        ordering = ('-price',)
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'

    name = models.CharField(verbose_name='نام', max_length=50, unique=True)
    image = models.ImageField(verbose_name='تصویر', default='product.png', upload_to='books/')
    author = models.CharField(verbose_name='نویسنده', max_length=50)
    price = models.DecimalField(verbose_name='قیمت به تومان', max_digits=8, decimal_places=2)
    created = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    stock = models.IntegerField(verbose_name='موجودی', default=1)
    description = models.CharField(verbose_name='درباره کتاب', max_length=500, default='بدون توضیحات')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        هنگام ذخیره ی هر شی اسلاگ آن را بررسی و بهتر می کند.
        """

        self.slug = slugify(self.name)
        book_slug = self.slug
        if book_slug == "":
            book_slug = slugify(str(self.name) + " " + "book")
            qs = Category.objects.filter(slug=book_slug).exists()
            while qs:
                book_slug = slugify(book_slug + " " + str(random.randint(1, 500)))
                qs = Category.objects.filter(slug=book_slug).exists()
        self.slug = book_slug
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """
        :return: قیمت نهایی هر کتاب پس از اعمال تمامی کد تخفیفهای درصدی و نقدی روی هر عنوان کتاب
        """

        total_cache_coupon = 0
        total_percent_coupon = 0

        cache_coupons_of_book_qs = self.bookcashcoupon_set.all()
        percent_coupons_of_book_qs = self.bookpercentcoupon_set.all()

        if cache_coupons_of_book_qs.exists():
            for cache_coupon in cache_coupons_of_book_qs:
                total_cache_coupon += cache_coupon.discount_price

        if percent_coupons_of_book_qs.exists():
            for percent_coupon in percent_coupons_of_book_qs:
                total_percent_coupon += percent_coupon.discount_percent

        self.price = float(self.price)
        self.price = int(self.price)
        book_total_price = ((self.price - total_cache_coupon) * (100 - total_percent_coupon)) / 100

        return book_total_price

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add_cart', kwargs={'slug': self.slug})
