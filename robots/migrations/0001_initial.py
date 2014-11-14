# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('robot', models.CharField(help_text="This should be a user agent string like 'Googlebot'. Enter an asterisk (*) for all user agents. For a full list look at the <a target=_blank href='http://www.robotstxt.org/db.html'> database of Web Robots</a>.", max_length=255, verbose_name='robot')),
                ('crawl_delay', models.DecimalField(decimal_places=1, max_digits=3, blank=True, help_text="Between 0.1 and 99.0. This field is supported by some search engines and defines the delay between successive crawler accesses in seconds. If the crawler rate is a problem for your server, you can set the delay up to 5 or 10 or a comfortable value for your server, but it's suggested to start with small values (0.5-1), and increase as needed to an acceptable value for your server. Larger delay values add more delay between successive crawl accesses and decrease the maximum crawl rate to your web server.", null=True, verbose_name='crawl delay')),
            ],
            options={
                'verbose_name': 'rule',
                'verbose_name_plural': 'rules',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(help_text="Case-sensitive. A missing trailing slash does also match to files which start with the name of the pattern, e.g., '/admin' matches /admin.html too. Some major search engines allow an asterisk (*) as a wildcard and a dollar sign ($) to match the end of the URL, e.g., '/*.jpg$'.", max_length=255, verbose_name='pattern')),
            ],
            options={
                'verbose_name': 'url',
                'verbose_name_plural': 'url',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rule',
            name='allowed',
            field=models.ManyToManyField(help_text='The URLs which are allowed to be accessed by bots.', related_name='allowed', verbose_name='allowed', to='robots.Url', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rule',
            name='disallowed',
            field=models.ManyToManyField(help_text='The URLs which are not allowed to be accessed by bots.', related_name='disallowed', verbose_name='disallowed', to='robots.Url', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rule',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', verbose_name='sites'),
            preserve_default=True,
        ),
    ]
