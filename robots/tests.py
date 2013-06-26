from django.test import TestCase
from robots.helpers import get_choices
from robots.models import Url, Rule
from cms.api import create_page
from django.contrib.sites.models import Site
from django.contrib.auth.models import User


class TestRules(TestCase):

    def setUp(self):
        self.site = Site.objects.get(id=1)
        self._create_pages(self.site)

    def _create_pages(self, site):
        page1 = create_page('page1', 'test.html', 'en', site=site, published=True)
        page2 = create_page('page2', 'test.html', 'en', slug='page2', site=site, published=True)
        page3 = create_page('page3', 'test.html', 'en', slug='page3', site=site, published=True)
        page4 = create_page('page4', 'test.html', 'en', slug='page4', site=site, published=True)
        page41 = create_page('page4_1', 'test.html', 'en', slug='page41', site=site, parent=page4, published=True)
        page42 = create_page('page4_2', 'test.html', 'en', slug='page42', site=site, parent=page4, published=True)

    def _get_superuser(self):
        admin = User(username="admin", is_staff=True, is_active=True, is_superuser=True)
        admin.set_password("admin")
        admin.save()
        return admin

    def test_choices_no_existing_disallowed_rule(self):

        choices = get_choices(self.site, 'http')

        self.assertListEqual(choices, \
            [['1', '/admin/'], ['disallowed_0', u'/'],
             ['disallowed_1', u'/page2/'], ['disallowed_2', u'/page3/'],
             ['disallowed_3', u'/page4/'], ['disallowed_4', u'/page4/page41/'],
             ['disallowed_5', u'/page4/page42/']])

    def test_choices_existing_disallowed_rules(self):
        rule = Rule.objects.create(robot='*')
        rule.sites.add(self.site)
        url1 = Url.objects.create(pattern='/default/')
        url2 = Url.objects.create(pattern='/page2/')
        rule.disallowed.add(url1)

        choices = get_choices(self.site, 'http')
        self.assertListEqual(choices, \
            [['3', '/admin/'], [1, u'/default/'], [2, u'/page2/'],
             ['disallowed_0', u'/'], ['disallowed_1', u'/page3/'],
             ['disallowed_2', u'/page4/'], ['disallowed_3', u'/page4/page41/'],
             ['disallowed_4', u'/page4/page42/']])

    def test_selection_boxes_add_rule_admin_selected_by_default(self):
        su = self._get_superuser()
        self.client.login(username='admin', password='admin')
        response = self.client.get('/admin/robots/rule/add/')

        #/admin/ is selected by default
        selection_tag = \
"""<select multiple="multiple" class="selectfilter" name="disallowed" id="id_disallowed">
<option value="1" selected="selected">/admin/</option>
<option value="disallowed_0">/</option>
<option value="disallowed_1">/page2/</option>
<option value="disallowed_2">/page3/</option>
<option value="disallowed_3">/page4/</option>
<option value="disallowed_4">/page4/page41/</option>
<option value="disallowed_5">/page4/page42/</option>
</select>"""

        self.assertTrue(selection_tag in response.content)

    def test_selection_boxes_existing_rule(self):
        rule = Rule.objects.create(robot='*')
        rule.sites.add(self.site)
        url1 = Url.objects.create(pattern='/admin/')
        url2 = Url.objects.create(pattern='/default/')
        url3 = Url.objects.create(pattern='/page2/')
        rule.disallowed.add(url1)
        rule.disallowed.add(url2)
        rule.disallowed.add(url3)
        su = self._get_superuser()
        self.client.login(username='admin', password='admin')
        response = self.client.get('/admin/robots/rule/1/')

        selection_tag = \
"""<select multiple="multiple" class="selectfilter" name="disallowed" id="id_disallowed">
<option value="1" selected="selected">/admin/</option>
<option value="2" selected="selected">/default/</option>
<option value="3" selected="selected">/page2/</option>
<option value="disallowed_0">/</option>
<option value="disallowed_1">/page3/</option>
<option value="disallowed_2">/page4/</option>
<option value="disallowed_3">/page4/page41/</option>
<option value="disallowed_4">/page4/page42/</option>
</select>"""

        self.assertTrue(selection_tag in response.content)
