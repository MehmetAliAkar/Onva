# SaaS Product Agent Platform

**Akıllı Ürün Satış ve Destek Agent'ı**

## 🎯 Proje Amacı

Bu platform, üçüncü taraf uygulamaları satan SaaS şirketlerine entegre edilebilen akıllı bir agent çözümüdür. Agent:

- ✅ Satılan ürünü derinlemesine bilir
- ✅ Müşteri sorularını anlık cevaplayabilir
- ✅ Kullanıcı girdilerine göre ürünü özelleştirir
- ✅ Satış sürecini hızlandırır ve otomatikleştirir

## 🏗️ Mimari

```
┌─────────────────┐
│  SaaS Platform  │
└────────┬────────┘
         │ API
    ┌────▼─────────────────┐
    │  Agent Platform      │
    │  ├─ Knowledge Base   │
    │  ├─ Q&A Engine       │
    │  ├─ Config Manager   │
    │  └─ Product Handler  │
    └──────────────────────┘
```

## 📁 Proje Yapısı

```
Compagent/
├── agent/                 # Agent çekirdeği
│   ├── knowledge_base/    # Ürün bilgi yönetimi
│   ├── qa_engine/         # Soru-cevap motoru
│   ├── config_manager/    # Ürün konfigürasyon yönetimi
│   └── product_handler/   # Ürün işlemleri
├── api/                   # REST API
├── integrations/          # SaaS platform entegrasyonları
├── models/                # Veri modelleri
├── tests/                 # Test dosyaları
└── docs/                  # Dokümantasyon
```

## 🚀 Hızlı Başlangıç

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Groq API Key alın: https://console.groq.com/
# .env dosyasını düzenleyin ve GROQ_API_KEY ekleyin

# Groq bağlantısını test edin
python test_groq.py

# Geliştirme sunucusunu başlat
python main.py

# API dokümantasyonu
http://localhost:8000/docs
```

**Detaylı kurulum için**: [QUICKSTART.md](QUICKSTART.md) (5 dakika)

## 💼 Kullanım Senaryoları

### 1. Ürün Tanıtımı
Agent, potansiyel müşterilere ürün özelliklerini detaylı anlatır.

### 2. Teknik Sorular
Entegrasyon, API kullanımı gibi teknik soruları cevaplayabilir.

### 3. Özelleştirme ve Demo
Müşteri ihtiyaçlarına göre ürünü anında yapılandırır ve demo sunar.

### 4. Satış Desteği
Fiyatlandırma, paket seçimi gibi konularda yardımcı olur.

## 🔧 Teknoloji Stack

- **Backend**: Python (FastAPI)
- **AI/ML**: Groq API (Llama 3.1 8B Instant)
- **Database**: PostgreSQL / Vector DB
- **Cache**: Redis
- **API**: REST, WebSocket

## 📊 Özellikler

- [x] Multi-tenant yapı (birden fazla SaaS müşterisi)
- [x] Özelleştirilebilir ürün bilgi tabanı
- [x] Doğal dil işleme (NLP)
- [x] Gerçek zamanlı chat desteği
- [x] API tabanlı entegrasyon
- [x] Analytics ve raporlama

## 🔐 Güvenlik

- API Key authentication
- Rate limiting
- Data encryption
- GDPR compliant

## 📝 Lisans

MIT License

## 📧 İletişim

Daha fazla bilgi için: info@compagent.com
