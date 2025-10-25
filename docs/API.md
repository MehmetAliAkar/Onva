# SaaS Product Agent - API Dokümantasyonu

## API Endpoint'leri

### Agent Endpoints

#### 1. Chat with Agent
**POST** `/api/v1/agent/chat`

Müşteri soruları ve ürün bilgisi talebi için kullanılır.

**Request Body:**
```json
{
  "product_id": "prod_123",
  "message": "Bu ürünün fiyatlandırma modelleri nelerdir?",
  "context": {
    "user_type": "enterprise",
    "industry": "fintech"
  },
  "session_id": "session_abc123"
}
```

**Response:**
```json
{
  "response": "Ürünümüzün 3 farklı fiyatlandırma modeli bulunmaktadır...",
  "confidence": 0.92,
  "suggestions": [
    "Entegrasyon seçenekleri nelerdir?",
    "Demo talep edebilir miyim?"
  ],
  "product_config": {
    "recommended_tier": "enterprise"
  }
}
```

#### 2. Configure Product
**POST** `/api/v1/agent/configure`

Kullanıcı gereksinimlerine göre ürün yapılandırması oluşturur.

**Request Body:**
```json
{
  "product_id": "prod_123",
  "user_inputs": {
    "deployment_type": "cloud",
    "scale": "enterprise",
    "features": ["api", "analytics", "reporting"],
    "region": "eu-west-1"
  },
  "requirements": [
    "GDPR uyumluluğu gerekli",
    "5000+ kullanıcı desteği"
  ]
}
```

**Response:**
```json
{
  "product_id": "prod_123",
  "configuration": {
    "deployment": {
      "type": "cloud",
      "region": "eu-west-1",
      "scale": "enterprise"
    },
    "features": {...},
    "security": {...}
  },
  "estimated_price": 499.00,
  "setup_steps": [
    "1. Hesap oluşturma ve API anahtarı alma",
    "2. Gerekli bağımlılıkları yükleme",
    "..."
  ]
}
```

#### 3. Get Product Capabilities
**GET** `/api/v1/agent/product/{product_id}/capabilities`

Ürün özelliklerini ve yeteneklerini getirir.

**Response:**
```json
{
  "product_id": "prod_123",
  "capabilities": [
    "Real-time analytics",
    "Multi-tenant support",
    "API integrations",
    "Custom reporting"
  ]
}
```

#### 4. Analyze Requirements
**POST** `/api/v1/agent/analyze-requirements`

Müşteri gereksinimlerini analiz eder ve uygunluk skoru hesaplar.

**Request Body:**
```json
{
  "product_id": "prod_123",
  "requirements": [
    "10,000+ daily active users",
    "Real-time data processing",
    "GDPR compliance"
  ]
}
```

**Response:**
```json
{
  "product_id": "prod_123",
  "requirements_analysis": "Gereksinimleriniz ürünümüzle yüksek uyumluluk göstermektedir...",
  "recommended_config": {
    "summary": "Enterprise tier önerilir...",
    "full_analysis": "..."
  },
  "compatibility_score": 0.92
}
```

---

### Products Endpoints

#### 5. List Products
**GET** `/api/v1/products/`

Tüm ürünleri listeler.

**Query Parameters:**
- `category` (optional): Kategori filtresi
- `skip` (optional): Sayfa başlangıcı (default: 0)
- `limit` (optional): Sayfa boyutu (default: 100)

**Response:**
```json
[
  {
    "id": "prod_123",
    "name": "Analytics Pro",
    "description": "Advanced analytics platform",
    "category": "analytics",
    "features": [...],
    "pricing_model": "subscription",
    "integration_options": ["REST API", "Webhooks"],
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  }
]
```

#### 6. Create Product
**POST** `/api/v1/products/`

Yeni ürün ekler.

**Request Body:**
```json
{
  "name": "Analytics Pro",
  "description": "Advanced analytics platform for enterprises",
  "category": "analytics",
  "features": [
    "Real-time dashboards",
    "Custom reports",
    "API access"
  ],
  "pricing_model": "subscription",
  "integration_options": ["REST API", "Webhooks", "SDK"],
  "documentation_url": "https://docs.example.com",
  "knowledge_base": {
    "faq": [...],
    "technical_specs": {...}
  }
}
```

#### 7. Get Product
**GET** `/api/v1/products/{product_id}`

Belirli bir ürünü getirir.

#### 8. Update Product
**PUT** `/api/v1/products/{product_id}`

Ürün bilgilerini günceller.

#### 9. Delete Product
**DELETE** `/api/v1/products/{product_id}`

Ürünü siler.

---

### Analytics Endpoints

#### 10. Conversation Metrics
**GET** `/api/v1/analytics/conversations`

Konuşma metriklerini getirir.

**Query Parameters:**
- `start_date`: Başlangıç tarihi
- `end_date`: Bitiş tarihi

**Response:**
```json
{
  "total_conversations": 1250,
  "avg_conversation_length": 5.8,
  "avg_response_time": 1.2,
  "satisfaction_rate": 0.92
}
```

#### 11. Product Metrics
**GET** `/api/v1/analytics/products/{product_id}`

Ürün bazlı metrikleri getirir.

**Query Parameters:**
- `days`: Gün sayısı (default: 30)

**Response:**
```json
{
  "product_id": "prod_123",
  "total_inquiries": 456,
  "configuration_requests": 89,
  "conversion_rate": 0.35,
  "top_questions": [
    "Pricing information",
    "Integration options",
    "..."
  ]
}
```

#### 12. Agent Performance
**GET** `/api/v1/analytics/agent/performance`

Agent performans metriklerini getirir.

**Response:**
```json
{
  "total_interactions": 3450,
  "successful_resolutions": 3120,
  "escalations": 89,
  "avg_confidence_score": 0.87,
  "response_accuracy": 0.91
}
```

#### 13. Dashboard Summary
**GET** `/api/v1/analytics/dashboard`

Dashboard özet bilgilerini getirir.

---

## Kimlik Doğrulama

Tüm API istekleri için API Key gereklidir:

```bash
curl -H "X-API-Key: your_api_key_here" \
  https://api.compagent.com/api/v1/agent/chat
```

## Rate Limiting

- **Limit**: 100 istek / dakika
- **Header**: `X-RateLimit-Remaining`

## Error Responses

```json
{
  "detail": "Error message here"
}
```

**HTTP Status Codes:**
- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error
