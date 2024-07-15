from rest_framework import serializers
from shop.models import Category, Product, Article


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # adding "description" to our list of fields
        fields = ['id', 'name', 'date_created', 'date_updated', 'description']

    # modify our list serializer because it is used for the create action
    def validate_name(self, value):
        """
        This method first checks if a category with the same name exists.
        Otherwise, it then checks if the name contains prohibited words from a predefined list.
        If a forbidden word is found, a ValidationError is raised.
        """
        # We check that the category exists
        if Category.objects.filter(name=value).exists():
            # In the event of an error, DRF provides us with the ValidationError exception
            raise serializers.ValidationError('Category already exists')

        # We could imagine a word filter system for a forum, for example
        # Added additional validations (like a banned word filter)
        # List of prohibited words
        forbidden_words = ["spam", "advertisement", "banned"]

        # Check if the name contains banned words
        for word in forbidden_words:
            if word in value.lower():
                raise serializers.ValidationError(f"The name contains a forbidden word: {word}")

        return value

    def validate(self, data):
        # Let's check that the name is present in the description
        if data['name'] not in data['description']:
            # Let's raise a ValidationError if this is not the cas
            raise serializers.ValidationError('Name must be in description')
        return data


class CategoryDetailSerializer(serializers.ModelSerializer):

    # define the related_name 'product' attribute by specifying a serializer set to 'many=True'
    # because there are multiple products for a category
    # to have more details on the products in the category do not display only the IDs
    # products = serializers.ProductSerializer(many=True)

    # Using a `SerializerMethodField', it is necessary to write a method named 'get_extra_info'
    # where extra_info is the name of the attribute, here 'products'
    products = serializers.SerializerMethodField()   # gives the possibility to filter the products to be returned

    class Meta:
        model = Category
        # add the list of IDs in an attribute with the same name as the related_name=='products'
        fields = ['id', 'name', 'date_created', 'date_updated', 'products']

    def get_products(self, obj):
        """Le paramètre 'obj' est l'instance de la catégorie consultée.
        Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a d'entités dans la liste
        Show only products that are active"""
        queryset = obj.products.filter(active=True)
        # The serializer is created with the queryset defined and always set as many=True
        serializer = ProductListSerializer(queryset, many=True)
        # the '.data' property is the rendering of our serializer that we return here
        return serializer.data  # Calculate some data to return.


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created', 'date_updated', 'category']


class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()  # gives the possibility to filter the articles to be returned

    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created', 'date_updated', 'category', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']

    def validate_price(self, value):
        # The price must be greater than 1€
        if value < 1:
            raise serializers.ValidationError("The price must be greater than 1€")
        return value

    def validate_product(self, value):
        # The associated product must be active.
        if not value.active:
            raise serializers.ValidationError('The associated product must be active')
        return value
