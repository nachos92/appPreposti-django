from django.contrib import admin
from .models import *


class SettimanaAdmin(admin.ModelAdmin):

    fields = [
        'cod_preposto',
        'area',
        'data_inizio',
        'lun',
        'mar',
        'mer',
        'gio',
        'ven',
	    'lun_fatto',
	    'lun_check',
        'mar_fatto',
        'mar_check',
        'mer_fatto',
        'mer_check',
        'gio_fatto',
        'gio_check',
        'ven_fatto',
        'ven_check',
    ]

    list_display = [
        'id',
        'completato',
        'cod_preposto',
        'area',
        'data_inizio',
	    'lun_fatto',
	    'lun_check',
        'mar_fatto',
        'mar_check',
        'mer_fatto',
        'mer_check',
        'gio_fatto',
        'gio_check',
        'ven_fatto',
        'ven_check',
    ]

class SegnalazioneAdmin(admin.ModelAdmin):
    fields =[
        'matricola',
        'dettaglio'
    ]

    list_display = [
        'id',
        'matricola',
        'data'
    ]
    readonly_fields = ('data',)

class SegnalazionePrepAdmin(admin.ModelAdmin):
    fields =[
        'matricola',
        'dettaglio'
    ]

    list_display = [
        'id',
        'matricola',
        'data'
    ]
    readonly_fields = ('data',)

admin.site.register(Settimana, SettimanaAdmin)
admin.site.register(Segnalazione, SegnalazioneAdmin)
admin.site.register(SegnalazionePrep, SegnalazionePrepAdmin)