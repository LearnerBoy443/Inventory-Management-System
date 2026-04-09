from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import csv

from .models import User, Category, Product, Transaction
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, TransactionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.save()
        Transaction.objects.create(
            product=product, 
            user=self.request.user, 
            type='IN', 
            quantity=product.stock
        )

    def perform_update(self, serializer):
        old_stock = self.get_object().stock
        product = serializer.save()
        new_stock = product.stock
        
        diff = new_stock - old_stock
        if diff != 0:
            trans_type = 'IN' if diff > 0 else 'OUT'
            Transaction.objects.create(
                product=product,
                user=self.request.user,
                type=trans_type,
                quantity=abs(diff)
            )

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        products = Product.objects.all()
        total_products = products.count()
        low_stock = sum(1 for p in products if p.stock < 10)
        inventory_value = sum(p.stock * p.price for p in products)
        
        return Response({
            'total_products': total_products,
            'low_stock': low_stock,
            'inventory_value': inventory_value
        })

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Stock', 'Price'])
        
        for product in Product.objects.all().values_list('id', 'name', 'stock', 'price'):
            writer.writerow(product)
            
        return response

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
