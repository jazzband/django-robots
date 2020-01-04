# -*- coding: utf-8 -*-
from django.db import models
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Url'
        db.create_table(
            "robots_url",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                (
                    "pattern",
                    self.gf("django.db.models.fields.CharField")(max_length=255),
                ),
            ),
        )
        db.send_create_signal("robots", ["Url"])

        # Adding model 'Rule'
        db.create_table(
            "robots_rule",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                ("robot", self.gf("django.db.models.fields.CharField")(max_length=255)),
                (
                    "crawl_delay",
                    self.gf("django.db.models.fields.DecimalField")(
                        null=True, max_digits=3, decimal_places=1, blank=True
                    ),
                ),
            ),
        )
        db.send_create_signal("robots", ["Rule"])

        # Adding M2M table for field allowed on 'Rule'
        db.create_table(
            "robots_rule_allowed",
            (
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID", primary_key=True, auto_created=True
                    ),
                ),
                ("rule", models.ForeignKey(orm["robots.rule"], null=False)),
                ("url", models.ForeignKey(orm["robots.url"], null=False)),
            ),
        )
        db.create_unique("robots_rule_allowed", ["rule_id", "url_id"])

        # Adding M2M table for field disallowed on 'Rule'
        db.create_table(
            "robots_rule_disallowed",
            (
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID", primary_key=True, auto_created=True
                    ),
                ),
                ("rule", models.ForeignKey(orm["robots.rule"], null=False)),
                ("url", models.ForeignKey(orm["robots.url"], null=False)),
            ),
        )
        db.create_unique("robots_rule_disallowed", ["rule_id", "url_id"])

        # Adding M2M table for field sites on 'Rule'
        db.create_table(
            "robots_rule_sites",
            (
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID", primary_key=True, auto_created=True
                    ),
                ),
                ("rule", models.ForeignKey(orm["robots.rule"], null=False)),
                ("site", models.ForeignKey(orm["sites.site"], null=False)),
            ),
        )
        db.create_unique("robots_rule_sites", ["rule_id", "site_id"])

    def backwards(self, orm):
        # Deleting model 'Url'
        db.delete_table("robots_url")

        # Deleting model 'Rule'
        db.delete_table("robots_rule")

        # Removing M2M table for field allowed on 'Rule'
        db.delete_table("robots_rule_allowed")

        # Removing M2M table for field disallowed on 'Rule'
        db.delete_table("robots_rule_disallowed")

        # Removing M2M table for field sites on 'Rule'
        db.delete_table("robots_rule_sites")

    models = {
        "robots.rule": {
            "Meta": {"object_name": "Rule"},
            "allowed": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {
                    "symmetrical": "False",
                    "related_name": "'allowed'",
                    "blank": "True",
                    "to": "orm['robots.Url']",
                },
            ),
            "crawl_delay": (
                "django.db.models.fields.DecimalField",
                [],
                {
                    "null": "True",
                    "max_digits": "3",
                    "decimal_places": "1",
                    "blank": "True",
                },
            ),
            "disallowed": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {
                    "symmetrical": "False",
                    "related_name": "'disallowed'",
                    "blank": "True",
                    "to": "orm['robots.Url']",
                },
            ),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "robot": ("django.db.models.fields.CharField", [], {"max_length": "255"}),
            "sites": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {"to": "orm['sites.Site']", "symmetrical": "False"},
            ),
        },
        "robots.url": {
            "Meta": {"object_name": "Url"},
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "pattern": ("django.db.models.fields.CharField", [], {"max_length": "255"}),
        },
        "sites.site": {
            "Meta": {
                "ordering": "('domain',)",
                "object_name": "Site",
                "db_table": "'django_site'",
            },
            "domain": ("django.db.models.fields.CharField", [], {"max_length": "100"}),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "name": ("django.db.models.fields.CharField", [], {"max_length": "50"}),
        },
    }

    complete_apps = ["robots"]
