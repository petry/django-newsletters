from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from newsletters.models import Subscription

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
        response = self.client.get(reverse('subscription-activate',
                                        kwargs={'activation_key':000}))
        self.assertEqual(response.status_code, 200)


    def test_subscription_deactivate_view_works(self):
        response = self.client.get(reverse('subscription-deactivate',
                                           kwargs={'deactivation_key':000}))
        self.assertEqual(response.status_code, 200)


class SubscriptionTest(TestCase):
    def setUp(self):
        self.client = Client()


    def test_subscription_add_an_email(self):
        self.assertEqual(Subscription.objects.count(), 0)

        response = self.client.post(reverse('subscribe'),
                                    data={'email':'test@test.com'})
        self.assertEqual(Subscription.objects.count(), 1)


    def test_unsubscription_remove_email(self):
        Subscription.objects.create(email="test@test.com")

        response = self.client.post(reverse('unsubscribe'),
                                    data={'email':'test@test.com'})

        self.assertEqual(Subscription.objects.count(), 0)


    def test_only_one_email_are_bubscribed(self):
        Subscription.objects.create(email="test@test.com")
        response = self.client.post(reverse('subscribe'),
                                        data={'email':'test@test.com'})
        form = response.context['form']
        self.assertEqual(form.errors['email'], [u'E-mail already registered'])

