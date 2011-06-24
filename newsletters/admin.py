# -*- coding: utf-8 -*-
from datetime import datetime
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from newsletters.forms import NewsletterForm
from newsletters.models import Subscription, Newsletter
from django.utils.translation import ugettext_lazy as _


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

        if request.method == 'POST':
            object.sent_date = datetime.now()
            object.save()
            self.message_user(request, _(u"Newsletter sent successfully"))
            return HttpResponseRedirect(reverse('admin:newsletters_newsletter_changelist'))
        subscribers = Subscription.objects.filter(subscribed=True)
        opts = Newsletter._meta
        app_label = opts.app_label



        return render_to_response('admin/newsletters/send_mail.html',
                                  locals(),
                                  RequestContext(request))

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Subscription, SubscriptionAdmin)