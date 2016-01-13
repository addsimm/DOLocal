# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields
import mezzanine.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffGallery',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('featured_image', mezzanine.core.fields.FileField(max_length=255, null=True, verbose_name='Featured Image', blank=True)),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Staff Gallery',
                'verbose_name_plural': 'Staff Galleries',
            },
            bases=(mezzanine.utils.models.AdminThumbMixin, 'pages.page'),
        ),
    ]
