"""
Provides default settings for the newsletters application when the
project settings module does not contain the appropriate settings.
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Set NEWSLETTER_ACTIVATION_DAYS to the number of 
# days a key should remain valid after a subscription is registered.
NEWSLETTER_ACTIVATION_DAYS = getattr(settings, 'NEWSLETTER_ACTIVATION_DAYS', 5)

# Set NEWSLETTER_FROM_EMAIL is a valid email to be set as from in
# the newsletter email
NEWSLETTER_FROM_EMAIL = getattr(settings, 'NEWSLETTER_FROM_EMAIL', None)
if NEWSLETTER_FROM_EMAIL is None:
    raise ImproperlyConfigured('Please make sure you specified a NEWSLETTER_FROM_EMAIL setting.')