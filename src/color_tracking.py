import cv2
import numpy as np
from collections import deque

# Nesnenin arkasında bırakacağı çizginin geçmiş koordinatlarını tutacak kuyruk (Maksimum 32 nokta)
iz_noktalari = deque(maxlen=32)

# Mavi renk için HSV sınırları
mavi_alt_sinir = np.array([100, 60, 60])
mavi_ust_sinir = np.array([140, 255, 255])

kamera = cv2.VideoCapture(0)

while True:
    kontrol, kare = kamera.read()
    if not kontrol:
        break
        
    kare = cv2.flip(kare, 1)
    bulanik_kare = cv2.GaussianBlur(kare, (11, 11), 0)
    hsv_kare = cv2.cvtColor(bulanik_kare, cv2.COLOR_BGR2HSV)
    
    maske = cv2.inRange(hsv_kare, mavi_alt_sinir, mavi_ust_sinir)
    maske = cv2.erode(maske, None, iterations=2)
    maske = cv2.dilate(maske, None, iterations=2)
    
    # --- YENİ EKLENEN KISIM: KONTUR VE MOMENT HESAPLAMA ---
    
    # Maske ekranındaki beyaz lekelerin sınırlarını (konturlarını) buluyoruz
    konturlar, _ = cv2.findContours(maske.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    merkez = None
    
    # Eğer ekranda en az bir beyaz leke bulunduysa
    if len(konturlar) > 0:
        # Alanı en büyük olan beyaz lekeyi seç (Böylece arkadaki küçük gürültü piksellerini eliyoruz!)
        en_buyuk_kontur = max(konturlar, key=cv2.contourArea)
        
        # Bu büyük lekeyi saran en küçük çemberin koordinatlarını ve yarıçapını hesapla
        ((x, y), yaricap) = cv2.minEnclosingCircle(en_buyuk_kontur)
        
        # Görüntü Momentleri ile beyaz lekenin kütle merkezini (tam orta noktasını) hesaplıyoruz
        M = cv2.moments(en_buyuk_kontur)
        if M["m00"] != 0:
            merkez = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
        # Eğer nesne yeterince büyükse (gürültü değilse) ekrana çizim yap
        if yaricap > 10:
            # Ana kameraya nesneyi saran yeşil bir çember çiz
            cv2.circle(kare, (int(x), int(y)), int(yaricap), (0, 255, 0), 2)
            # Tam merkezine kırmızı küçük bir hedef noktası koy
            cv2.circle(kare, merkez, 5, (0, 0, 255), -1)
            
    # Merkez noktasını takip çizgisi için geçmiş listemize ekliyoruz
    iz_noktalari.appendleft(merkez)
    
    # Arkasında kalan kırmızı izi ekrana çizme döngüsü
    for i in range(1, len(iz_noktalari)):
        if iz_noktalari[i - 1] is None or iz_noktalari[i] is None:
            continue
            
        # Çizginin geçmişe doğru incelmesini sağlayan şık bir kalınlık hesabı
        kalinlik = int(np.sqrt(32 / float(i + 1)) * 2.5)
        # Kırmızı takip çizgisini çiziyoruz
        cv2.line(kare, iz_noktalari[i - 1], iz_noktalari[i], (0, 0, 255), kalinlik)
        
    # Pencereleri göster
    cv2.imshow("Canli Kamera Goruntusu", kare)
    cv2.imshow("Bilgisayarin Gordugu (Maske)", maske)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()