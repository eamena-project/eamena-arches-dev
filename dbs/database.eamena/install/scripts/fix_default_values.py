from django.core.management.base import BaseCommand
from arches.app.models.system_settings import settings
from arches.app.models import models
import logging, sys, os, json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
        """
        Fixes the widgets that have no defaultValue
        """

        def handle(self, *args, **options):

                for w in models.Widget.objects.all():

                        if 'defaultValue' in w.defaultconfig:
                                continue

                        print(w)
                        print(w.defaultconfig)
                        print("")

                        w.defaultconfig['defaultValue'] = None
                        w.save()