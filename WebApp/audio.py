import soundfile as sf
import numpy as np
import sounddevice as sd
import os

sayi_sozlugu = {0:'sıfır', 1:'bir', 2:'iki', 3:'üç', 4:'dört',5:'beş',
                6:'altı', 7:'yedi', 8:'sekiz', 9:'dokuz', 10:'on', 20:'yirmi', 
                30:'otuz', 40:'kırk', 50:'elli', 60:'altmış', 70:'yetmiş', 80:'seksen', 
                90:'doksan', 100:'yüz', 1000:'bin', 1e6:'milyon', 1e9:'milyar'}


WAV_KAYIT_ADRESI = './WebApp/static/'

sayilar = list(sayi_sozlugu.values())
ses_adresleri = [WAV_KAYIT_ADRESI + sayi + '.wav' for sayi in sayilar]

sesler = [sf.read(adres)[0] for adres in ses_adresleri]

sayi_ses_sozlugu = {'frekans' : sf.read(ses_adresleri[0])[1]}

for sayi, ses in zip(sayilar, sesler):
    # her bir sayinin karsisina o sayinin ses dosyasini deger olarak atiyorum.
    sayi_ses_sozlugu[sayi] = ses



def uc_basamak_cevirici(sayi, okunus=None):
    if okunus is None:
        okunus = list()
    birler_basamagi = sayi % 10
    onlar_basamagi = ((sayi // 10) % 10) * 10
    yuzler_basamagi = sayi // 100
    if yuzler_basamagi != 0:
        if yuzler_basamagi != 1:
            okunus.append(sayi_sozlugu[yuzler_basamagi])
        okunus.append(sayi_sozlugu[100])
    if onlar_basamagi != 0:
        okunus.append(sayi_sozlugu[onlar_basamagi])     
    if birler_basamagi != 0:
        okunus.append(sayi_sozlugu[birler_basamagi])
    return(okunus)



def sayidan_metin_cevirici(sayi):
    birinci_uc_basamak = sayi % 1e3
    ikinci_uc_basamak = (sayi // 1e3) % 1e3
    ucuncu_uc_basamak = (sayi // 1e6) % 1e3
    dorduncu_uc_basamak = (sayi // 1e9) % 1e3
    okunus = None
    if dorduncu_uc_basamak != 0:
        okunus = uc_basamak_cevirici(dorduncu_uc_basamak)
        okunus.append(sayi_sozlugu[1e9])
        
    if ucuncu_uc_basamak != 0:
        okunus = uc_basamak_cevirici(ucuncu_uc_basamak, okunus)
        okunus.append(sayi_sozlugu[1e6])
    
    if ikinci_uc_basamak != 0:
        if ikinci_uc_basamak == 1:
            if not okunus == None:
                okunus.append(sayi_sozlugu[1e3])
            else:
                okunus = [sayi_sozlugu[1e3]]
                
        else:
            okunus = uc_basamak_cevirici(ikinci_uc_basamak, okunus)
            okunus.append(sayi_sozlugu[1e3])

        
    if birinci_uc_basamak != 0:
        okunus = uc_basamak_cevirici(birinci_uc_basamak, okunus)
        
    if okunus is None:
        okunus = ['sıfır']
        
    return okunus

def ses_birlestirici(okunus_listesi):
    ses_birlesimi = np.array([[0, 0]])
    for key in okunus_listesi:
        ses_birlesimi = np.concatenate((ses_birlesimi, sayi_ses_sozlugu[key]))
    return ses_birlesimi

def calistir(sayi, i):
    sayi = sayi.replace('\n', '').replace(' ', '')
    
    if not sayi.isdigit():
        return False, "Girdiginiz bir tam sayi olmalidir!"
        
    sayi = int(sayi)
    if len(str(sayi)) > 12:
        return False, "Girdiginiz sayi 9 basamagi gecmemelidir!"

    okunus_listesi = sayidan_metin_cevirici(sayi)
    birlesim = ses_birlestirici(okunus_listesi)
    frekans = sayi_ses_sozlugu['frekans']
    #print(os.getcwd())
    sf.write(f'./WebApp/static/audio{i}.wav', birlesim, frekans)
    return (True, ' '.join([str(a) for a in okunus_listesi]))