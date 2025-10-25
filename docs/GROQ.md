# Groq API Kullanımı

Bu proje **Groq API** ve **Llama 3.1 8B Instant** modelini kullanır.

## Groq API Key Alma

1. [Groq Console](https://console.groq.com/) adresine gidin
2. Hesap oluşturun veya giriş yapın
3. **API Keys** bölümünden yeni bir key oluşturun
4. Key'i kopyalayın

## Kurulum

### 1. Groq API Key'i Ayarlayın

`.env` dosyasını düzenleyin:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### 2. Bağımlılıkları Yükleyin

```powershell
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın

```powershell
python main.py
```

## Groq Avantajları

✅ **Hız**: OpenAI'dan 10-20x daha hızlı yanıt süresi  
✅ **Maliyet**: Daha uygun fiyatlandırma  
✅ **Llama 3.1**: Meta'nın güçlü açık kaynak modeli  
✅ **Rate Limit**: Yüksek istek limitleri

## Model Seçenekleri

Groq'ta kullanabileceğiniz diğer modeller:

```env
# Hızlı ve verimli (önerilen)
GROQ_MODEL=llama-3.1-8b-instant

# Daha güçlü, biraz daha yavaş
GROQ_MODEL=llama-3.1-70b-versatile

# Büyük context window
GROQ_MODEL=llama-3.1-405b-reasoning

# Mixtral alternatifi
GROQ_MODEL=mixtral-8x7b-32768
```

## Örnek Kullanım

```python
from groq import Groq
from core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

response = client.chat.completions.create(
    model=settings.GROQ_MODEL,
    messages=[
        {"role": "system", "content": "Sen bir SaaS satış uzmanısın."},
        {"role": "user", "content": "Ürününüz hakkında bilgi alabilir miyim?"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

## Rate Limits (Free Tier)

- **Llama 3.1 8B**: 30 requests/minute, 7,000 requests/day
- **Llama 3.1 70B**: 30 requests/minute, 7,000 requests/day
- **Context Window**: 8,192 tokens (Llama 3.1 8B)

## Fiyatlandırma

Groq şu anda **ücretsiz** API erişimi sunuyor! 

Production kullanımı için [Groq Pricing](https://console.groq.com/settings/billing) sayfasını kontrol edin.

## Sorun Giderme

### API Key Hatası

```
Error: Invalid API Key
```

**Çözüm**: `.env` dosyasındaki `GROQ_API_KEY` değerini kontrol edin.

### Rate Limit Hatası

```
Error: Rate limit exceeded
```

**Çözüm**: 
1. Bir dakika bekleyin
2. Request'lerinizi throttle edin
3. Groq Dashboard'dan limitinizi kontrol edin

### Model Bulunamadı

```
Error: Model not found
```

**Çözüm**: `.env` dosyasında `GROQ_MODEL` değerini kontrol edin. Desteklenen modeller:
- `llama-3.1-8b-instant`
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

## Daha Fazla Bilgi

- **Groq Docs**: https://console.groq.com/docs
- **Groq Discord**: https://discord.gg/groq
- **Llama 3.1 Info**: https://ai.meta.com/blog/meta-llama-3-1/

## Migrasyon Notları

Bu proje başlangıçta OpenAI için tasarlanmıştı. Groq'a geçişte yapılan değişiklikler:

### Değişen Dosyalar:
- ✅ `requirements.txt` - Groq paketi eklendi
- ✅ `core/config.py` - Groq ayarları eklendi
- ✅ `agent/qa_engine/qa_processor.py` - Groq client kullanımı
- ✅ `agent/config_manager/config_handler.py` - Groq client kullanımı
- ✅ `.env` - Groq API key ayarı

### API Uyumluluğu:
Groq, OpenAI-compatible API kullanır, bu yüzden kod değişiklikleri minimal:
- `AsyncOpenAI` → `Groq`
- `OPENAI_API_KEY` → `GROQ_API_KEY`
- `OPENAI_MODEL` → `GROQ_MODEL`

Tüm diğer fonksiyonalite aynı kalır! 🚀
