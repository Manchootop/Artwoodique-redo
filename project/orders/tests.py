from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from django.utils import timezone
from project.main.models import Product
from project.orders.models import OrderItem, Order

UserModel = get_user_model()

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(email='testuser@gmail.com', password='password')
        self.product1 = Product.objects.create(title='Product 1', price=10.0)
        self.product2 = Product.objects.create(title='ALabala', price=15.0)
        self.order = Order.objects.create(user=self.user)
        self.order_item1 = OrderItem.objects.create(user=self.user, order=self.order, item=self.product1)
        self.order_item2 = OrderItem.objects.create(user=self.user, order=self.order, item=self.product2)

    def test_authenticated_user_cart_view(self):
        self.client.login(email='testuser@gmail.com', password='password')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')
        self.assertIn('tables', response.context)
        self.assertIn('total', response.context)
        self.assertEqual(len(response.context['tables']), 2)  # Assuming two items are in the cart

    def test_unauthenticated_user_cart_view(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')
        self.assertIn('tables', response.context)
        self.assertIn('total', response.context)
        self.assertEqual(len(response.context['tables']), 0)  # Assuming cart is empty for unauthenticated user

    def test_order_creation_for_authenticated_user(self):
        self.client.login(email='testuser@gmail.com', password='password')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(user=self.user, ordered_date__isnull=False).exists())

    def test_order_item_addition_to_order_for_authenticated_user(self):
        self.client.login(email='testuser@gmail.com', password='password')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Order.objects.filter(user=self.user, items__in=[self.order_item1, self.order_item2])), 1)

    def test_order_creation_for_unauthenticated_user(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.filter(user=self.user, ordered_date__isnull=False).exists())

    def test_order_item_addition_to_order_for_unauthenticated_user(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Order.objects.filter(user=self.user, items__in=[self.order_item1, self.order_item2])), 0)

    def tearDown(self):
        self.client.logout()
