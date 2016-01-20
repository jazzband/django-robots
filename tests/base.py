# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import SESSION_KEY
from django.http import SimpleCookie
from django.test import RequestFactory, TestCase
from django.utils.six import StringIO


class BaseTest(TestCase):
    """
    Base class with utility function
    """
    @classmethod
    def setUpClass(cls):
        super(BaseTest, cls).setUpClass()
        cls.request_factory = RequestFactory()

    def get_request(self, path, user, lang, secure=False):
        from django.contrib.auth.models import AnonymousUser
        request = self.request_factory.get(path, secure=secure)

        if not user:
            user = AnonymousUser()
        request.user = user
        request._cached_user = user
        request.session = {}
        if secure:
            request.environ['SERVER_PORT'] = str('443')
            request.environ['wsgi.url_scheme'] = str('https')
        if user.is_authenticated():
            request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
        request.cookies = SimpleCookie()
        request.errors = StringIO()
        request.LANGUAGE_CODE = lang
        if request.method == 'POST':
            request._dont_enforce_csrf_checks = True
        return request
