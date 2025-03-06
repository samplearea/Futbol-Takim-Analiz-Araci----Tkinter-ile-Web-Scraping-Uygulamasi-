import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import os

# Varsayılan değer
DEFAULT_MAC_SAYISI = 10  # Gol analizi için kullanılacak son maç sayısı

def takim_bilgilerini_cek(takim):
    clear_screen()  # Ekranı temizle
    # Web sitesinden verileri çek 
    url = f"https://www.sporx.com/{takim}-fiksturu-ve-mac-sonuclari"  # Takımın fikstürüne ve maç sonuçlarına ulaşmak için URL
    response = requests.get(url)  # URL'ye istek gönder
    soup = BeautifulSoup(response.content, "html.parser")  # Gelen HTML'yi BeautifulSoup ile parse et

    # Maç sonuçlarını bul 
    maclar = soup.find_all("tr")  # Maçları içeren tüm satırları bul
    galibiyet_sayisi = 0  # Galibiyet sayısını başlat
    toplam_gol = 0  # Toplam gol sayısını başlat
    son_mac_skoru = None  # Son maçın skorunu başlat
    for mac in maclar:  # Her bir maçı kontrol et
        skor_element = mac.find("a", class_="d-block rounded bg-sporx text-white fw-bolder py-1 px-1 text-nowrap")  # Skoru içeren elementi bul
        if skor_element:  # Eğer skor varsa
            skor = skor_element.get_text(strip=True)  # Skoru al
            gol_sayisi = skor.split("-")  # Skoru iki takıma ayır
            if len(gol_sayisi) == 2 and gol_sayisi[0].strip() and gol_sayisi[1].strip():  # Skor geçerliyse
                try:
                    attigi_gol = int(gol_sayisi[0])  # Ev sahibi takımın attığı gol
                    gol_sayisi_g2 = int(gol_sayisi[1])  # Deplasman takımının attığı gol
                except ValueError:
                    continue  # Eğer skor sayıya dönüşemiyorsa, bir sonraki maça geç
                ev_sahibi = mac.find("td", class_="text-start w-25").find("a").get_text(strip=True)  # Ev sahibi takım adı
                deplasman = mac.find("td", class_="text-end w-25").find("a").get_text(strip=True)  # Deplasman takım adı
                if takim.lower() == turkce_karakter_degistir(ev_sahibi.lower()):  # Takım ev sahibi ise
                    toplam_gol += attigi_gol  # Toplam gole ekle
                    if attigi_gol > gol_sayisi_g2:  # Galibiyet mi?
                        galibiyet_sayisi += 1
                    son_mac_skoru = f"{ev_sahibi} {skor} {deplasman}\n"  # Son maçın skoru
                elif takim.lower() == turkce_karakter_degistir(deplasman.lower()):  # Takım deplasmanda ise
                    toplam_gol += gol_sayisi_g2  # Toplam gole deplasman golünü ekle
                    if attigi_gol < gol_sayisi_g2:  # Galibiyet mi?
                        galibiyet_sayisi += 1
                    son_mac_skoru = f"Son Maç: {ev_sahibi} {skor} {deplasman}\n"  # Son maçın skoru
    if galibiyet_sayisi == 0:
        messagebox.showerror("Hata", f"{takim.capitalize()} takımı için bilgi bulunamadı.")  # Eğer takımın galibiyeti yoksa hata mesajı göster
        return None, None, None
    else:
        return galibiyet_sayisi, toplam_gol, son_mac_skoru  # Galibiyet sayısı, toplam gol ve son maç skoru döndür

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizlemek için işletim sistemine göre komut

def turkce_karakter_degistir(takim_ad):
    # Türkçe karakterleri İngilizce karşılıklarına dönüştür
    takim_ad = takim_ad.replace("ı", "i") 
    takim_ad = takim_ad.replace("ç", "c") 
    takim_ad = takim_ad.replace("ş", "s") 
    takim_ad = takim_ad.replace("ğ", "g") 
    takim_ad = takim_ad.replace("ü", "u") 
    takim_ad = takim_ad.replace("ö", "o") 
    return takim_ad.replace(" ", "-")  # Boşlukları '-' ile değiştir

def tahmini_mac_sonucu(gol_tahmini):
    takim1_gol = int(gol_tahmini)  # İlk takım için gol sayısı
    takim2_gol = takim1_gol - 1 if takim1_gol > 0 else 0  # İkinci takımın gol sayısını belirle (ilk takımdan 1 eksik)
    takim1 = turkce_karakter_degistir(takim1_entry.get())  # Ev sahibi takım ismini al ve Türkçe karakterleri değiştir
    takim2 = turkce_karakter_degistir(takim2_entry.get())  # Deplasman takım ismini al ve Türkçe karakterleri değiştir
    return f"Tahmini maç sonucu: {takim1.capitalize()} {takim1_gol} - {takim2_gol} {takim2.capitalize()}"  # Tahmini maç sonucunu döndür

