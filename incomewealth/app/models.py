# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class IncomeWealth(models.Model):
    year = models.IntegerField(null=False, blank=False)
    income_top_10 = models.FloatField(null=False, blank=False)
    wealth_top_10 = models.FloatField(null=False, blank=False)
    income_bottom_50 = models.FloatField(null=False, blank=False)
    wealth_bottom_50 = models.FloatField(null=False, blank=False)
