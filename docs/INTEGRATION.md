# SaaS Entegrasyon Kılavuzu

Bu kılavuz, Compagent platformunu kendi SaaS uygulamanıza nasıl entegre edeceğinizi gösterir.

## Entegrasyon Yöntemleri

### 1. REST API Entegrasyonu (Önerilen)
### 2. JavaScript SDK
### 3. Webhook'lar
### 4. Embed Widget

---

## 1. REST API Entegrasyonu

### Adım 1: API Key Alın

```bash
# Platform üzerinden API key oluşturun
# Dashboard > Settings > API Keys > Create New Key
```

### Adım 2: Ürün Bilgisi Ekleyin

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "https://api.compagent.com/api/v1"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Yeni ürün ekle
product_data = {
    "name": "Your SaaS Product",
    "description": "Description of your product",
    "category": "productivity",
    "features": [
        "Feature 1",
        "Feature 2",
        "Feature 3"
    ],
    "pricing_model": "subscription",
    "integration_options": ["REST API", "Webhooks"],
    "knowledge_base": {
        "faq": [
            {
                "question": "How does it work?",
                "answer": "It works by..."
            }
        ],
        "technical_specs": {
            "api_version": "v2",
            "rate_limits": "1000 req/min"
        }
    }
}

response = requests.post(
    f"{BASE_URL}/products/",
    headers=headers,
    json=product_data
)

product_id = response.json()["id"]
print(f"Product created: {product_id}")
```

### Adım 3: Agent ile İletişim

```python
def ask_agent(product_id, user_message, session_id=None):
    """Agent'a soru sor"""
    
    data = {
        "product_id": product_id,
        "message": user_message,
        "session_id": session_id or f"session_{int(time.time())}"
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/chat",
        headers=headers,
        json=data
    )
    
    return response.json()

# Örnek kullanım
result = ask_agent(
    product_id="prod_123",
    user_message="What are the pricing options?"
)

