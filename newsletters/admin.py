# -*- coding: utf-8 -*-
from django.contrib import admin
from newsletters.forms import NewsletterForm
from newsletters.models import Subscription, Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    form = NewsletterForm

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Subscription)