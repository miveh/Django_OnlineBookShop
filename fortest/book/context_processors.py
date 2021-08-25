def categories(request):
    """
    :return: تمامی دسته بندی هایی که شامل کتاب هستند - تمامی کتابها - 4 تا کتاب با بیشترین قیمت
    """

    from book.models import Category, Book
    return {
                'categories_books': Category.objects.exclude(book__isnull=True),
                'books': Book.objects.filter(stock__gt=0)[:4],
            }
