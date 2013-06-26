from django.conf import settings
from robots.models import Url
from cms.sitemaps import CMSSitemap
from robots.settings import ADMIN
from django.db.models import Q
from itertools import chain

ID_PREFIX = 'disallowed'


def get_site_id(data, instance, sites_field):
    if instance and instance.id:
        id = instance.sites.all()[0].id
    else:
        id = sites_field.choices.queryset[0].id
    return data.get('sites', id)


def get_url(pattern):
    try:
        return Url.objects.get_or_create(pattern=pattern)[0]
    except Url.MultipleObjectsReturned:
        return Url.objects.filter(pattern=pattern)[0]


def get_choices(site, protocol):
    """
    Returns a list with the urls patterns for the site parameter
    The list will be in this format required by the disallowed field widget:
    [['1', '/pattern1/'], ['2', '/pattern2/'], ['disallowed_3', '/pattern4/'], ...]

    The patterns are taken from the sitemap for the site param.
    Some of the ids are real db ids, and others (like disallowed_3) are fake ones
    (generated here).
    """

    #generate patterns from the sitemap
    saved_site = settings.__class__.SITE_ID.value
    settings.__class__.SITE_ID.value = site.id
    urls = CMSSitemap().get_urls(site=site, protocol=protocol)
    all_patterns = map(lambda item: item['location'].replace("%s://%s" % (protocol, site.domain), ''), urls)
    settings.__class__.SITE_ID.value = saved_site

    #some patterns are already present in the db and I need their real ids
    f = Q(pattern__in=all_patterns) | Q(disallowed__in=site.rule_set.all())
    db_urls = Url.objects.filter(f).values_list('id', 'pattern').distinct()
    db_ids, db_patterns = ([], []) if not db_urls.exists() else zip(*db_urls)

    # Generate some fake ids for the patterns that were not
    #  previously saved in the db
    remaining_patterns = [x for x in all_patterns if x not in db_patterns]
    fake_ids = map(lambda x: '%s_%d' % (ID_PREFIX, x), range(len(remaining_patterns)))

    # Make sure that the '/admin/' pattern is allways present
    #  in the choice list
    admin = get_url(ADMIN)
    admin_pair = [[str(admin.id), admin.pattern]] if not admin.id in db_ids else []

    # returns a list of ['id', 'pattern'] pairs
    return map(lambda x: list(x), chain(admin_pair, db_urls, zip(fake_ids, remaining_patterns)))