def iki_takimli_analiz():
    takim1 = turkce_karakter_degistir(takim1_entry.get())  # Ev sahibi takım ismini al ve Türkçe karakterleri değiştir
    takim2 = turkce_karakter_degistir(takim2_entry.get())  # Deplasman takım ismini al ve Türkçe karakterleri değiştir
    mac_sayisi = int(mac_sayisi_entry.get())  # Gol tahmini için kullanılacak son maç sayısını al

    if not takim1 or not takim2:
        messagebox.showerror("Hata", "Lütfen takımları girin.")  # Takım ismi girilmemişse hata mesajı
        return
    sonuc = ""
    takim1_bilgilerini_cek = takim_bilgilerini_cek(takim1)  # Ev sahibi takım bilgilerini çek
    if takim1_bilgilerini_cek is None:
        return
    galibiyet_sayisi_g1, gol_sayisi_g1, son_mac_skoru_g1 = takim1_bilgilerini_cek  # Ev sahibi takımın bilgilerini ayır
    takim2_bilgilerini_cek = takim_bilgilerini_cek(takim2)  # Deplasman takım bilgilerini çek
    if takim2_bilgilerini_cek is None:
        return
    galibiyet_sayisi_g2, gol_sayisi_g2, son_mac_skoru_g2 = takim2_bilgilerini_cek  # Deplasman takımının bilgilerini ayır

    sonuc += f"{takim1.capitalize()}\nGalibiyet Sayısı:{galibiyet_sayisi_g1}\nGol Sayısı:{gol_sayisi_g1}\n{son_mac_skoru_g1}\n\n"  # Ev sahibi takım bilgilerini ekle
    sonuc += f"{takim2.capitalize()}\nGalibiyet Sayısı:{galibiyet_sayisi_g2}\nGol Sayısı:{gol_sayisi_g2}\n{son_mac_skoru_g2}\n\n"  # Deplasman takım bilgilerini ekle

    if galibiyet_sayisi_g1 is not None and galibiyet_sayisi_g2 is not None:
        if galibiyet_sayisi_g1 > galibiyet_sayisi_g2:
            sonuc += f"{takim1.capitalize()} Takımı {takim2.capitalize()} simülasyona göre yendi!\n"  # Ev sahibi takım galip
        elif galibiyet_sayisi_g1 < galibiyet_sayisi_g2:
            sonuc += f"{takim2.capitalize()} Takımı {takim1.capitalize()} simülasyona göre yendi!\n"  # Deplasman takım galip
        else:
            sonuc += f"İki takım arasındaki maç simülasyona göre berabere bitti\n"  # Beraberlik durumu
            
    # Gol sayısı tahmini
    if galibiyet_sayisi_g1 is not None and galibiyet_sayisi_g2 is not None:
        takim1_son_mac_gol = son_mac_bilgilerini_cek(takim1, mac_sayisi)  # Ev sahibi takımın son maçlarından gol bilgisi al
        takim2_son_mac_gol = son_mac_bilgilerini_cek(takim2, mac_sayisi)  # Deplasman takımının son maçlarından gol bilgisi al

        if len(takim1_son_mac_gol) < mac_sayisi or len(takim2_son_mac_gol) < mac_sayisi:
            messagebox.showerror("Hata", "Gol tahmini yapmak için yeterli veri bulunamadı.")  # Yeterli veri yoksa hata
            return
            
        ortalama_gol_takim1 = sum(takim1_son_mac_gol) / len(takim1_son_mac_gol)  # Ev sahibi takımın ortalama golü
        ortalama_gol_takim2 = sum(takim2_son_mac_gol) / len(takim2_son_mac_gol)  # Deplasman takımının ortalama golü

        # Tahmin edilen gol sayısını hesapla
        ortalama_gol = (ortalama_gol_takim1 + ortalama_gol_takim2) / 2  # Ortalama gol
        gol_tahmini = ortalama_gol + 0.25 if takim1_son_mac_gol[-1] > takim2_son_mac_gol[-1] else ortalama_gol  # Gol tahmini

        sonuc += f"Maçta Muhtemelen {gol_tahmini:.2f} gol olacak.\n"  # Gol tahminini ekle

        # Maç sonucunu tahmin et
        tahmini_sonuc = tahmini_mac_sonucu(gol_tahmini)  # Tahmin edilen maç sonucunu al
        sonuc += tahmini_sonuc  # Sonucu ekle
        
    sonuc_label.config(text=sonuc)  # Sonucu arayüzde göster

