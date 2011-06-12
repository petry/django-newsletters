from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

class RequestTest(TestCase):
    def setUp(self):
        self.client = Client()


    def test_subscribe_view_works(self):
        response = self.client.get(reverse('subscribe'))
        self.assertEqual(response.status_code, 200)


    def test_subscription_optin_view_works(self):
        response = self.client.get(reverse('subscription-opt-in'))
        self.assertEqual(response.status_code, 200)


    def test_subscription_optout_view_works(self):
        response = self.client.get(reverse('unsubscription-opt-out'))
        self.assertEqual(response.status_code, 200)


    def test_subscription_activate_view_works(self):
        response = self.client.get(reverse('subscription-activate', kwargs={'activation_key':000}))
        self.assertEqual(response.status_code, 200)


    def test_subscription_deactivate_view_works(self):
        response = self.client.get(reverse('subscription-deactivate', kwargs={'deactivation_key':000}))
        self.assertEqual(response.status_code, 200)

    