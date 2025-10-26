# Onva – Agent Üretim Platformu

SaaS ürünleri için akıllı destek ve konfigurasyon agent'ları oluşturmanızı sağlayan platform.

---

## 1. 📘 Proje Açıklaması & Amacı

Onvo; SaaS ürünlerini yöneten veya satan şirketlerin uygulamalarına kolayca entegre edilebilen, ürün bilgisini öğrenen ve son kullanıcıyla etkileşime giren akıllı agent'lar üretmek için tasarlanmış bir platformdur.

### Neler Sağlar?

- Ürün özellikleri ve dokümantasyonu üzerinden bilgi edinme
- Gerçek zamanlı soru-cevap (chat) deneyimi
- Kullanıcı girdisine göre yapılandırma ve entegrasyon yönlendirmesi
- Satış sürecinde paket / fiyat önerisi
- API ve entegrasyon adımlarını açıklama
- Çoklu müşteri (multi-tenant) veri izolasyonu

### Fark Yaratan Özellikler

- Vektör tabanlı semantik bilgi erişimi
- Özelleştirilebilir persona ve rol tanımları
- Doküman + API endpoint + persona yönetimi tek ekranda
- Guidance Agentlar yerine aksiyon alabilen agent

---

## 2. 🛠 Kurulum (Installation)

### Gereksinimler

- Python 3.10+
- PostgreSQL
- Redis
- Groq API Key

### Depoyu Klonla

```bash
git clone https://github.com/your-org/onvo.git
cd onvo
```

### Sanal Ortam ve Bağımlılıklar

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### Ortam Değişkenleri (.env Örneği)

```env
GROQ_API_KEY=xxx
DATABASE_URL=postgresql://user:pass@localhost:5432/onvo
REDIS_URL=redis://localhost:6379/0
APP_ENV=development
LOG_LEVEL=info
SECRET_KEY=change_me_dev
```

### Çalıştırma

```bash
python main.py
# veya
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Dokümantasyon: [http://localhost:8000/docs](http://localhost:8000/docs)

### Testler

```bash
pytest -q
pytest --maxfail=1 --disable-warnings -q
```

---

## 3. 🚀 Kullanım Rehberi (Usage Guide)

### Temel Akış

1. Yeni agent oluştur: Persona + açıklama ekle
2. Ürün dokümanlarını yükle
3. API endpoint'lerini tanımla (metod, URL, istek/yanıt örnekleri)
4. Agent'ı chat arayüzünden test et
5. Gerekirse güncelle / sil



### Örnek API İstekleri

Agent Listesi:

```bash
curl http://localhost:8000/api/v1/agents
```

Yeni Agent Oluşturma:

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name":"Destek Agentı","description":"Müşteri destek soruları","persona_role":"support"}'
```

Chat Mesajı Gönderme:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"s1","message":"Fiyatlandırma nasıl?"}'
```

WebSocket Chat Örneği:

```python
import websockets, asyncio, json

async def run():
    async with websockets.connect("ws://localhost:8000/ws/chat?session_id=s1") as ws:
        await ws.send(json.dumps({"message": "Merhaba!"}))
        print(await ws.recv())

asyncio.run(run())
```

### Kullanım Senaryoları

- Satış destek & paket önerisi
- Teknik entegrasyon rehberliği
- Ürün konfigürasyonu yönlendirme
- Onboarding / eğitim
- Self-servis destek

---

## 4. 🔧 Teknolojiler (Technologies Used)

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python (FastAPI) |
| AI / LLM | Groq API (Llama 3.1 8B Instant) |
| Veri | PostgreSQL |
| Vektör Arama | ChromaDB (opsiyonel: Qdrant / PGVector) |
| Cache | Redis |
| İletişim | REST + WebSocket |
| Test | Pytest |
| Ortam | pydantic-settings / .env |

### Mimarinin Özeti

```text
Client ─ REST / WS ─> FastAPI ──> Groq API
                 │
                 ├─ Vector Store (Chroma)
                 ├─ Document Processing
                 ├─ Endpoint Registry
                 └─ Persona / Prompt Yönetimi
```

---

## 5. 👥 Matreus Team Members

| Mehmet Ali Akar|
| Resül Dinç|
| Utku Aydın|

---

## 📩 İletişim

Sorularınız için: [info@matreus.com](mailto:info@matreus.com)

---

![test](image.png)