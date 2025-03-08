from django.urls import path
from .views import *

# app_name = 'scraper'

urlpatterns = [
    path('scrape/', scrape_amazon, name='scrape'),
    path('compare_price/', compare_price, name='compare_price'),
    path('productDetails/', product, name='productDetails'),
    path('push_data/', push_product, name='push_data'),
    path('submit/', submit, name="submit"),
    path('', home, name='home'),
]
