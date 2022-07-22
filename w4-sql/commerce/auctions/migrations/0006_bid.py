# Generated by Django 4.0.6 on 2022-07-22 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_listing_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('bidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bidder', to=settings.AUTH_USER_MODEL)),
                ('listing_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listing_id', to='auctions.listing')),
            ],
        ),
    ]
