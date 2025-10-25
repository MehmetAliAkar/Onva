# 🚀 Hızlı Başlangıç (5 Dakika)

Bu kılavuz ile Compagent'ı 5 dakikada çalıştırabilirsiniz!

## Adım 1: Groq API Key Alın (2 dakika)

1. https://console.groq.com/ adresine gidin
2. **Sign Up** ile ücretsiz hesap açın (Google ile giriş yapabilirsiniz)
3. Sol menüden **API Keys** seçin
4. **Create API Key** butonuna tıklayın
5. Key'i kopyalayın (gsk_... ile başlar)

## Adım 2: Projeyi Hazırlayın (2 dakika)

```powershell
# Klasöre gidin
cd C:\Compagent

# Virtual environment aktifleştirin (zaten var)
.\venv\Scripts\Activate.ps1

# Bağımlılıkları yükleyin
pip install groq fastapi uvicorn pydantic pydantic-settings python-dotenv

# .env dosyasını düzenleyin
notepad .env
```

`.env` dosyasında sadece bu satırı güncelleyin:

```env
GROQ_API_KEY=gsk_your_actual_groq_key_here_paste_it
```

Kaydedin ve kapatın.

## Adım 3: Test Edin (1 dakika)

```powershell
# Groq bağlantısını test edin
python test_groq.py
```

✅ "TEST BAŞARILI!" görmelisiniz!

## Adım 4: Sunucuyu Başlatın

```powershell
python main.py
```

Tarayıcınızda açın: http://localhost:8000/docs

## 🎉 Tebrikler!

API'niz hazır! Şimdi test edebilirsiniz:

### Test 1: Health Check

http://localhost:8000/health

### Test 2: Chat Endpoint

Swagger UI'da (http://localhost:8000/docs):

1. **POST /api/v1/agent/chat** endpoint'ini açın
2. **Try it out** butonuna tıklayın
3. Request body'yi düzenleyin:

```json
{
  "product_id": "prod_demo",
  "message": "Merhaba! Ürününüz hakkında bilgi alabilir miyim?",
  "session_id": "test_123"
}
```

4. **Execute** butonuna tıklayın
5. Agent'ın yanıtını görün! 🤖

## Sorun mu var?

### ❌ "GROQ_API_KEY ayarlanmamış" hatası

**Çözüm**: `.env` dosyasında `GROQ_API_KEY=gsk_...` satırını kontrol edin

### ❌ "Import groq could not be resolved" hatası

**Çözüm**:
```powershell
pip install groq
```

### ❌ Port zaten kullanımda

**Çözüm**: `.env` dosyasında port'u değiştirin:
```env
API_PORT=8001
```

### ❌ Rate limit hatası

Groq free tier limitler:
- 30 istek/dakika
- 7,000 istek/gün

1 dakika bekleyin ve tekrar deneyin.

## Sonraki Adımlar

1. ✅ [API Dokümantasyonu](docs/API.md) okuyun
2. ✅ [Entegrasyon Kılavuzu](docs/INTEGRATION.md) inceleyin
3. ✅ [Groq Detayları](docs/GROQ.md) öğrenin
4. ✅ [Örnek Kullanımlar](docs/EXAMPLES.md) deneyin

## Demo Senaryosu

Bir SaaS ürünü ekleyelim:

```python
import requests

# Ürün ekle
response = requests.post(
    "http://localhost:8000/api/v1/products/",
    json={
        "name": "Analytics Pro",
        "description": "Gelişmiş veri analizi platformu",
        "category": "analytics",
        "features": ["Real-time dashboards", "API access", "Custom reports"],
        "pricing_model": "subscription",
        "integration_options": ["REST API", "Webhooks"],
        "knowledge_base": {
            "faq": [
                {
                    "question": "Fiyatı nedir?",
                    "answer": "Basic: $99/ay, Pro: $299/ay, Enterprise: $999/ay"
                }
            ]
        }
    }
)

product = response.json()
print(f"Ürün oluşturuldu: {product['id']}")

# Agent ile konuş
chat_response = requests.post(
    "http://localhost:8000/api/v1/agent/chat",
    json={
        "product_id": product['id'],
        "message": "Fiyatlandırma paketleriniz nelerdir?",
        "session_id": "demo_session"
    }
)

print(f"Agent: {chat_response.json()['response']}")
```

## 🎯 Production'a Geçiş

Development'ta çalıştığınıza göre, production için:

1. PostgreSQL ve Redis kurun
2. `.env` dosyasında connection string'leri güncelleyin
3. `DEBUG=false` yapın
4. Gunicorn ile deploy edin

Detaylar için [SETUP.md](docs/SETUP.md) dosyasını okuyun.

## Yardım

- 💬 Issues: https://github.com/yourcompany/compagent/issues
- 📧 Email: support@compagent.com
- 📚 Docs: docs/ klasörü

Mutlu kodlamalar! 🚀
