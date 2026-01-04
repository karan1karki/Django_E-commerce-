from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class TimestampedModel(models.Model):
    """
    Abstract base class demonstrating INHERITANCE and REUSE
    Provides common timestamp fields for all models that inherit from it
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # ← This is key - abstract base class (OOP Inheritance + Abstraction)


class Category(TimestampedModel):
    """Product category - simple hierarchical possibility later"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    # Simple business rule encapsulation
    def get_product_count(self):
        return self.products.count()


class Product(TimestampedModel):
    """
    Main product entity
    Demonstrates ENCAPSULATION (business logic inside model)
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.category})"

    # Encapsulated business logic
    @property
    def is_in_stock(self):
        """Abstraction of stock checking logic"""
        return self.stock > 0 and self.available

    def reduce_stock(self, quantity):
        """Encapsulated stock management"""
        if quantity > self.stock:
            raise ValueError(f"Not enough stock. Only {self.stock} available.")
        self.stock -= quantity
        self.save(update_fields=['stock'])


class Order(TimestampedModel):
    """Order - main purchase record"""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_address = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    # Business logic encapsulation
    def calculate_total(self):
        """Calculate total from order items"""
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])
        return total

    def update_status(self, new_status):
        """Simple state transition (could be expanded with validation)"""
        self.status = new_status
        self.save(update_fields=['status'])


class OrderItem(TimestampedModel):
    """Individual product in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of purchase

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    @property
    def subtotal(self):
        """Encapsulated price calculation"""
        return self.quantity * self.price