# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from robots.models import Rule, Url
from itertools import ifilter
from robots.settings import ADMIN


def duplicate_rules_with_multiple_sites(rules):
    for r in ifilter(lambda x: x.sites.count() > 1, rules):
        for site in r.sites.all()[1:]:
            rule = Rule.objects.create(robot=r.robot, crawl_delay=r.crawl_delay)
            rule.allowed = r.allowed.all()
            rule.disallowed = r.disallowed.all()
            rule.sites.add(site)
            rule.save()
        first_site = r.sites.all()[0]
        r.sites.clear()
        r.sites.add(first_site)


def get_url(pattern):
    try:
        return Url.objects.get_or_create(pattern=pattern)
    except Url.MultipleObjectsReturned:
        return Url.objects.filter(pattern=pattern)[0]


def add_default_disallowed(rules):
    admin = get_url(ADMIN)
    for r in rules.exclude(disallowed__in=[admin]):
        rule.disallowed.add(admin)


def add_default_allowed(rules):
    allow_all = get_url('/*')
    for r in rules.exclude(allowed__in=[allow_all]):
        rule.allowed.add(allow_all)


class Migration(SchemaMigration):

    no_dry_run = True

    def forwards(self, orm):

        # Changing field 'Rule.crawl_delay'
        db.alter_column('robots_rule', 'crawl_delay', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1))

        rules = orm.models.get("robots.rule").objects\
                        .db_manager(router.db_for_write(Rule)).all()
        duplicate_rules_with_multiple_sites(rules)

        rules = orm.models.get("robots.rule").objects\
                        .db_manager(router.db_for_write(Rule)).iterator()

        add_default_disallowed(rules)
        add_default_allowed(rules)

    def backwards(self, orm):

        # Changing field 'Rule.crawl_delay'
        db.alter_column('robots_rule', 'crawl_delay', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=1))

    models = {
        'robots.rule': {
            'Meta': {'object_name': 'Rule'},
            'allowed': ('django.db.models.fields.related.ManyToManyField', [], {'default': "'/*'", 'related_name': "'allowed'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['robots.Url']"}),
            'crawl_delay': ('django.db.models.fields.DecimalField', [], {'default': '5', 'max_digits': '3', 'decimal_places': '1'}),
            'disallowed': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'disallowed'", 'blank': 'True', 'to': "orm['robots.Url']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'robot': ('django.db.models.fields.CharField', [], {'default': "'*'", 'max_length': '255'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'})
        },
        'robots.url': {
            'Meta': {'object_name': 'Url'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['robots']