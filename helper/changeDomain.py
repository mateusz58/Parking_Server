
import sys


from django.contrib.sites.models import Site
site = Site(domain="192.168.8.106:8000", name="My awesome site")
site.save()