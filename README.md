# 🚦 Gerçek Zamanlı Trafik Veri Platformu

Bu proje, TomTom Traffic API üzerinden gerçek zamanlı trafik verilerini toplayan, PostgreSQL üzerinde katmanlı veri mimarisiyle saklayan, dbt ile dönüştüren, Apache Airflow ile otomatikleştiren ve Power BI ile analiz edilebilir hale getiren uçtan uca (End-to-End) bir Data Engineering projesidir.

Projenin temel amacı; gerçek dünyadaki veri mühendisliği süreçlerini modern teknolojiler kullanarak uygulamak ve ölçeklenebilir bir veri hattı (Data Pipeline) oluşturmaktır.

---

## 🏗️ Proje Mimarisi

Projede ELT (Extract, Load, Transform) yaklaşımı benimsenmiştir.

İlk olarak TomTom Traffic API üzerinden trafik verileri Python kullanılarak çekilir. Ham veriler herhangi bir değişiklik yapılmadan PostgreSQL'in Bronze katmanına kaydedilir. Daha sonra dbt modelleri çalıştırılarak veriler temizlenir, dönüştürülür ve analiz için hazır hale getirilir. Son aşamada oluşturulan Gold katmanındaki tablolar Power BI dashboardlarında kullanılır.

```text
TomTom Traffic API
        │
        ▼
Python Veri Toplama
        │
        ▼
PostgreSQL (Bronze)
        │
        ▼
dbt (Silver)
        │
        ▼
dbt (Gold)
        │
        ▼
Power BI Dashboard
```

Bu mimari sayesinde ham veri ile analiz verisi birbirinden ayrılmış, sürdürülebilir ve ölçeklenebilir bir veri platformu oluşturulmuştur.

---

## 🚀 Bu Projede Neler Yapıldı?

- TomTom Traffic API üzerinden gerçek zamanlı trafik verileri toplandı.
- Python kullanılarak veri çekme (Extraction) süreci geliştirildi.
- PostgreSQL üzerinde Bronze, Silver ve Gold katmanlarından oluşan veri ambarı oluşturuldu.
- dbt kullanılarak veri temizleme ve dönüşüm işlemleri gerçekleştirildi.
- Trafik yoğunluğu hesaplandı ve sınıflandırıldı.
- Seyahat gecikmeleri hesaplandı.
- Airflow ile veri hattı otomatik hale getirildi.
- Docker kullanılarak tüm geliştirme ortamı container yapısına taşındı.
- Power BI ile analiz dashboardları oluşturuldu.

---

## 🔄 Veri Akışı

### 1. Veri Toplama

Python uygulaması belirlenen lokasyonlar için TomTom Traffic API'ye istek gönderir.

API'den aşağıdaki bilgiler alınır:

- Güncel hız (Current Speed)
- Serbest akış hızı (Free Flow Speed)
- Güncel seyahat süresi
- Normal seyahat süresi
- Güven skoru (Confidence)
- Yol kapalı bilgisi
- Lokasyon bilgisi
- Veri oluşturulma zamanı

---

### 2. Bronze Katmanı

Bu katmanda API'den gelen ham veri hiçbir işleme tabi tutulmadan PostgreSQL'e kaydedilir.

Amaç;

- Orijinal veriyi korumak
- Ham veri geçmişini saklamak
- Gerektiğinde yeniden işleyebilmek

Örnek tablo:

```
bronze.traffic_raw
```

---

### 3. Silver Katmanı

Bu katmanda dbt kullanılarak veri temizleme ve zenginleştirme işlemleri yapılır.

Gerçekleştirilen işlemler:

- Hatalı hız değerlerinin filtrelenmesi
- Güven skoru düşük kayıtların çıkarılması
- Eksik verilerin temizlenmesi
- Yeni hesaplanan kolonların oluşturulması

Oluşturulan bazı alanlar:

- delay_seconds
- traffic_ratio
- traffic_level

Böylece ham veri analiz edilebilir hale gelir.

---

### 4. Gold Katmanı

Gold katmanı raporlama ve dashboardlar için optimize edilmiş tabloları içerir.

Bu projede oluşturulan modeller:

- fact_traffic_summary
- fact_traffic_history
- fact_traffic_hourly
- fact_traffic_daily

Power BI doğrudan bu tablolar üzerinden beslenmektedir.

---

## 🗄️ Veritabanı Katmanları

### 🥉 Bronze

Ham API verisinin saklandığı katmandır.

Özellikleri:

- Veri değiştirilmez.
- Ham veri korunur.
- Geçmiş kayıtlar tutulur.

---

### 🥈 Silver

Veri temizleme ve dönüşüm katmanıdır.

Bu katmanda;

- Trafik gecikmesi hesaplanır.
- Trafik oranı hesaplanır.
- Trafik seviyesi belirlenir.
- Kalite kontrolleri uygulanır.

---

### 🥇 Gold

Analiz ve raporlama katmanıdır.

Dashboardlarda kullanılan özet tablolar burada oluşturulur.

---

## ⚙️ Veri Dönüşüm Mantığı

dbt modelleri kullanılarak aşağıdaki hesaplamalar yapılmıştır.

### Trafik Gecikmesi

```
delay_seconds =
current_travel_time - free_flow_travel_time
```

---

### Trafik Oranı

```
traffic_ratio =
current_speed / free_flow_speed
```

---

### Trafik Seviyesi

SQL CASE ifadeleri kullanılarak trafik durumu;

- Akıcı
- Orta
- Yoğun

şeklinde sınıflandırılmıştır.

---

## 📊 Sonuç

Bu proje yalnızca API'den veri çekmekten ibaret değildir.

Modern bir Data Engineering yaklaşımıyla;

- Veri toplama
- Veri depolama
- Veri temizleme
- Veri modelleme
- Pipeline orkestrasyonu
- Dashboard hazırlama

süreçlerinin tamamı uçtan uca gerçekleştirilmiştir.

---

## 💡 Bu Projede Kazanılan Data Engineering Yetkinlikleri

- REST API Entegrasyonu
- Python ile Veri Toplama
- PostgreSQL Veri Ambarı
- Bronze / Silver / Gold Mimarisi
- dbt ile SQL Dönüşümleri
- Apache Airflow ile Pipeline Yönetimi
- Docker ile Container Kullanımı
- Veri Kalitesi Kontrolleri
- Analitik Veri Modelleme
- Power BI ile Görselleştirme

---

## 🚀 Gelecekte Yapılabilecek Geliştirmeler

- Kafka ile gerçek zamanlı veri akışı
- Great Expectations ile veri kalite kontrolleri
- GitHub Actions ile CI/CD
- Prometheus & Grafana ile izleme
- AWS üzerinde bulut ortamına taşıma
- Incremental dbt modelleri
- Unit Test ve Integration Test eklenmesi

---
