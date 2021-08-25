from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from BOOK_STORE import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^jet/', include('jet.urls', 'jet')),
    path('accounts/', include('account.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('book.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('book.urls')),
#     path('', include('coupon.urls')),
#     path('', include('cart.urls')),
#     path('', include('zahra.urls')),
# ]
