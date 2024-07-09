from django.contrib import admin
from django.urls import path, include
from shop.views import CategoryAPIView
# from shop.views import category_list
# from shop.views import CategoryList
from shop.views import ProductList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/category/', CategoryAPIView.as_view()),
    path('api/product/', ProductList.as_view(), name='product_list'),  # Pour la vue basée sur les classes with
    # generic views
    # path('category/list/', category_list, name='category_list'),            # Pour la vue basée sur les fonctions
    # path('category/list/', CategoryList.as_view(), name='category_list'),   # Pour la vue basée sur les classes with
]

