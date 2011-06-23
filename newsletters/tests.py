from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from newsletters.models import Subscription, Newsletter

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


from newsletters.forms import NewsletterForm

class NewsletterFormTest(TestCase):
    def test_newsletter_with_invalid_template_dit_not_work(self):
        data = dict(
            title = 'fake-title',
            slug = 'fake-slug',
            template = 'fake-template',
            body = 'fake-body'
        )

        form = NewsletterForm(data)
        self.assertFalse(form.is_valid())


    def test_newsletter_with_valid_template_works(self):
        data = dict(
            title = 'fake-title',
            slug = 'fake-slug',
            template = 'newsletters/newsletter_template.html',
            body = 'fake-body'
        )

        form = NewsletterForm(data)
        self.assertTrue(form.is_valid(), form.errors)


class AdminViewsTests(TestCase):
    fixtures = ['test_auth.json']


    def setUp(self):
        self.newsletter = Newsletter.objects.create(
            title = 'fake-title',
            slug = 'fake-slug',
            template = 'newsletters/newsletter_template.html',
            body = 'fake-body'
        )
        self.client = Client()
        self.client.login(username='testclient', password='password')


    def test_change_view_has_send_button(self):
        view = reverse('admin:newsletters_newsletter_change', args=[self.newsletter.pk,])
        response = self.client.get(view)
        self.assertTrue('sendlink' in response.content)

    def test_send_mail_view_works(self):
        response = self.client.get('/admin/newsletters/newsletter/1/send_mail/')
        self.assertEquals(response.status_code, 200)

    def test_send_mail_view_has_nresletter_object(self):
        Subscription.objects.create(email="test@test.com")
        response = self.client.get('/admin/newsletters/newsletter/1/send_mail/')
        newsletter = response.context['object']
        self.assertEqual(newsletter.title, 'fake-title')

    def test_send_mail_view_has_subscribers_list(self):
        Subscription.objects.create(email="test@test.com")
        response = self.client.get('/admin/newsletters/newsletter/1/send_mail/')
        subscription_list = [s.email for s in response.context['subscribers']]
        self.assertTrue('test@test.com' in subscription_list)


    def test_redirect_to_list_on_post_send_mail_view(self):
        response = self.client.post('/admin/newsletters/newsletter/1/send_mail/',
                                    data={'action':'send_mail'})
        self.assertRedirects(response=response,
            expected_url=reverse('admin:newsletters_newsletter_changelist') )
