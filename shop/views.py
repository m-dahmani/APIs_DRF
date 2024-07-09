from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView


class CategoryAPIView(APIView):

    def get(self, *args, **kwargs):
        categories = Category.objects.all()  # Récupérer toutes les catégories en utilisant l’ORM de Django
        # many => permet de générer une liste d’éléments à partir de l’itérable (notre queryset) qui lui est transmis
        serializer = CategorySerializer(categories, many=True)  # Sérialiser les données à l’aide de notre serializer
        # print(serializer.data)
        return Response(serializer.data)  # Renvoyer une réponse qui contient les données sérialisées


# # Vue basée sur les fonctions
# @api_view(['GET'])
# def category_list(request):
#     print('La méthode de requête est : ', request.method)
#     print('Les données POST sont : ', request.POST)
#
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     # print(serializer.data)
#     return JsonResponse(serializer.data, safe=False)


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