print(f"Agent Response: {result['response']}")
print(f"Confidence: {result['confidence']}")
```

### Adım 4: Ürün Yapılandırması

```python
def configure_product(product_id, user_inputs):
    """Ürünü kullanıcı gereksinimlerine göre yapılandır"""
    
    data = {
        "product_id": product_id,
        "user_inputs": user_inputs,
        "requirements": [
            "Must support 10,000+ users",
            "GDPR compliance required"
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/configure",
        headers=headers,
        json=data
    )
    
    return response.json()

# Örnek kullanım
config = configure_product(
    product_id="prod_123",
    user_inputs={
        "deployment_type": "cloud",
        "scale": "enterprise",
        "features": ["analytics", "reporting"],
        "region": "eu-west-1"
    }
)

print(f"Estimated Price: ${config['estimated_price']}")
print(f"Setup Steps: {config['setup_steps']}")
```

---

## 2. JavaScript SDK Entegrasyonu

### Kurulum

```html
<!-- HTML'e ekle -->
<script src="https://cdn.compagent.com/sdk/v1/compagent.js"></script>
```

veya npm ile:

```bash
npm install @compagent/sdk
```

### Kullanım

```javascript
import Compagent from '@compagent/sdk';

// SDK'yı başlat
const agent = new Compagent({
  apiKey: 'your_api_key_here',
  productId: 'prod_123'
});

// Chat widget'ını göster
agent.showChat({
  position: 'bottom-right',
  theme: 'light',
  language: 'tr'
});

// Programmatik olarak mesaj gönder
agent.sendMessage('Fiyatlandırma hakkında bilgi alabilir miyim?')
  .then(response => {
    console.log('Agent Response:', response.message);
  });

// Event listener'lar
agent.on('message', (data) => {
  console.log('User sent:', data.message);
});

agent.on('response', (data) => {
  console.log('Agent replied:', data.response);
});

agent.on('config-generated', (data) => {
  console.log('Configuration:', data.config);
  // Kullanıcıya yapılandırmayı göster
});
```

### React Entegrasyonu

```jsx
import { CompagentProvider, useCompagent } from '@compagent/react';

function App() {
  return (
    <CompagentProvider
      apiKey="your_api_key"
      productId="prod_123"
    >
      <YourApp />
    </CompagentProvider>
  );
}

function ChatButton() {
  const { openChat, sendMessage } = useCompagent();
  
  return (
    <button onClick={() => openChat()}>
      Chat with Sales Agent
    </button>
  );
}
```

---

## 3. Webhook Entegrasyonu

### Webhook Ayarlama

```python
# Webhook endpoint'i kaydet
webhook_config = {
    "url": "https://your-app.com/webhooks/compagent",
    "events": [
        "conversation.started",
        "conversation.ended",
        "configuration.generated",
        "lead.qualified"
    ],
    "secret": "your_webhook_secret"
}

requests.post(
    f"{BASE_URL}/webhooks",
    headers=headers,
    json=webhook_config
)
```

### Webhook Alma

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhooks/compagent', methods=['POST'])
def handle_webhook():
    # Webhook doğrulama
    signature = request.headers.get('X-Compagent-Signature')
    payload = request.get_data()
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if signature != expected_signature:
        return 'Invalid signature', 401
    
    # Event işle
    event = request.json
    event_type = event['type']
    
    if event_type == 'conversation.ended':
        # Konuşma bitti, lead'i kaydet
        lead_data = event['data']
        save_lead(lead_data)
    
    elif event_type == 'configuration.generated':
        # Yapılandırma oluşturuldu
        config = event['data']['configuration']
        send_to_sales_team(config)
    
    return 'OK', 200
```

---

## 4. Embed Widget

### Basit Embed

```html
<!-- Web sitenize ekleyin -->
<div id="compagent-widget"></div>

<script>
window.CompagentConfig = {
  apiKey: 'your_api_key',
  productId: 'prod_123',
  theme: {
    primaryColor: '#0066cc',
    position: 'bottom-right'
  },
  language: 'tr'
};
</script>
<script src="https://cdn.compagent.com/widget/v1/embed.js" async></script>
```

### Özelleştirilmiş Widget

```html
<script>
window.CompagentConfig = {
  apiKey: 'your_api_key',
  productId: 'prod_123',
  
  // Görünüm
  theme: {
    primaryColor: '#0066cc',
    fontFamily: 'Inter, sans-serif',
    borderRadius: '12px',
    position: 'bottom-right',
    offset: { x: 20, y: 20 }
  },
  
  // Başlangıç mesajı
  greeting: {
    message: 'Merhaba! Size nasıl yardımcı olabilirim?',
    delay: 2000
  },
  
  // Özelleştirmeler
  features: {
    fileUpload: true,
    voiceInput: false,
    emailCapture: true
  },
  
  // Callbacks
  onOpen: () => {
    console.log('Chat opened');
  },
  onClose: () => {
    console.log('Chat closed');
  },
  onLeadCaptured: (lead) => {
    console.log('Lead captured:', lead);
    // Kendi CRM'inize kaydet
  }
};
</script>
```

---

## Güvenlik Best Practices

### 1. API Key Güvenliği

```javascript
// ❌ YANLIŞ: Frontend'de API key açığa çıkar
const agent = new Compagent({
  apiKey: 'sk-xxx-your-secret-key' // YAPMAYIN!
});

// ✅ DOĞRU: Backend'den proxy kullan
const agent = new Compagent({
  endpoint: '/api/agent-proxy' // Kendi backend'iniz
});
```

### 2. Rate Limiting

```python
from functools import wraps
from time import time

def rate_limit(max_per_minute=10):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            calls[:] = [c for c in calls if c > now - 60]
            
            if len(calls) >= max_per_minute:
                raise Exception('Rate limit exceeded')
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_per_minute=20)
def call_agent(message):
    return ask_agent(product_id, message)
```

### 3. Input Validation

```python
from pydantic import BaseModel, validator

class ChatRequest(BaseModel):
    message: str
    session_id: str
    
    @validator('message')
    def validate_message(cls, v):
        if len(v) > 1000:
            raise ValueError('Message too long')
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
```

---

## Örnek Kullanım Senaryoları

### Senaryo 1: E-ticaret Sitesi

```javascript
// Ürün sayfasında agent'ı başlat
const productAgent = new Compagent({
  apiKey: API_KEY,
  productId: getCurrentProductId(),
  context: {
    page: 'product-detail',
    productName: product.name,
    price: product.price
  }
});

// Fiyat sorusuna özel aksiyon
productAgent.on('intent:pricing', (data) => {
  // Checkout'a yönlendir
  showCheckoutModal(data.configuration);
});
```

### Senaryo 2: SaaS Dashboard

```javascript
// Dashboard'da yardım butonu
function showContextualHelp() {
  const agent = new Compagent({
    apiKey: API_KEY,
    productId: 'prod_123',
    context: {
      userRole: currentUser.role,
      currentPage: window.location.pathname,
      recentActions: getUserRecentActions()
    }
  });
  
  agent.open();
}
```

### Senaryo 3: Lead Qualification

```python
# Webhook ile lead'leri otomatik qualify et
@app.route('/webhooks/compagent', methods=['POST'])
def qualify_lead():
    event = request.json
    
    if event['type'] == 'conversation.ended':
        lead = event['data']
        
        # Lead skorlama
        score = calculate_lead_score(lead)
        
        if score > 80:
            # Yüksek kaliteli lead - Sales'e hemen gönder
            notify_sales_team(lead)
        elif score > 50:
            # Orta kaliteli - Nurture campaign'e ekle
            add_to_nurture_campaign(lead)
        else:
            # Düşük kaliteli - Self-service'e yönlendir
            send_documentation(lead)
    
    return 'OK', 200
```

---

## Monitoring ve Analytics

### Dashboard Metrikleri

```python
# Analytics API'den metrikleri çek
def get_dashboard_metrics():
    metrics = requests.get(
        f"{BASE_URL}/analytics/dashboard",
        headers=headers
    ).json()
    
    return {
        'conversations_today': metrics['overview']['total_conversations_today'],
        'satisfaction_rate': metrics['overview']['avg_satisfaction'],
        'conversion_rate': metrics['trends']['conversion_trend'][-1]
    }
```

### Custom Events

```javascript
// Custom event gönder
agent.track('product_demo_requested', {
  productId: 'prod_123',
  userType: 'enterprise',
  source: 'pricing_page'
});
```

---

## Destek

- **Teknik Dokümantasyon**: https://docs.compagent.com
- **API Reference**: https://api.compagent.com/docs
- **GitHub**: https://github.com/yourcompany/compagent
- **Email**: support@compagent.com
- **Discord Community**: https://discord.gg/compagent
