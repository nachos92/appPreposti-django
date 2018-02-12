import datetime
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from setup.models import Responsabile, Preposto, Impostazione
from models import Settimana, SegnalazionePrep


#------- Variabili modificati in base ai valori di Impostazione

SOGLIA_ORE = 1
SOGLIA_MINUTI = 0



startDate = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
endDate = startDate + datetime.timedelta(days=6)

soglia_tot = datetime.timedelta(hours=SOGLIA_ORE, minutes=SOGLIA_MINUTI)


def aggiornaMessaggio(prima,dopo):
    prima = dopo

###-------- Fine blocco variabili

# ----------------------------------------->
'''
Gruppo di funzioni che vanno selezionano l'attributo "standard" o inserito in impostazioni,
in base allo stato attivo/non attivo dell'oggetto impostazione.
'''

def selezMessaggio():
    try:
        imp = Impostazione.objects.get(pk=1)
        if (imp.attiva==True):
            return imp.getMessaggio()
    except:
        print "Impostazione(pk=1) inesistente."
    else:
        return getattr(settings, "MESSAGGIO", None)

def selezMittente():
    try:
        imp = Impostazione.objects.get(pk=1)
        if (imp.attiva==True):
            return imp.getSMTP_username()
    except:
        print "Impostazione (pk=1) inesistente."
    else:
        return getattr(settings, "EMAIL_HOST_USER", None)

def selezPassword():
    try:
        imp = Impostazione.objects.get(pk=1)
        if (imp.attiva==True):
            return imp.getSMTP_password()
    except:
        print "Impostazione (pk=1) inesistente."
    else:
        return getattr(settings, "EMAIL_HOST_PASSWORD", None)


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
        print "INVIO MAIL ----------"

    except:
        print "Errore send_mail"
    else:
        pass






"""
Esegue il controllo periodico per verificare che i preposti non abbiano
dimenticato di fare un giro controlli o che non l'abbiano fatto fuori tempo limite (questo
secondo caso vuol dire che magari hanno iniziato tardi e all'orario limite devono ancora finire).
"""
def check_controlli():
    #Ottengo gli elem di Settimana nel periodo giusto
    totali = Settimana.objects.filter(
        data_inizio__range=[startDate, endDate],
    )

    '''
    Per ogni elem di totali devo prima fare uno switch-case per il weekday e poi verifico
    se gg_check==false; nel caso, se gg_fatto==false invio una notifica al superiore.
    '''
    k = date.today().weekday()


    for x in totali:

        if (k == 0):
            if x.lun_festivo == False and x.lun_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.lun,'%H:%M')+ soglia_tot).time():

                    if x.lun_fatto == False:

                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)


                    x.lun_check = True
                    x.save()


        if (k == 1):
            if x.mar_festivo == False and x.mar_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.mar,'%H:%M')+ soglia_tot).time():

                    if x.mar_fatto == False:
                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)


                    x.mar_check = True
                    x.save()


        if (k == 2):
            if x.mer_festivo == False and x.mer_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.mer,'%H:%M')+ soglia_tot).time():

                    if x.mer_fatto == False:
                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)



                    x.mer_check = True
                    x.save()


        if (k == 3):

            if x.gio_festivo == False and x.gio_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.gio,'%H:%M')+ soglia_tot).time():

                    if x.gio_fatto == False:
                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)


                    x.gio_check = True
                    x.save()



        if (k == 4):

            if x.ven_festivo == False and x.ven_check == False:
                if datetime.datetime.now().time() > \
                        (datetime.datetime.strptime(x.ven,'%H:%M')+ soglia_tot).time():

                    if x.ven_fatto == False:
                        try:
                            SegnalazionePrep.create(
                                matr= x.getPreposto(),
                                dett= selezMessaggio(),
                            ).save()

                        except:
                            print "Errore creazione SegnalazionePrep."


                        invio_email(x)



                    x.ven_check = True
                    x.save()


"""
Ricordarsi per la prima volta che si compila l'impostazione,
di mettere la data odierna, in modo che vengano caricati i valori
"""
def aggiornamento():
    sett = Impostazione.objects.get(pk=1)
    if(sett.nuovo & sett.is_today()):

        #DA SBLOCCARE DOPO AVER CREATO UN CUSTOM EMAIL BACKEND
        '''
        global EMAIL_HOST
        EMAIL_HOST = sett.getSMTP_server()

        global EMAIL_HOST_USER
        EMAIL_HOST_USER = sett.getSMTP_username()

        global EMAIL_HOST_PASSWORD
        EMAIL_HOST_PASSWORD = sett.getSMTP_password()
        '''

        #global MESSAGGIO
        #MESSAGGIO = sett.getMessaggio()

        sett.nuovo = False
        sett.save()



def check_impostazioni():
    imp = Impostazione.objects.get(pk=1)

    if(imp):
        if (imp.is_today()):
            imp.attiva = True
            imp.save()