# TasarBot - Proje Analiz Asistanı 🤖

TasarBot, üniversite öğrencilerinin proje geliştirme süreçlerinde karşılaştıkları temel zorlukları aşmalarına yardımcı olmak için tasarlanmış yapay zeka destekli bir komut satırı asistanıdır.

## 🌟 Özellikler

- Risk analizi ve planlama desteği
- Kaynak yönetimi önerileri
- Potansiyel sorunları önceden belirleme
- SWOT analizi
- Zaman çizelgesi oluşturma
- Proje yol haritası planlama

## 💻 Gereksinimler

- Python 3.12+
- SQLite3
- Anthropic API Anahtarı

## 🚀 Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/cherdukay/tasarbot.git
cd tasarbot
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

4. 

.env

 dosyası oluşturun ve API anahtarınızı ekleyin:
```
ANTHROPIC_API_KEY=your-api-key-here
```

## 📘 Kullanım

Programı başlatmak için:
```bash
python src/main.py
```

## 🔍 Ana Menü Seçenekleri

1. Yeni Proje Oluştur
2. Proje Yükle
3. Analiz Yap
4. Mevcut Projeyi Görüntüle
5. Projeyi Kaydet
6. Çıkış

## 🗃️ Veri Saklama

Tüm proje verileri SQLite veritabanında 

tasarbot.db

 konumunda saklanır.

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.