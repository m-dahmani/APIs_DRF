from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer
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
#        # redéfinir get_queryset est la solution à adopter car elle permet d’être plus fin sur les éléments à retourner
#         return Category.objects.all()
#

# transform ApiView into a ReadOnlyModelViewset
class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


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
class ProductViewset(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
