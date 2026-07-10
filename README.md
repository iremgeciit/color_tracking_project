# 🎯 Canlı Kamera Üzerinden Renk Tabanlı Nesne Takibi

Bu proje, **Python** ve **OpenCV** kullanarak belirli bir renkteki (örneğin mavi) nesneleri canlı kamera görüntüsü veya statik resimler üzerinden gerçek zamanlı olarak takip etmeyi amaçlar.

---

## 🚀 Kullanılan Teknolojiler & Teknikler

- **HSV Renk Uzayı:** Işık değişimlerinden etkilenmeden renk tespiti.
- **Maskeleme (Thresholding):** Hedef rengi arka plandan ayırma.
- **Morfolojik İşlemler:** Görüntüdeki küçük gürültüleri temizleme.
- **Görüntü Momentleri:** Nesnenin kütle merkezini (X, Y) hesaplama.

---

## 🛠️ Kurulum

```bash
pip install -r requirements.txt
```

---

## 🎯 Bu Proje Tam Olarak Neyi Amaçlıyor?

> **Bilgisayara karmaşık, renkli ve gürültülü bir dünyadan yalnızca ilgilendiği nesneyi ayıklamayı öğretmektir.**

İnsan gözü odaya baktığında masayı, duvarı, yüzleri ve elindeki mavi kalemi saniyeler içinde ayırt eder. Bilgisayar ise yalnızca milyonlarca piksel görür.

Bu projede bilgisayara şu üç temel komut öğretilir:

1. **Dünyayı Basitleştir**
   - Görüntüyü HSV renk uzayına çevir.
   - Işık değişimlerinden etkilenme.

2. **Sadece Hedefe Odaklan**
   - Seçilen renk dışındaki tüm pikselleri siyah yap.
   - Hedef nesneyi beyaz olarak bırak.

3. **Merkezi Bul**
   - Nesnenin merkez koordinatını (X, Y) hesapla.
   - Bu noktaya hedef işareti çiz.

---

## ⚙️ İşlem Akışı

```
Kameradan Kare Al
        ↓
BGR → HSV Dönüşümü
        ↓
Renk Maskesi Oluştur
        ↓
Morfolojik Temizlik
        ↓
Kontur Bul
        ↓
Moment Hesapla
        ↓
Merkez Noktasını Çiz
```

---

## ❓ Neden BGR Değil de HSV?

OpenCV görüntüleri varsayılan olarak **BGR (Blue, Green, Red)** formatında okur.

Ancak gerçek hayatta ışık şiddeti değiştikçe aynı nesnenin BGR değerleri de önemli ölçüde değişebilir. Bu durum renk tabanlı tespiti zorlaştırır.

HSV renk uzayı ise rengi parlaklıktan ayırır.

- **Hue (H):** Gerçek renk bilgisi
- **Saturation (S):** Rengin doygunluğu
- **Value (V):** Parlaklık

Bu sayede sistem farklı ışık koşullarında bile aynı rengi daha güvenilir şekilde algılar.

---

## 📷 Sonuçlar

### 1️⃣ Uzaktan Takip

Nesne uzaktayken ve görüntüde daha büyük başka bir mavi alan bulunduğunda sistem en büyük alana odaklanır.

![Uzaktan Takip](outputs/uzak_takip.png)

---

### 2️⃣ Yakından Takip

Mavi nesne kameraya yaklaştırıldığında sistem yeni en büyük alanı hedef olarak seçer ve merkezini takip eder.

![Yakından Takip](outputs/yakin_takip.png)
