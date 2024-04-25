from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from accounts.models import Customer, Order, Product
from accounts.views import home, createOrder, deleteOrder

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('user-page')
        self.home_url_admin = reverse('home')

        # Create a user and a group
        
        self.group_customer = Group.objects.create(name='customer')
        self.group_admin = Group.objects.create(name='admin')
        
        self.user = User.objects.create_user(username='Admin', password='table123456')
        self.user_admin = User.objects.create_user(username='Admin_user', password='table123456')

        self.user.groups.add(self.group_customer)
        self.user_admin.groups.add(self.group_admin)

        
        
        self.user.save()
        

        # Create mock data for Customer and Order
        self.customer = Customer.objects.create(user=self.user,name='John Doe', email='john@example.com')
        self.product_instance = Product.objects.create(name="oil",category='Indoor')
        self.order = Order.objects.create(customer=self.customer, product=self.product_instance, status='Pending')
        self.create_order_url = reverse('createOrder_user', args=[self.customer.id])  # '1' is a string as per your URL config
        self.delete_order_url = reverse('delete_order', args=[self.customer.id])  # '1' is a string as per your URL config

    def test_home_GET(self):
        self.client.login(username='Admin', password='table123456')
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user.html')
        
    def test_home_admin_GET(self):
        self.client.login(username='Admin_user', password='table123456')
        response = self.client.get(self.home_url_admin)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')

    def test_create_order_GET(self):
        self.client.login(username='Admin', password='table123456')
        response = self.client.get(self.create_order_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/order_form.html')

    def test_create_order_POST_adds_new_order(self):
        self.client.login(username='Admin', password='table123456')
        
        # Prepare data for one form in the formset
        data = {
            'order_set-TOTAL_FORMS': '1',  # Indicates how many forms in the formset
            'order_set-INITIAL_FORMS': '0',  # Initial number of forms
            'order_set-MIN_NUM_FORMS': '0',  # Minimum number of forms required
            'order_set-0-product': self.product_instance.id,  # Use the product id
            'order_set-0-delivery_address': '123 Test St',
            'order_set-0-delivery_date': '2023-10-01',
            'order_set-0-price': '49.99',
        }
        
        # Post data to the view
        print("Orders before POST:", Order.objects.count())
        response = self.client.post(self.create_order_url, data)
        print("Orders after POST:", Order.objects.count(), list(Order.objects.values()))
        # Check response
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful form submission
        self.assertEqual(Order.objects.count(), 2)  # Check that an Order has been created
        new_order = Order.objects.get(id=2)
  
        self.assertEqual(new_order.product, self.product_instance)
        self.assertEqual(new_order.delivery_address, '123 Test St')

    # def test_delete_order_POST(self):
    #     self.client.login(username='Admin', password='table123456')
    #     response = self.client.post(self.delete_order_url)

    #     self.assertEquals(response.status_code, 302)  # redirect to home
    #     self.assertEquals(Order.objects.filter(id=1).count(), 0)

    def test_home_no_access_without_login(self):
        response = self.client.get(self.home_url)
        self.assertNotEqual(response.status_code, 200)  # 302 or 403 expected

# Add more tests as needed for other scenarios and views
