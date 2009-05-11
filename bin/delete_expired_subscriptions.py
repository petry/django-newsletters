#!/sw/bin/python
"""
A script which removes expired/inactive subscription from the
database.

This is intended to be run as a cron job; for example, to have it run
at midnight each Sunday, you could add lines like the following to
your crontab::

    DJANGO_SETTINGS_MODULE=yoursite.settings
    0 0 * * sun python /path/to/newsletter/bin/delete_expired_subscriptions.py

See the method ``delete_expired_subscriptions`` of the ``SubscriptionOptInMananger``
class in ``newsletters/models.py`` for further documentation.

"""
import sys, os
from optparse import OptionParser, OptionValueError

def delete_expired_subscriptions(parser):
    if parser.values.model_str:
        from django.db.models import get_model
        model = get_model(*parser.values.model_str.split('.')) 
        model._default_manager.delete_expired_subscriptions()
    else:
        from newsletters.models import SubscriptionOptIn
        SubscriptionOptIn.objects.delete_expired_subscriptions()

def check_valid_model(option, opt_str, value, parser):
    from django.db.models import get_model
    
    model = get_model(*value.split('.'))
    if not model:
        raise OptionValueError("cannot find '%s' model in your application" % value)
    
    setattr(parser.values, option.dest, value)

if __name__ == '__main__':
    project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    site_packages_dir = os.path.abspath(os.path.join(project_root_dir, 'site-packages'))
    
    sys.path.insert(0, site_packages_dir)
    sys.path.insert(0, project_root_dir)
    sys.path.insert(0, project_dir)
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'franckgalland.settings'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(project_root_dir, 'tmp')
    from django.core.management import setup_environ
    import franckgalland.settings
    setup_environ(franckgalland.settings)
    
    parser = OptionParser("usage: %prog --model_str")
    parser.add_option('-m', '--model_str', action='callback', dest='model_str', type="string", callback=check_valid_model, help="model_str must be formatted: app_name.model_name")
    (options,args) = parser.parse_args()
    
    delete_expired_subscriptions(parser)
