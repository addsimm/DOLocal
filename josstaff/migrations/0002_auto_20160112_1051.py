# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import josstaff.models
import mezzanine.core.fields
import mezzanine.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('sites', '0001_initial'),
        ('josstaff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JOSStaffMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keywords_string', models.CharField(max_length=500, editable=False, blank=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('_meta_title', models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('status', models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True)),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True)),
                ('short_url', models.URLField(null=True, blank=True)),
                ('in_sitemap', models.BooleanField(default=True, verbose_name='Show in sitemap')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('modified_date', models.DateField(auto_now=True)),
                ('first_name', josstaff.models.StrippedCharField(max_length=60)),
                ('last_name', josstaff.models.StrippedCharField(max_length=60)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('bio_text', models.TextField(blank=True)),
                ('bio_image', mezzanine.core.fields.FileField(max_length=255, null=True, verbose_name='Bio Image', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'JOS Staff Member',
                'verbose_name_plural': 'JOS Staff Members',
            },
            bases=(mezzanine.utils.models.AdminThumbMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='staffgallery',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='StaffGallery',
        ),
    ]
