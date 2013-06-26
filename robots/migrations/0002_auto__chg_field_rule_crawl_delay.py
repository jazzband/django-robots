# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from robots.models import Rule, Url
from itertools import ifilter
from django.db import router
from robots.settings import ADMIN
from django.db import transaction


@transaction.commit_manually
def flush_transaction():
    transaction.commit()


def get_url(pattern, manager):
    try:
        return manager.get_or_create(pattern=pattern)[0]
    except Url.MultipleObjectsReturned:
        return manager.filter(pattern=pattern)[0]


def duplicate_rules_with_multiple_sites(rules, manager):
    for r in ifilter(lambda x: x.sites.count() > 1, rules):
        for site in r.sites.all()[1:]:
            rule = manager.create(robot=r.robot, crawl_delay=r.crawl_delay)
            rule.allowed = r.allowed.all()
            rule.disallowed = r.disallowed.all()
            rule.sites.add(site)
            rule.save()
        first_site = r.sites.all()[0]
        r.sites.clear()
        r.sites.add(first_site)


def add_default_disallowed(rules, manager):
    admin = get_url(ADMIN, manager)
    for r in rules.exclude(disallowed__in=[admin]):
        r.disallowed.add(admin)


def add_default_allowed(rules, manager):
    allow_all = get_url('/*', manager)
    for r in rules.exclude(allowed__in=[allow_all]):
        r.allowed.add(allow_all)


class Migration(SchemaMigration):

    no_dry_run = True

    def forwards(self, orm):

        # Changing field 'Rule.crawl_delay'
        db.alter_column('robots_rule', 'crawl_delay', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1))

        rules_manager = orm.models.get("robots.rule").objects\
                        .db_manager(router.db_for_write(Rule))

        duplicate_rules_with_multiple_sites(rules_manager.all(), rules_manager)

        flush_transaction()

        rules_manager = orm.models.get("robots.rule").objects\
                        .db_manager(router.db_for_write(Rule))
        url_manager = orm.models.get("robots.url").objects\
                        .db_manager(router.db_for_write(Url))

        add_default_disallowed(rules_manager.all(), url_manager)
        add_default_allowed(rules_manager.all(), url_manager)


    def backwards(self, orm):

        # Changing field 'Rule.crawl_delay'
        db.alter_column('robots_rule', 'crawl_delay', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=1))

    models = {
        'robots.rule': {
            'Meta': {'object_name': 'Rule'},
            'allowed': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'allowed'", 'blank': 'True', 'to': "orm['robots.Url']"}),
            'crawl_delay': ('django.db.models.fields.DecimalField', [], {'default': '5.0', 'max_digits': '3', 'decimal_places': '1'}),
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