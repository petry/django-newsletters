from django import forms
from newsletters.models import Subscription, SubscriptionOptIn
from django.utils.translation import ugettext_lazy as _

class SubscriptionForm(forms.ModelForm):
    
    def clean_email(self):
        try:
            self._meta.model._default_manager.get(email=self.cleaned_data['email'])
            raise forms.ValidationError(_('E-mail already registered'))
        except self._meta.model.DoesNotExist:
            pass
        return self.cleaned_data['email']
    
    class Meta:
        model = Subscription
        fields = ('email',)

class SubscriptionOptInForm(SubscriptionForm):
    
    class Meta:
        model = SubscriptionOptIn
        fields = ('email',)
        
class UnsubscriptionForm(forms.ModelForm):

    def clean_email(self):
        try:
            self._meta.model._default_manager.get(email=self.cleaned_data['email'])
        except self._meta.model.DoesNotExist:
            raise forms.ValidationError(_('E-mail not found'))
        return self.cleaned_data['email']
    
    def save(self, commit=True):
        try:
            params = dict(self.cleaned_data.items())
            self.instance = self._meta.model._default_manager.get(**params)
        except:
            raise forms.ValidationError(_('E-mail not registered'))

        return super(UnsubscriptionForm, self).save(commit=commit)
    
    class Meta:
        model = Subscription
        fields = ('email',)

class UnsubscriptionOptInForm(UnsubscriptionForm):
    
    class Meta:
        model = SubscriptionOptIn
        fields = ('email',)