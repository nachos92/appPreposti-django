import datetime
from datetime import date
from django.core.mail import send_mail
from setup.models import Responsabile, Impostazione, GiornoChiusura, Dipendente
from models import Settimana, SegnalazionePrep
from django.conf import settings



################## Funzioni e variabili di supporto
# ----------------------------------------->
'''
Gruppo di funzioni che vanno selezionano l'attributo "standard" o inserito in impostazioni,
in base allo stato attivo/non attivo dell'oggetto impostazione.
'''

def selezMessaggio():
    try:
        imp = Impostazione.objects.get(id=1)
        if (imp.attiva==True):
            return imp.getMessaggio()
    except:
        print "Errore selezMessaggio()."
    else:
        return getattr(settings, "MESSAGGIO", None)

def selezMittente():
    return getattr(settings, "EMAIL_HOST_USER", None)

def selezPassword():
    return getattr(settings, "EMAIL_HOST_PASSWORD", None)

def selezSoglia_ore():
    try:
        imp = Impostazione.objects.get(id=1)
        if (imp.attiva==True):
            return imp.getSogliaControllo_ore()
    except:
        print "Errore selezSoglia_ore()."
        return getattr(settings, "SOGLIA_ORE", None)

def selezSoglia_minuti():
    try:
        imp = Impostazione.objects.get(id=1)
        if (imp.attiva==True):
            return imp.getSogliaControllo_minuti()
    except:
        print "Errore selezSoglia_minuti()."
        return getattr(settings, "SOGLIA_MINUTI", None)


# <-----------------------------------------

def invio_email(x):
    try:
        send_mail(
            subject=('['+str(x.getPreposto())+'] Mancato giro controlli'),
            message= selezMessaggio(),
            from_email= selezMittente(),
            recipient_list=[
                Responsabile.objects.get(
                    last_name=x.getPreposto().getSuperiore()
                ).getEmail(),
            ],
            auth_user= selezMittente(),
            auth_password= selezPassword(),
            fail_silently=False
        )
        print "INVIO EMAIL"
    except:
        print "Errore send_mail"

soglia_tot = datetime.timedelta(
    hours=selezSoglia_ore(),
    minutes=selezSoglia_minuti()
)


################## Fine funzioni e variabili di supporto



def check_giornochiusura():
    oggi = datetime.date.today()
    if(GiornoChiusura.objects.filter(data=oggi).exists() == True):
        pass
    else:
        check_controlli()


def check_fuoriorario(orario):
    '''
    Ritorna true se si e' oltre l'orario limite per eseguire i controlli
    del giorno.
    '''
    if datetime.datetime.now().time() > ((datetime.datetime.combine(
            datetime.date(1,1,1),
            orario.getOrario()) + soglia_tot)).time():
        return True
    else:
        return False


"""
Esegue il controllo periodico per verificare che i preposti non abbiano
dimenticato di fare un giro controlli o che non l'abbiano fatto fuori tempo limite (questo
secondo caso vuol dire che magari hanno iniziato tardi e all'orario limite devono ancora finire).
"""
def check_controlli():

    #Ottengo gli elem di Settimana nel periodo giusto
    totali = Settimana.objects.filter(data_inizio__lte=date.today())

    '''
    Per ogni elem di totali devo prima fare uno switch-case per il weekday e poi verifico
    se gg_check==false; nel caso, se gg_fatto==false invio una notifica al superiore.
    '''
    k = date.today().weekday()

    for x in totali:
        persone = Dipendente.objects.filter(impiego=x.getArea(), fatto=False)

        if (k == 0):
            if x.lun_check == False:
                if check_fuoriorario(x.lunedi) == True:

                    '''
                    Azzeramento dei valori di tutti i gg_check (impostazione a False)
                    '''
                    x.mar_check = False
                    x.mer_check = False
                    x.gio_check = False
                    x.ven_check = False
                    x.sab_check = False
                    x.dom_check = False

                    if x.lun_fatto == False:

                        if len(persone)== 0:
                            x.lun_fatto=True
                        else:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                            invio_email(x)


                    x.lun_check = True
                    x.save()


        if (k == 1):
            if x.mar_check == False:

                if check_fuoriorario(x.martedi) == True:
                    if x.mar_fatto == False:
                        if len(persone)==0:
                            x.mar_fatto = True
                        else:

                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                            invio_email(x)

                    x.mar_check = True
                    x.save()


        if (k == 2):
            if x.mer_check == False:

                if check_fuoriorario(x.mercoledi) == True:
                    if x.mer_fatto == False:
                        if len(persone)==0:
                            x.mar_fatto = True
                        else:

                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                            invio_email(x)

                    x.mer_check = True
                    x.save()


        if (k == 3):

            if x.gio_check == False:
                if check_fuoriorario(x.giovedi) == True:
                    if x.gio_fatto == False:
                        if len(persone)==0:
                            x.gio_fatto = True
                        else:

                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                            invio_email(x)

                    x.gio_check = True
                    x.save()


        if (k == 4):

            if x.ven_check == False:
                if check_fuoriorario(x.venerdi) == True:
                    if x.ven_fatto == False:
                        if len(persone)==0:
                            x.ven_fatto = True
                        else:

                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                            invio_email(x)

                    x.ven_check = True
                    x.save()

        if (k == 5):
            if x.sab_check == False:
                if check_fuoriorario(x.sabato) == True:

                    if x.sab_fatto == False:
                        if len(persone) == 0:
                            x.sab_fatto = True
                        else:

                            SegnalazionePrep.create(
                                matr=x.getPreposto(),
                                dett=selezMessaggio(),
                            ).save()

                            invio_email(x)

                    x.sab_check = True
                    x.save()
        if (k == 6):

            if x.dom_check == False:
                if check_fuoriorario(x.domenica) == True:
                    x.lun_check = False

                    if x.dom_fatto == False:
                        if len(persone) == 0:
                            x.dom_fatto = True
                        else:

                            SegnalazionePrep.create(
                                matr=x.getPreposto(),
                                dett=selezMessaggio(),
                            ).save()

                            invio_email(x)

                    x.dom_check = True
                    x.save()


def check_impostazioni():

    imp = Impostazione.objects.get(pk=1)
    imp_fut = Impostazione.objects.get(pk=2)


    if (imp_fut.attiva == True):
        if (imp_fut.is_today()):

            #Copia dei valori di #2 in #1
            imp.messaggio = imp_fut.getMessaggio()

            imp.sogliaControllo_ore = imp_fut.getSogliaControllo_ore()
            imp.sogliaControllo_minuti = imp_fut.getSogliaControllo_minuti()
            imp.data_inizio = imp_fut.data_inizio
            imp_fut.attiva = False
            imp_fut.save()

    if (imp_fut.attiva == False):
        if (imp_fut.is_today()==False):
            imp_fut.attiva=True
            imp_fut.save()

    if (imp.is_today()):
        imp.attiva = True
        imp.save()

    if (imp.data_inizio > date.today()):
        if imp.attiva == True:
            imp.attiva = False
            imp.save()