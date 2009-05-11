from django.db.models import get_model
from django.shortcuts import render_to_response
from django.template import RequestContext
from newsletters.forms import SubscriptionForm, SubscriptionOptInForm, UnsubscriptionForm, UnsubscriptionOptInForm

def subscribe(request, form_class=SubscriptionForm,
              template_name='newsletters/subscribe.html',
              success_template='newsletters/subscribe_success.html'):
    
    form = form_class()
    
    if request.POST:
        form = form_class(request.POST)
        
        if form.is_valid():
            instance = form.save()
            return render_to_response(success_template, locals(), RequestContext(request))
    
    return render_to_response(template_name, locals(), RequestContext(request))

def subscribe_optin(request, form_class=SubscriptionOptInForm,
              model_str="newsletters.SubscriptionOptIn",
              template_name='newsletters/subscribe.html',
              success_template='newsletters/subscribe_success.html',
              email_template='newsletters/opt-in.html',
              send_email=True):
    
    form = form_class()
              
    if request.POST:
        form = form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                model = get_model(*model_str.split('.'))
                model._default_manager.create_inactive_subscription(instance, email_template=email_template, send_email=send_email)
            except model.DoesNotExist:
                pass
            return render_to_response(success_template, locals(), RequestContext(request))
    
    return render_to_response(template_name, locals(), RequestContext(request))

def unsubscribe(request, form_class=UnsubscriptionForm,
              template_name='newsletters/unsubscribe.html',
              success_template='newsletters/unsubscribe_success.html'):

    form = form_class()
    
    if request.POST:
        form = form_class(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.delete()
            return render_to_response(success_template, locals(), RequestContext(request))
    
    return render_to_response(template_name, locals(), RequestContext(request))

def unsubscribe_optin(request, form_class=UnsubscriptionOptInForm,
              model_str="newsletters.SubscriptionOptIn",
              template_name='newsletters/unsubscribe.html',
              success_template='newsletters/unsubscribe_success.html',
              email_template='newsletters/opt-out.html',
              send_email=True):
    
    form = form_class()
    
    if request.POST:
        form = form_class(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            try:
                model = get_model(*model_str.split('.'))
                model._default_manager.deactivate_subscription(instance, email_template=email_template, send_email=send_email)
            except model.DoesNotExist:
                pass
                
            return render_to_response(success_template, locals(), RequestContext(request))
    
    return render_to_response(template_name, locals(), RequestContext(request))

def activate(request, activation_key, model_str="newsletters.SubscriptionOptIn",
             success_template='newsletters/opt-in_success.html',
             error_template='newsletters/opt-in_error.html'):
    
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    
    try:
        model = get_model(*model_str.split('.')) 
        if not model._default_manager.activate_subscription(activation_key):
            return render_to_response(error_template, locals(), RequestContext(request))
    except model.DoesNotExist: 
        return render_to_response(error_template, locals(), RequestContext(request))
    
    return render_to_response(success_template, locals(), RequestContext(request))
    
def deactivate(request, deactivation_key, model_str="newsletters.SubscriptionOptIn",
             success_template='newsletters/opt-out_success.html',
             error_template='newsletters/opt-out_error.html'):

    deactivation_key = deactivation_key.lower() # Normalize before trying anything with it.

    try:
        model = get_model(*model_str.split('.')) 
        if not model._default_manager.delete_subscription(deactivation_key):
            return render_to_response(error_template, locals(), RequestContext(request))
    except model.DoesNotExist:
        return render_to_response(error_template, locals(), RequestContext(request))

    return render_to_response(success_template, locals(), RequestContext(request))