def son_mac_bilgilerini_cek(takim, mac_sayisi):
    url = f"https://www.sporx.com/{takim}-fiksturu-ve-mac-sonuclari"  # Son maç verilerini çekmek için URL
    response = requests.get(url)  # URL'ye istek gönder
    soup = BeautifulSoup(response.content, "html.parser")  # Gelen HTML'yi parse et
    maclar = soup.find_all("tr")  # Maçları içeren tüm satırları bul
    son_mac_gol_sayilari = []  # Son maç gol sayılarının tutulacağı liste
    mac_sayaci = 0  # Maç sayacı

    for mac in maclar:  # Maçları kontrol et
        skor_element = mac.find("a", class_="d-block rounded bg-sporx text-white fw-bolder py-1 px-1 text-nowrap")  # Skor elementini bul
        if skor_element:  # Eğer skor varsa
            skor = skor_element.get_text(strip=True)  # Skoru al
            gol_sayisi = skor.split("-")  # Skoru iki takıma ayır
            if len(gol_sayisi) == 2 and gol_sayisi[0].strip() and gol_sayisi[1].strip():  # Skor geçerliyse
                try:
                    gol_sayisi_g1 = int(gol_sayisi[0])  # Ev sahibi takımın gol sayısı
                    gol_sayisi_g2 = int(gol_sayisi[1])  # Deplasman takımının gol sayısı
                    son_mac_gol_sayilari.append(gol_sayisi_g1)  # Gol sayısını ekle
                    son_mac_gol_sayilari.append(gol_sayisi_g2)
                    mac_sayaci += 1  # Maç sayacını arttır
                except ValueError:
                    continue  # Skor geçersizse, bir sonraki maça geç
                if mac_sayaci >= mac_sayisi:  # İstenilen maç sayısına ulaşılırsa dur
                    break
    return son_mac_gol_sayilari

def analiz_kaydet():
    analiz_text = sonuc_label.cget("text")  # Sonuç metnini al
    if not analiz_text:
        messagebox.showerror("Hata", "Analiz yapılmadı.")  # Eğer analiz yapılmamışsa hata mesajı göster
        return
    with open("takim_analizi.txt", "w") as f:  # Analizi kaydetmek için dosya aç
        f.write(analiz_text)  # Analizi dosyaya yaz
    messagebox.showinfo("Başarılı", "Analiz başarıyla kaydedildi.")  # Başarı mesajı

# Tkinter penceresini başlat
root = tk.Tk()
root.title("Futbol Takım Analiz Aracı")  # Başlık
root.iconbitmap('btc.ico')  # İkon ekleme

# Arka plan rengini ayarlayın
root.config(bg="#f0f0f0")  # Pencere arka plan rengini açık gri olarak ayarlıyoruz

# Başlangıçta bulunan etiketler ve giriş kutuları
takim1_label = tk.Label(root, text="Ev Sahibi Takım:", bg="#f0f0f0", font=("Arial", 12))
takim1_label.pack(padx=10, pady=10)

takim1_entry = tk.Entry(root, font=("Arial", 12))
takim1_entry.pack(padx=10, pady=5)

takim2_label = tk.Label(root, text="Deplasman Takım:", bg="#f0f0f0", font=("Arial", 12))
takim2_label.pack(padx=10, pady=10)

takim2_entry = tk.Entry(root, font=("Arial", 12))
takim2_entry.pack(padx=10, pady=5)

mac_sayisi_label = tk.Label(root, text="Gol Tahmini İçin Son Maç Sayısı:", bg="#f0f0f0", font=("Arial", 12))
mac_sayisi_label.pack(padx=10, pady=10)

mac_sayisi_entry = tk.Entry(root, font=("Arial", 12))
mac_sayisi_entry.insert(0, str(DEFAULT_MAC_SAYISI))  # Varsayılan maç sayısını ekle
mac_sayisi_entry.pack(padx=10, pady=5)

analiz_button = tk.Button(root, text="Analiz Yap", bg="#4CAF50", fg="white", font=("Arial", 12), command=iki_takimli_analiz)
analiz_button.pack(padx=10, pady=20)

sonuc_label = tk.Label(root, text="", bg="#f0f0f0", font=("Arial", 12))
sonuc_label.pack(padx=10, pady=5)

kaydet_button = tk.Button(root, text="Analizi Kaydet", bg="#008CBA", fg="white", font=("Arial", 12), command=analiz_kaydet)
kaydet_button.pack(padx=10, pady=10)

root.mainloop()
