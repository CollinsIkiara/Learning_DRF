from rest_framework import serializers
from .models import Product, Order, OrderItem, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock',
        )
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2
    )
    
    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal' # This is a property method in the OrderItem model that calculates the subtotal for each order item based on the product price and quantity.
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'date_joined'
        )

# The OrderSerializer implements nested serialization for the Order model, including related User and OrderItem data. It also calculates the total price of the order using a custom method.
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # many=True because a user can have multiple orders, and read_only=True because we don't want to allow the user to be modified through the order serializer.
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total') # SerializerMethodField is used to add a custom field to the serializer that is not directly tied to a model field.
    
    def total(self, obj):
        order_items = obj.items.all() # Get all order items for the order
        return sum(order_item.item_subtotal for order_item in order_items) # Calculate the total price by summing the item subtotals
    
    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price'
            )