# Onvo
**Agent Üretim Platformu**

## 🎯 Proje Amacı
Bu platform, üçüncü taraf SaaS ürünlerini satan şirketlerin uygulamalarına entegre edilebilen akıllı bir agent üretim platformudur. Üretilen agentlar:
- Ürünü derinlemesine bilir
- Ürünün kullanıcı girdisiyle kullanımını sağlar
- Müşteri sorularını anlık yanıtlar
- Kullanıcı girdilerine göre yapılandırma önerir
- Satış sürecini hızlandırır
- Entegrasyon ve API konularını açıklar
- Çoklu müşteri (multi-tenant) yapısını destekler

## 🏗️ Mimari
```
SaaS Uygulaması ──> REST / WebSocket
        │
        ▼
┌────────────────────────────┐
│        Agent Platform      │
│  ├─ Knowledge Base         │  (Vektör Arama / Ürün Dokümanları)
│  ├─ Q&A Engine             │  (Retrieval + LLM)
│  ├─ Config Manager         │  (Özelleştirme Akışı)
│  ├─ Product Handler        │  (Ürün Operasyonları)
│  ├─ Session + Multi-tenant │
│  └─ Analytics + Logging    │
└────────────────────────────┘
```

## 📁 Proje Yapısı
```
Onvo/
├── agent/                 # Agent çekirdeği
│   ├── knowledge_base/    # Ürün bilgi yönetimi
│   ├── qa_engine/         # Soru-cevap motoru
│   ├── config_manager/    # Ürün konfigürasyon yönetimi
│   └── product_handler/   # Ürün işlemleri
├── api/                   # FastAPI servisleri
├── integrations/          # SaaS entegrasyon adaptörleri
├── models/                # Veri modelleri / ORM
├── tests/                 # Testler
├── docs/                  # Ek dokümantasyon
└── README.md
```

## ✅ Özellikler
- Multi-tenant yapı
- Özelleştirilebilir bilgi tabanı
- Gerçek zamanlı chat (WebSocket)
- API tabanlı entegrasyon
- Analytics ve raporlama
- Rate limiting + API Key auth
- Cache / hızlandırma (Redis)
- Vektör tabanlı bilgi erişimi

## 🔧 Teknoloji Stack
| Katman        | Teknoloji |
|---------------|-----------|
| Backend       | Python, FastAPI |
| LLM / AI      | Groq API (Llama 3.1 8B Instant) |
| Veri          | PostgreSQL |
| Vektör Arama  | (Seçilebilir: PGVectoR / Qdrant / Chroma) |
| Cache         | Redis |
| İletişim      | REST + WebSocket |
| Test          | Pytest |
| Ortam         | .env yapılandırması |

## 📦 Gereksinimler
- Python 3.10+
- PostgreSQL
- Redis
- Groq API Key

## 🚀 Kurulum
```bash
# Depoyu klonla
git clone https://github.com/your-org/compagent.git
cd compagent

# Sanal ortam
python -m venv .venv
.\.venv\Scripts\activate

# Bağımlılıklar
pip install -r requirements.txt
```

### Ortam Değişkenleri (.env)
```
GROQ_API_KEY=xxx
DATABASE_URL=postgresql://user:pass@localhost:5432/compagent
REDIS_URL=redis://localhost:6379/0
APP_ENV=development
LOG_LEVEL=info
```

### Groq Doğrulama
```bash
python test_groq.py
```

### Geliştirme Sunucusu
```bash
python main.py
# veya
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```
API Dokümantasyon: http://localhost:8000/docs

## 🧪 Test Çalıştırma
```bash
pytest -q
pytest --maxfail=1 --disable-warnings -q
```

## 🔌 Örnek API Kullanımı

### 1. Agent Listesi
```bash
curl -H "X-API-KEY: YOUR_KEY" http://localhost:8000/api/v1/agents
```

### 2. Soru-Cevap (Chat)
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: YOUR_KEY" \
  -d '{"session_id":"abc123","message":"Fiyatlandırma nasıl çalışıyor?"}'
```

### 3. Ürün Bilgisi Ekleme
```bash
curl -X POST http://localhost:8000/api/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{"product_id":"prod_1","content":"Yeni entegrasyon detayları..."}'
```

### 4. WebSocket Chat (Örnek)
```python
import websockets, asyncio, json

async def run():
    async with websockets.connect("ws://localhost:8000/ws/chat?session_id=abc123") as ws:
        await ws.send(json.dumps({"message": "Merhaba, paket önerisi?"}))
        msg = await ws.recv()
        print(msg)

asyncio.run(run())
```

## 🧩 Kullanım Senaryoları
1. Ürün Tanıtımı: Özellik ve değer önerisi açıklama
2. Teknik Destek: API entegrasyon adımları
3. Demo / Özelleştirme: Kullanıcı girdisine göre yapılandırma
4. Satış Yardımı: Paket seçimi, fiyat açıklama
5. Eğitim / Onboarding: Yeni kullanıcı yönlendirme


## 👥 Ekip
| Mehmet Ali Akar | meakar@matreus.com |
| Resül Dinç | rdinc@matreus.com |
| Utku Aydın | uaydin@matreus.com |


## 📧 İletişim
info@matreus.com
