# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter(name='i18n_month')
def i18n_month(value):
    months = {
        1:u"Janvier",
        2:u"Février",
        3:u"Mars",
        4:u"Avril",
        5:u"Mai",
        6:u"Juin",
        7:u"Juillet",
        8:u"Août",
        9:u"Septembre",
        10:u"Octobre",
        11:u"Novembre",
        12:u"Décembre",
        
    }
    return months[value]
