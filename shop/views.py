from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from shop.models import Category, Product, Article
from shop.serializers import CategoryListSerializer, CategoryDetailSerializer, ProductListSerializer, ProductDetailSerializer, ArticleSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet


# class CategoryAPIView(APIView):
#
#     def get(self, *args, **kwargs):
#         categories = Category.objects.all()   # Retrieve all categories using Django ORM
#         # many => permet de générer une liste d’éléments à partir de l’itérable (notre queryset) qui lui est transmis
#         serializer = CategorySerializer(categories, many=True)   # Serialize the data using our serializer
#         # print(serializer.data)
#         return Response(serializer.data)   # Return a response that contains the serialized data


# transform ApiView into a ModelViewset
# class CategoryViewset(ModelViewSet):
#     serializer_class = CategorySerializer
#     Redefining the queryset class attribute mainly allows for quick testing.
#     # queryset = Category.objects.all()
#
#     def get_queryset(self):
#         redefine get_queryset is the solution to adopt it allows you to be more precise on the elements to return
#         return Category.objects.all()
#

class MultipleSerializerMixin:
    """Create and use a Mixin. This is to allow us to share the code which allows us to define the serializer
    to use according to the list and the details. This will avoid rewriting code and make maintenance easier."""

    detail_serializer_class = None

    def get_serializer_class(self):
        # If the requested action is retrieve we return the detail serializer
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


# transform ApiView into a ReadOnlyModelViewset
class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    # Let's add a class attribute that allows us to define our detail serialize
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        # Apply a filter on only active categories
        # Le warning concernant la pagination peut être résolu en spécifiant un ordre explicite dans votre queryset :
        # Cela garantit que les résultats paginés sont renvoyés dans un ordre cohérent.
        return Category.objects.filter(active=True).order_by('id')
        # return Category.objects.all() # pour activer les categories via def enable il faut apply all categories

    # Create and use a Mixin instead
    # def get_serializer_class(self):
    #     # If the requested action is retrieve we return the detail serializer
    #     if self.action == 'retrieve':
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()

    @action(detail=True, methods=['post'])  # We defined our accessible action on the POST method only
    # it concerns the detail because it allows you to deactivate a category
    def disable(self, request, pk):
        # We can call the disable method
        self.get_object().disable()
        # Return a response (status_code=200 by default) to indicate the success of the action
        return Response()

    @action(detail=True, methods=['post'])
    def enable(self, request, pk=None):
        category = self.get_object()
        # Debug
        print(f"Enable action called for category ID: {pk}")
        category.enable()
        return Response({"status": "category and associated products enabled"})


# Function based view
# @api_view(['GET'])
# def category_list(request):
#     print('La méthode de requête est : ', request.method)
#     print('Les données POST sont : ', request.POST)
#
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     # print(serializer.data)
#     return JsonResponse(serializer.data, safe=False)


# transform ListAPIView into a ReadOnlyModelViewset
# class ProductList(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# transform ListAPIView into a ReadOnlyModelViewset
class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        # We retrieve all active products in a variable named queryset
        # queryset = Product.objects.filter(active=True)
        # add a parameter to include unavailable categories
        include_inactive = self.request.GET.get('include_inactive')
        # Let's check the presence of the 'category_id' parameter in the url and if yes then apply our filter
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        # force display of inactive products
        if include_inactive is not None:
            if include_inactive.lower() == 'true':
                queryset = queryset.filter(active=False)
        else:
            queryset = queryset.filter(active=True).order_by('id')

        return queryset

    # Create and use a Mixin instead
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response({"status": "product and associated articles disabled"})


class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
