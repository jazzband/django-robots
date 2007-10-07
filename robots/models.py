from django.db import models
from django.core import validators
from django.contrib.admin.views.doc import simplify_regex
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.utils.text import get_text_list
from django.conf import settings
# for backward incompatible changes in 0.97/trunk
try:
    from django.db.models import DecimalField as FloatField
except ImportError:
    from django.db.models import FloatField 

class Url(models.Model):
    """
    Defines a URL pattern for use with a robot exclusion rule. It's 
    case-sensitive and exact, e.g., "/admin" and "/admin/" are different URLs.
    """
    pattern = models.CharField(_('pattern'), max_length=255, core=True, help_text=_("Case-sensitive. A missing trailing slash does also match to files which start with the name of the pattern, e.g., '/admin' matches /admin.html too. Some major search engines allow an asterisk (*) as a wildcard and a dollar sign ($) to match the end of the URL, e.g., '/*.jpg$'."))

    class Meta:
        verbose_name = _('url')
        verbose_name_plural = _('url')

    class Admin:
        pass

    def __unicode__(self):
        return u"%s" % self.pattern

    def save(self):
        if not self.pattern.startswith('/'):
            self.pattern = '/' + self.pattern
        super(Url, self).save()

class Rule(models.Model):
    """
    Defines an abstract rule which is used to respond to crawling web robots,
    using the robot exclusion standard, a.k.a. robots.txt. It allows or 
    disallows the robot identified by its user agent to access the given URLs.
    The Site contrib app is used to enable multiple robots.txt per instance.
    """
    robot = models.CharField(_('robot'), max_length=255, help_text=_("This should be a user agent string like 'Googlebot'. Enter an asterisk (*) for all user agents. For a full list look at the <a target=_blank href='http://www.robotstxt.org/wc/active/html/index.html'>database of Web Robots</a>."))
    allowed = models.ManyToManyField(Url, blank=True, validator_list=[validators.RequiredIfOtherFieldNotGiven('disallowed')], related_name="allowed", help_text=_("These are URLs which are allowed to be accessed by web robots."))
    disallowed = models.ManyToManyField(Url, blank=True, validator_list=[validators.RequiredIfOtherFieldNotGiven('allowed')], related_name="disallowed", help_text=_("These are URLs which are not allowed to be accessed by web robots."))
    sites = models.ManyToManyField(Site)
    crawl_delay = FloatField(_('crawl delay'), blank=True, null=True, max_digits=3, decimal_places=1, help_text=("From 0.1 to 99.0. This field is supported by some search engines and defines the delay between successive crawler accesses in seconds. If the crawler rate is a problem for your server, you can set the delay up to 5 or 10 or a comfortable value for your server, but it's suggested to start with small values (0.5–1), and increase as needed to an acceptable value for your server. Larger delay values add more delay between successive crawl accesses and decrease the maximum crawl rate to your web server."))

    class Meta:
        verbose_name = _('rule')
        verbose_name_plural = _('rules')

    class Admin:
        fields = (
            (None, {'fields': ('robot', 'sites')}),
            (_('URL patterns'), {'fields': ('allowed', 'disallowed')}),
            (_('Advanced options'), {'classes': 'collapse', 'fields': ('crawl_delay',)}),
        )
        list_filter = ('sites',)
        list_display = ('robot', 'allowed_urls', 'disallowed_urls')
        search_fields = ('robot','urls')

    def __unicode__(self):
        return u"%s" % self.robot

    def allowed_urls(self):
        return get_text_list(list(self.allowed.all()), _('and'))
    allowed_urls.short_description = _('allowed')

    def disallowed_urls(self):
        return get_text_list(list(self.disallowed.all()), _('and'))
    disallowed_urls.short_description = _('disallowed')
