# -*- coding: utf-8 -*-
from datetime import datetime
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from newsletters.forms import NewsletterForm
from newsletters.models import Subscription, Newsletter
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class  SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed')



class NewsletterAdmin(admin.ModelAdmin):
    form = NewsletterForm
    list_display = ('title', 'sent_date')
    prepopulated_fields = {'slug': ('title',)}



    def get_urls(self):
        urls = super(NewsletterAdmin, self).get_urls()

        info = self.admin_site.name, self.model._meta.app_label, self.model._meta.module_name
        my_urls = patterns('',
            url(r'^(?P<newsletter_id>\d+)/send_mail/$',
             self.send_mail,
             name = '%s:%s_%s_sendmail' % info),

        )
        return my_urls + urls


    def send_mail(self, request, newsletter_id):
        object = Newsletter.objects.get(id=newsletter_id)

        subscribers = Subscription.objects.filter(subscribed=True)

        site = Site.objects.get_current()
        template = render_to_string(object.template, locals(), RequestContext(request))

        if request.method == 'POST':
            object.sent_date = datetime.now()
            object.save()
            email = EmailMessage(subject = '%s - %s' % (object.title, site),
                                 body = template,
                                 from_email = settings.NEWSLETTER_FROM_EMAIL,
                                 bcc = [e.email for e in subscribers],
                                 headers = {'Reply-To': settings.NEWSLETTER_REPLYTO_EMAIL}
            )
            email.content_subtype = "html"  # Main content is now text/html
            email.send()
            self.message_user(request, _(u"Newsletter sent successfully"))

            return HttpResponseRedirect(reverse('admin:newsletters_newsletter_changelist'))
        opts = Newsletter._meta
        app_label = opts.app_label



        return render_to_response('admin/newsletters/send_mail.html',
                                  locals(),
                                  RequestContext(request))

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Subscription, SubscriptionAdmin)