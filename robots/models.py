from django.db import models
from django.contrib.admin.views.doc import simplify_regex
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

def installed_url_patterns():
    """
    Helper function to return URL patterns of the installed applications
    """
    paths = []
    urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
    for pattern in urlconf.urlpatterns:
        url_pattern = simplify_regex(pattern.regex.pattern)
        if not url_pattern.endswith("robots.txt"):
            paths.append(url_pattern)
    return " ".join(paths)

class Url(models.Model):
    """
    Defines a URL pattern which should not be allowed to be accessed by a web
    robot. It's case-sensitive and exact, e.g. "/admin" and "/admin/" are
    different URLs.
    """
    pattern = models.CharField(_('pattern'), max_length=255, core=True,
        help_text=_('This is case-sensitive! Installed apps: %(patterns)s') % {'patterns': installed_url_patterns()})
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
    Defines a abstract rule which should be added to the virtual robots.txt
    file, disallowing the user agent to access the given URLs. It uses the
    Site contrib application to enable multiple robots.txt files.
    """
    user_agent = models.CharField(_('user agent'), max_length=255, 
        help_text=_("This should be a user agent string like 'Googlebot'. For a full list look at the <a href='http://www.robotstxt.org/wc/active/html/index.html'>database of Web Robots</a>. Enter '*' for matching all user agents."))
    urls = models.ManyToManyField(Url, help_text="These are URLs which are not allowed to be accessed by web robots.")
    sites = models.ManyToManyField(Site)
    class Meta:
        verbose_name = _('rule')
        verbose_name_plural = _('rules')
        ordering = ('-user_agent',)
    class Admin:
        list_filter = ('sites',)
        search_fields = ('user_agent',)
    def __unicode__(self):
        return u"%s" % self.user_agent
