from django.contrib import admin
from django.urls import path, include
# from shop.views import CategoryAPIView
# from shop.views import category_list
# from shop.views import CategoryList
# from shop.views import ProductList
from rest_framework import routers
from shop.views import CategoryViewset, ProductViewset, ArticleViewset, \
    AdminCategoryViewset, AdminArticleViewset #transform ApiView & ListAPIView into a ModelViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Here we create our router
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view afin que l’url générée soit celle que
# nous souhaitons ‘/api/category/’
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('article', ArticleViewset, basename='article')
router.register('admin/category', AdminCategoryViewset, basename='admin-category')
router.register('admin/article', AdminArticleViewset, basename='admin-article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),  # Remember to add the router URLs to the list of URLs
    # path('api/category/', CategoryAPIView.as_view()),
    # path('api/product/', ProductList.as_view(), name='product_list'),  # For the class-based view with generic views
    # path('category/list/', category_list, name='category_list'),     # For function based view
    # path('category/list/', CategoryList.as_view(), name='category_list'), # For class-based view with generic views
]