from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from newsletters import settings
import random, re, sha, datetime

class SubscriptionBaseSubscribedManager(models.Manager):
    def get_query_set(self):
        return super(SubscriptionBaseSubscribedManager, self).get_query_set().filter(subscribed=1)

class SubscriptionBase(models.Model):
    '''
    Abstract base class for newsletter subsription.
    
    This class 
    '''
    email = models.EmailField(_('email'))
    subscribed = models.BooleanField(_('subscribed'), default=True)
    date_joined = models.DateTimeField(_("created on"), auto_now_add=True)
    
    objects = models.Manager()
    active = SubscriptionBaseSubscribedManager()
    
    class Meta:
        abstract = True
    
    @classmethod
    def is_active(cls, email):
        try:
            return cls.objects.get(email=email).subscribed
        except cls.DoestNotExist, e:
            return False
         
    def __unicode__(self):
        return u'%s' % (self.email)


SHA1_RE = re.compile('^[a-f0-9]{16}$')
class SubscriptionOptInMananger(models.Manager):
    """
    Custom manager for the SubscriptionOptIn model.

    The methods defined here provide shortcuts for subscription creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired subscription accounts.
    """
    def activate_subscription(self, activation_key):
        """
        Validates an activation key and activates the corresponding
        Subscription if valid.

        If the key is valid and has not expired, returns the Subscription
        instance after activating.

        If the key is not valid or has expired, returns False.

        If the key is valid but the Subscription is already active,
        returns the Subscription instance.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                subscription = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not subscription.activation_key_expired():
                subscription.subscribed = True
                subscription.save()
                return subscription
        return False
    
    def create_inactive_subscription(self, instance, email_template='newsletters/opt-in.html', send_email=True):
        """
        Creates a new, inactive Subscription, generates a
        Subscription and emails its activation key to the
        user. Returns the new Subscription.

        To disable the email, call with send_email=False.
        """
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+instance.email).hexdigest()[:16]
        
        instance.activation_key = activation_key
        instance.subscribed = False
        instance.save()
        
        if send_email:
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            from django.contrib.sites.models import Site
            
            current_site = Site.objects.get_current()

            subject = ugettext('Confirm your subscription to %s' % (current_site.name))

            message = render_to_string(email_template,
                                       { 'activation_key': instance.activation_key,
                                         'expiration_days': settings.NEWSLETTER_ACTIVATION_DAYS,
                                         'site': current_site,
                                         'user': instance,
                                         'email': instance.email 
                                        })

            send_mail(subject, message, settings.NEWSLETTER_FROM_EMAIL, [instance.email], fail_silently=True)
        return instance
    
    def delete_subscription(self, deactivation_key):
        """
        Delete the corresponding Subscription if key is valid.

        If the key is valid and has not expired, returns True.

        If the key is not valid or has expired, returns False.

        If the key is valid but the Subscription is already inactive,
        returns True.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(deactivation_key):
            try:
                print 
                subscription = self.get(activation_key=deactivation_key)
            except self.model.DoesNotExist:
                return False
            subscription.delete()
            return True
        return False
            
    def deactivate_subscription(self, instance, email_template='newsletters/opt-out.html', send_email=True):
        """
        emails its deactivation key to the user.
        Returns the Subscription.

        To disable the email, call with send_email=False.
        """
        salt = sha.new(str(random.random())).hexdigest()[:5]
        deactivation_key = sha.new(salt+instance.email).hexdigest()[:16]
        
        instance.activation_key = deactivation_key
        instance.save()
        
        if send_email:
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            from django.contrib.sites.models import Site

            current_site = Site.objects.get_current()

            subject = ugettext('Confirm your unsubscription to %s' % (current_site.name))

            message = render_to_string(email_template,
                                       { 'deactivation_key': instance.activation_key,
                                         'site': current_site,
                                         'user': instance,
                                         'email': instance.email
                                        })

            send_mail(subject, message, settings.NEWSLETTER_FROM_EMAIL, [instance.email], fail_silently=True)
        return instance

    def delete_expired_subscriptions(self):
        """
        Removes expired instances of Subscription.

        Subscriptions to be deleted are identified by searching for
        instances with expired activation keys, and then checking to 
        see if they the field is_active set to False; any
        Subscription who is both inactive and has an expired activation
        key will be deleted.

        It is recommended that this method be executed regularly as
        part of your routine site maintenance; the file
        bin/delete_expired_users.py in this application provides a
        standalone script, suitable for use as a cron job, which will
        call this method.

        Regularly clearing out subscriptions which have never been
        activated serves two useful purposes:

        1. It alleviates the ocasional need to reset a
           Subscription and/or re-send an activation email
           when a subscription does not receive or does not act upon the
           initial activation email; since the subscription will be
           deleted, the subscription will be able to simply re-register and
           receive a new activation key.

        2. It prevents the possibility of a malicious user registering
           one or more emails and never activating them (thus
           denying the use of those emails to anyone else); since
           those subscription will be deleted, the emails will become
           available for use again.
        """
        for subscription in self.all():
            if subscription.activation_key_expired():
                if not subscription.subscribed:
                    subscription.delete()

class SubscriptionOptInBase(SubscriptionBase):
    '''
    Abstract base class for Opt-in/Opt-out subscription newsletter
    '''
    activation_key = models.CharField(_('activation key'), max_length=16)
    
    objects = SubscriptionOptInMananger()
    
    class Meta:
        abstract = True
    
    def activation_key_expired(self):
        """
        Determines whether this Subscription's activation
        key has expired.

        Returns True if the key has expired, False otherwise.

        Key expiration is determined by the setting
        NEWSLETTER_ACTIVATION_DAYS, which should be the number of
        days a key should remain valid after a subscription is registered.
        """
        expiration_date = datetime.timedelta(days=settings.NEWSLETTER_ACTIVATION_DAYS)
        return self.date_joined + expiration_date <= datetime.datetime.now()

class Subscription(SubscriptionBase):
    '''
    Generic subscription
    '''
    pass

class SubscriptionOptIn(SubscriptionOptInBase):
    '''
    Generic opt-in subscription
    '''
    pass