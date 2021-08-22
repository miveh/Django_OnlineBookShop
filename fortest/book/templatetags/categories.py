from django import template

from book.models import Category

register = template.Library()


@register.simple_tag()
def categry_books_qs():
    categories_tag = Category.objects.exclude(book__isnull=True)
    print(categories_tag)
    print('huiyudsdfghjkl')
    # return {'categories_tag': categories_tag, 'r': 4}
    return categories_tag
