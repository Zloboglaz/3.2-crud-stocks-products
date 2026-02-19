from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        queryset = Stock.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            # Ищем склады, где есть продукт с именем, содержащим search_query
            queryset = queryset.filter(positions__product__title__icontains=search_query).distinct()
        return queryset
