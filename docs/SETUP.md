# Kurulum Kılavuzu

## Gereksinimler

- Python 3.9+
- PostgreSQL 13+ (opsiyonel - production için)
- Redis 6+ (opsiyonel - production için)
- Groq API Key (ücretsiz - https://console.groq.com/)

## Adım 1: Repository'yi Klonlayın

```bash
git clone https://github.com/yourcompany/compagent.git
cd compagent
```

## Adım 2: Virtual Environment Oluşturun

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

## Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

## Adım 4: Ortam Değişkenlerini Ayarlayın

`.env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Groq API
GROQ_API_KEY=gsk-your-actual-groq-api-key-here
GROQ_MODEL=llama-3.1-8b-instant

# Database (opsiyonel - development'ta gerekli değil)
DATABASE_URL=postgresql://compagent_user:your_password@localhost:5432/compagent_db

# Redis (opsiyonel - development'ta gerekli değil)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=generate-a-secure-random-key-here
ALGORITHM=HS256

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Groq API Key Alma

1. [Groq Console](https://console.groq.com/) adresine gidin
2. Ücretsiz hesap oluşturun
3. **API Keys** bölümünden yeni key oluşturun
4. Key'i kopyalayın ve `.env` dosyasına yapıştırın

## Adım 5: Veritabanı Kurulumu

### PostgreSQL Kurulumu

#### Windows
1. PostgreSQL'i indirin: https://www.postgresql.org/download/windows/
2. Kurulumu yapın ve şifre belirleyin

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Mac (Homebrew)
```bash
brew install postgresql
brew services start postgresql
```

### Veritabanı Oluşturma

```bash
# PostgreSQL'e bağlan
psql -U postgres

# Veritabanı ve kullanıcı oluştur
CREATE DATABASE compagent_db;
CREATE USER compagent_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE compagent_db TO compagent_user;

# Çıkış
\q
```

## Adım 6: Redis Kurulumu

### Windows
1. Redis'i WSL üzerinden veya Docker ile kurun:

```bash
docker run -d -p 6379:6379 redis:latest
```

### Linux (Ubuntu/Debian)
```bash
sudo apt install redis-server
sudo systemctl start redis-server
```

### Mac (Homebrew)
```bash
brew install redis
brew services start redis
```

### Redis Test
```bash
redis-cli ping
# Yanıt: PONG
```

## Adım 7: Uygulamayı Başlatın

### Geliştirme Modu

```bash
python main.py
```

API şu adreste çalışacaktır: http://localhost:8000

### API Dokümantasyonu

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

## Adım 8: Test Edin

### Health Check

```bash
curl http://localhost:8000/health
```

### Test Chat İsteği

```bash
curl -X POST http://localhost:8000/api/v1/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "prod_1",
    "message": "Bu ürün hakkında bilgi verir misiniz?"
  }'
```

## Production Deployment

### Uvicorn ile Production

```bash
pip install gunicorn

gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Docker ile Deployment

```bash
# Docker image oluştur
docker build -t compagent:latest .

# Container çalıştır
docker run -d \
  --name compagent \
  -p 8000:8000 \
  --env-file .env \
  compagent:latest
```

### Docker Compose ile

```bash
docker-compose up -d
```

## Sorun Giderme

### OpenAI API Hatası

```
Error: OpenAI API key not configured
```

**Çözüm**: `.env` dosyasında `OPENAI_API_KEY` değerini kontrol edin.

### Database Connection Error

```
Error: could not connect to server
```

**Çözüm**: 
1. PostgreSQL'in çalıştığından emin olun
2. `DATABASE_URL`'in doğru olduğunu kontrol edin
3. Firewall ayarlarını kontrol edin

### Redis Connection Error

```
Error: Error connecting to Redis
```

**Çözüm**:
1. Redis'in çalıştığından emin olun: `redis-cli ping`
2. `REDIS_URL`'i kontrol edin

### Port Zaten Kullanımda

```
Error: [Errno 48] Address already in use
```

**Çözüm**:
1. Başka bir port kullanın: `.env` dosyasında `API_PORT=8001`
2. Veya çalışan uygulamayı durdurun

## Sonraki Adımlar

1. [API Dokümantasyonu](API.md) okuyun
2. [Entegrasyon Kılavuzu](INTEGRATION.md) inceleyin
3. [Kullanım Örnekleri](EXAMPLES.md) göz atın

## Destek

Sorunlarınız için:
- GitHub Issues: https://github.com/yourcompany/compagent/issues
- Email: support@compagent.com
- Docs: https://docs.compagent.com
