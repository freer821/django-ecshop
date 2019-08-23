from oscar.config import Shop
from django.urls import path
from .views import home
from apps.catalogue.views import *

class HomeShop(Shop):
    label = 'home'
    name = 'apps.home'

    # Override the get_urls method to remove the URL configuration for the
    # dashboard app
    def get_urls(self):
        urls = super().get_urls()
        for urlpattern in urls[:]:
            if hasattr(urlpattern, 'name') and (urlpattern.name == 'home'):
                urls.remove(urlpattern)
                urls.append(path('', home))

        urls.append(path('brands', brands))

        return self.post_process_urls(urls)