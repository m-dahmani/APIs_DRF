from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product


class ShopAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Let's create two categories of which only one is active
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        cls.product = cls.category.products.create(name='Ananas', active=True)
        cls.category.products.create(name='Banane', active=False)

        cls.category_2 = Category.objects.create(name='Légumes', active=True)
        cls.product_2 = cls.category_2.products.create(name='Tomate', active=True)

    def format_datetime(self, value):
        # Format DateTime Helper
        # a helper allowing you to format a date as a character string in the same format as that of the API
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestCategory(ShopAPITestCase):
    # We store the endpoint URL in a class attribute to be able to use it more easily in each of our tests
    url = reverse_lazy('category-list')
    
    def test_list(self):
        # We make the GET call using the client of the test class
        response = self.client.get(self.url)
        # We check that the status code is indeed 200
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                'id': category.id,
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            } for category in [self.category, self.category_2]
        ]
        # the values returned are those expected
        self.assertEqual(response.json(), expected)

    def test_create(self):
        category_count = Category.objects.count()
        # We check that no category exists before attempting to create one
        # self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        # Let's check that the status code is in error and prevents us from creating a category
        self.assertEqual(response.status_code, 405)
        # let's check that no new category has been created despite the status code 405
        self.assertEqual(Category.objects.count(), category_count)


class TestProduct(ShopAPITestCase):

    url = reverse_lazy('product-list')

    def get_product_detail_data(self, products):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id
            } for product in products
        ]

    def test_list(self):
        """Vérifie que la liste des produits actifs est retournée correctement."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_detail_data([self.product, self.product_2]), response.json())

    def test_list_filter(self):
        response = self.client.get(self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_detail_data([self.product]), response.json())

    def test_create_not_allowed(self):
        """Vérifie qu'on ne peut pas créer un produit via l'API."""
        product_count = Product.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Product.objects.count(), product_count)

    def test_update_not_allowed(self):
        """Vérifie qu'on ne peut pas mettre à jour un produit via l'API."""
        response = self.client.put(reverse('product-detail', args=[self.product.id]), {'name': 'Updated Apple'})
        self.assertEqual(response.status_code, 405)

    def test_delete_not_allowed(self):
        """Vérifie qu'on ne peut pas supprimer un produit via l'API."""
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()




























