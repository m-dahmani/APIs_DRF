import requests
from django.db import models, transaction


class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @transaction.atomic  # in case of error, we would then return to the previous state
    def disable(self):
        if self.active is False:
            # Let's do nothing if the category is already disabled
            return
        self.active = False
        self.save()
        # let's deactivate products in this category
        self.products.update(active=False)

    @transaction.atomic
    def enable(self):
        """The enable method will check if the category is inactive,
        then enable the category and all associated products."""
        if self.active:
            # Debug
            print(f"Category '{self.name}' is already enabled.")
            return
        # Debug
        print(f"Enabling category '{self.name}'")
        self.active = True
        self.save()
        self.products.update(active=True)


class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    @transaction.atomic
    def disable(self):
        if not self.active:
            return
        self.active = False
        self.save()
        self.articles.update(active=False)

    def call_external_api(self, method, url):  # Call an external API This method will be monkey patched
        return requests.request(method, url)

    @property
    # property that calls the API and returns the ecoscore
    def ecoscore(self):
        # call for open food fact
        url = 'https://world.openfoodfacts.org/api/v0/product/3229820787015.json'
        response = self.call_external_api('GET', url)
        if response.status_code == 200:
            # return the ecoscore if the response is valid
            return response.json()['product']['ecoscore_grade']


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name
