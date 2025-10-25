# Kullanım Örnekleri

Bu dokümanda Compagent platformunun çeşitli kullanım senaryolarını bulabilirsiniz.

## İçindekiler

1. [Basit Chat Örneği](#1-basit-chat-örneği)
2. [Ürün Yapılandırma](#2-ürün-yapılandırma)
3. [Multi-Language Destek](#3-multi-language-destek)
4. [Lead Qualification](#4-lead-qualification)
5. [A/B Testing](#5-ab-testing)
6. [Custom Context](#6-custom-context)

---

## 1. Basit Chat Örneği

### Python

```python
import requests
import json

API_KEY = "your_api_key"
BASE_URL = "https://api.compagent.com/api/v1"

def chat_with_agent(product_id, message, session_id=None):
    """Agent ile basit sohbet"""
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "product_id": product_id,
        "message": message,
        "session_id": session_id or "demo_session"
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/chat",
        headers=headers,
        json=data
    )
    
    result = response.json()
    return result

# Kullanım
if __name__ == "__main__":
    # Ürün hakkında genel soru
    response1 = chat_with_agent(
        product_id="prod_123",
        message="Bu ürün nedir ve ne işe yarar?"
    )
    print(f"Agent: {response1['response']}\n")
    
    # Fiyatlandırma sorusu
    response2 = chat_with_agent(
        product_id="prod_123",
        message="Fiyatlandırma paketleriniz nelerdir?",
        session_id="demo_session"  # Aynı session
    )
    print(f"Agent: {response2['response']}\n")
    print(f"Öneriler: {response2['suggestions']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_KEY = 'your_api_key';
const BASE_URL = 'https://api.compagent.com/api/v1';

async function chatWithAgent(productId, message, sessionId = null) {
  try {
    const response = await axios.post(
      `${BASE_URL}/agent/chat`,
      {
        product_id: productId,
        message: message,
        session_id: sessionId || `session_${Date.now()}`
      },
      {
        headers: {
          'X-API-Key': API_KEY,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    throw error;
  }
}

// Kullanım
(async () => {
  const result = await chatWithAgent(
    'prod_123',
    'Tell me about your enterprise plan'
  );
  
  console.log('Agent:', result.response);
  console.log('Confidence:', result.confidence);
  console.log('Suggestions:', result.suggestions);
})();
```

---

## 2. Ürün Yapılandırma

### Python - Otomatik Yapılandırma

```python
def configure_for_customer(customer_profile):
    """Müşteri profiline göre otomatik yapılandırma"""
    
    # Müşteri ihtiyaçlarını analiz et
    user_inputs = {
        "deployment_type": "cloud" if customer_profile["prefers_cloud"] else "on-premise",
        "scale": determine_scale(customer_profile["company_size"]),
        "features": select_features(customer_profile["industry"]),
        "region": customer_profile["region"],
        "api_integrations": customer_profile["existing_tools"]
    }
    
    # Yapılandırma oluştur
    response = requests.post(
        f"{BASE_URL}/agent/configure",
        headers=headers,
        json={
            "product_id": "prod_123",
            "user_inputs": user_inputs,
            "requirements": [
                f"Must support {customer_profile['user_count']} users",
                f"{customer_profile['compliance']} compliance required",
                f"Budget: ${customer_profile['budget']}/month"
            ]
        }
    )
    
    config = response.json()
    return config

def determine_scale(company_size):
    """Şirket büyüklüğüne göre scale belirle"""
    if company_size < 50:
        return "small"
    elif company_size < 500:
        return "standard"
    elif company_size < 5000:
        return "large"
    else:
        return "enterprise"

def select_features(industry):
    """Sektöre göre özellikler seç"""
    industry_features = {
        "fintech": ["analytics", "reporting", "security", "compliance"],
        "ecommerce": ["analytics", "api", "webhooks", "integrations"],
        "healthcare": ["security", "compliance", "encryption", "audit_logs"],
        "education": ["user_management", "reporting", "analytics"]
    }
    return industry_features.get(industry, ["basic_features"])

# Örnek kullanım
customer = {
    "company_name": "Acme Corp",
    "company_size": 250,
    "user_count": 500,
    "industry": "fintech",
    "region": "eu-west-1",
    "budget": 2000,
    "prefers_cloud": True,
    "compliance": "GDPR",
    "existing_tools": ["Salesforce", "Slack", "Stripe"]
}

config = configure_for_customer(customer)

print(f"Önerilen Yapılandırma:")
print(f"- Tahmini Fiyat: ${config['estimated_price']}/ay")
print(f"- Kurulum Adımları: {len(config['setup_steps'])} adım")
print(f"\nAdımlar:")
for step in config['setup_steps']:
    print(f"  {step}")
```

---

## 3. Multi-Language Destek

### Python - Çoklu Dil Desteği

```python
def chat_multilingual(product_id, message, language='tr'):
    """Çoklu dil destekli chat"""
    
    # Dil-spesifik context ekle
    context = {
        "language": language,
        "locale": get_locale(language)
    }
    
    data = {
        "product_id": product_id,
        "message": message,
        "context": context
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/chat",
        headers=headers,
        json=data
    )
    
    return response.json()

def get_locale(language):
    """Dil koduna göre locale döndür"""
    locales = {
        'tr': 'tr_TR',
        'en': 'en_US',
        'de': 'de_DE',
        'fr': 'fr_FR',
        'es': 'es_ES'
    }
    return locales.get(language, 'en_US')

# Farklı dillerde örnekler
languages = {
    'tr': 'Fiyatlandırma hakkında bilgi alabilir miyim?',
    'en': 'Can I get information about pricing?',
    'de': 'Kann ich Informationen über die Preisgestaltung erhalten?',
    'fr': 'Puis-je obtenir des informations sur les prix?',
    'es': '¿Puedo obtener información sobre precios?'
}

for lang, question in languages.items():
    print(f"\n{lang.upper()}:")
    response = chat_multilingual('prod_123', question, lang)
    print(f"Q: {question}")
    print(f"A: {response['response']}")
```

---

## 4. Lead Qualification

### Python - Otomatik Lead Skorlama

```python
from datetime import datetime

class LeadQualificationSystem:
    """Lead'leri otomatik qualify eden sistem"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.session_data = {}
    
    def track_conversation(self, session_id, message, response):
        """Konuşmayı kaydet ve analiz et"""
        
        if session_id not in self.session_data:
            self.session_data[session_id] = {
                'started_at': datetime.now(),
                'messages': [],
                'signals': [],
                'score': 0
            }
        
        session = self.session_data[session_id]
        session['messages'].append({
            'message': message,
            'response': response,
            'timestamp': datetime.now()
        })
        
        # Lead sinyallerini tespit et
        self.detect_signals(session_id, message, response)
        
        # Skoru güncelle
        session['score'] = self.calculate_score(session_id)
        
        return session['score']
    
    def detect_signals(self, session_id, message, response):
        """Önemli lead sinyallerini tespit et"""
        
        session = self.session_data[session_id]
        
        # Buying intent sinyalleri
        buying_keywords = [
            'fiyat', 'price', 'satın al', 'buy', 'demo',
            'başla', 'start', 'deneme', 'trial', 'paket', 'plan'
        ]
        
        # Budget sinyalleri
        budget_keywords = [
            'bütçe', 'budget', 'cost', 'maliyet',
            'ödeme', 'payment', 'aylık', 'monthly'
        ]
        
        # Decision maker sinyalleri
        decision_keywords = [
            'ekibim', 'team', 'şirket', 'company',
            'karar', 'decision', 'ceo', 'manager'
        ]
        
        # Timeline sinyalleri
        timeline_keywords = [
            'ne zaman', 'when', 'acil', 'urgent',
            'hızlı', 'quick', 'yakında', 'soon'
        ]
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in buying_keywords):
            session['signals'].append('buying_intent')
        
        if any(keyword in message_lower for keyword in budget_keywords):
            session['signals'].append('budget_discussion')
        
        if any(keyword in message_lower for keyword in decision_keywords):
            session['signals'].append('decision_maker')
        
        if any(keyword in message_lower for keyword in timeline_keywords):
            session['signals'].append('timeline_mentioned')
    
    def calculate_score(self, session_id):
        """Lead skorunu hesapla (0-100)"""
        
        session = self.session_data[session_id]
        score = 30  # Base score
        
        # Sinyal bazlı skorlama
        signal_scores = {
            'buying_intent': 25,
            'budget_discussion': 20,
            'decision_maker': 15,
            'timeline_mentioned': 10
        }
        
        for signal in set(session['signals']):
            score += signal_scores.get(signal, 0)
        
        # Engagement bazlı skorlama
        message_count = len(session['messages'])
        if message_count > 5:
            score += 10
        if message_count > 10:
            score += 10
        
        # Süre bazlı skorlama
        duration = (datetime.now() - session['started_at']).seconds / 60
        if duration > 5:  # 5 dakikadan fazla engagement
            score += 5
        
        return min(score, 100)  # Max 100
    
    def get_qualification(self, session_id):
        """Lead qualification seviyesini döndür"""
        
        score = self.session_data[session_id]['score']
        
        if score >= 80:
            return {
                'level': 'HOT',
                'action': 'Immediate sales follow-up',
                'priority': 'high'
            }
        elif score >= 60:
            return {
                'level': 'WARM',
                'action': 'Schedule demo within 24h',
                'priority': 'medium'
            }
        elif score >= 40:
            return {
                'level': 'COLD',
                'action': 'Add to nurture campaign',
                'priority': 'low'
            }
        else:
            return {
                'level': 'UNQUALIFIED',
                'action': 'Self-service resources',
                'priority': 'none'
            }

# Kullanım
lead_system = LeadQualificationSystem(API_KEY)

session_id = "lead_session_123"

# Konuşma simülasyonu
conversations = [
    "Ürününüz hakkında bilgi alabilir miyim?",
    "Fiyatlandırma paketleriniz nelerdir?",
    "500 kişilik ekibimiz için uygun mu?",
    "Bütçemiz aylık 2000-3000 dolar arası",
    "Demo yapabilir miyiz? CEO'muz da katılmak istiyor",
    "Bu ay içinde başlamak istiyoruz"
]

for message in conversations:
    # Agent'a gönder
    response = chat_with_agent('prod_123', message, session_id)
    
    # Lead skorunu güncelle
    score = lead_system.track_conversation(
        session_id,
        message,
        response['response']
    )
    
    print(f"\nUser: {message}")
    print(f"Agent: {response['response']}")
    print(f"Lead Score: {score}/100")

# Final qualification
qualification = lead_system.get_qualification(session_id)
print(f"\n=== LEAD QUALIFICATION ===")
print(f"Level: {qualification['level']}")
print(f"Action: {qualification['action']}")
print(f"Priority: {qualification['priority']}")
```

---

## 5. A/B Testing

### Python - Agent Varyasyonları Test Etme

```python
import random
from collections import defaultdict

class ABTestManager:
    """Agent varyasyonlarını A/B test eden sistem"""
    
    def __init__(self):
        self.variants = {
            'A': {'greeting': 'formal', 'tone': 'professional'},
            'B': {'greeting': 'casual', 'tone': 'friendly'}
        }
        self.results = defaultdict(lambda: {
            'conversations': 0,
            'qualified_leads': 0,
            'avg_satisfaction': 0,
            'conversion_rate': 0
        })
    
    def assign_variant(self, session_id):
        """Kullanıcıya varyant ata"""
        return random.choice(['A', 'B'])
    
    def chat_with_variant(self, product_id, message, variant, session_id):
        """Belirli varyant ile chat"""
        
        # Varyant-spesifik context
        context = {
            'variant': variant,
            'greeting_style': self.variants[variant]['greeting'],
            'tone': self.variants[variant]['tone']
        }
        
        response = chat_with_agent(
            product_id,
            message,
            session_id,
            context=context
        )
        
        return response
    
    def track_result(self, variant, metrics):
        """Sonuçları kaydet"""
        result = self.results[variant]
        result['conversations'] += 1
        result['qualified_leads'] += metrics['qualified']
        result['avg_satisfaction'] += metrics['satisfaction']
        result['conversion_rate'] = (
            result['qualified_leads'] / result['conversations']
        )
    
    def get_winner(self):
        """Kazanan varyantı belirle"""
        if all(v['conversations'] < 100 for v in self.results.values()):
            return None  # Yeterli data yok
        
        # En yüksek conversion rate'e sahip varyant
        winner = max(
            self.results.items(),
            key=lambda x: x[1]['conversion_rate']
        )
        
        return winner[0]

# Kullanım
ab_test = ABTestManager()

# 200 konuşma simüle et
for i in range(200):
    session_id = f"test_session_{i}"
    variant = ab_test.assign_variant(session_id)
    
    # Chat
    response = ab_test.chat_with_variant(
        'prod_123',
        'Tell me about your product',
        variant,
        session_id
    )
    
    # Simüle edilmiş metrikler
    metrics = {
        'qualified': random.random() > 0.7,
        'satisfaction': random.uniform(0.6, 1.0)
    }
    
    ab_test.track_result(variant, metrics)

# Sonuçlar
print("\n=== A/B TEST RESULTS ===")
for variant, data in ab_test.results.items():
    print(f"\nVariant {variant}:")
    print(f"  Conversations: {data['conversations']}")
    print(f"  Qualified Leads: {data['qualified_leads']}")
    print(f"  Conversion Rate: {data['conversion_rate']:.2%}")
    print(f"  Avg Satisfaction: {data['avg_satisfaction']/data['conversations']:.2f}")

winner = ab_test.get_winner()
if winner:
    print(f"\n🏆 Winner: Variant {winner}")
```

---

## 6. Custom Context

### Python - Dinamik Context Yönetimi

```python
class ContextManager:
    """Kullanıcı context'ini yöneten sistem"""
    
    def __init__(self):
        self.user_contexts = {}
    
    def build_context(self, user_id, user_data):
        """Kullanıcı için zengin context oluştur"""
        
        context = {
            # Kullanıcı bilgileri
            "user": {
                "id": user_id,
                "name": user_data.get('name'),
                "email": user_data.get('email'),
                "company": user_data.get('company'),
                "role": user_data.get('role')
            },
            
            # Davranış verileri
            "behavior": {
                "visits": user_data.get('visit_count', 0),
                "pages_viewed": user_data.get('pages_viewed', []),
                "time_spent": user_data.get('time_spent_seconds', 0),
                "last_action": user_data.get('last_action')
            },
            
            # Teknik bilgiler
            "technical": {
                "current_plan": user_data.get('current_plan'),
                "integrations": user_data.get('active_integrations', []),
                "api_usage": user_data.get('api_calls_last_month', 0)
            },
            
            # İş bilgileri
            "business": {
                "industry": user_data.get('industry'),
                "company_size": user_data.get('company_size'),
                "use_case": user_data.get('use_case'),
                "pain_points": user_data.get('pain_points', [])
            }
        }
        
        self.user_contexts[user_id] = context
        return context
    
    def chat_with_context(self, product_id, user_id, message):
        """Context-aware chat"""
        
        if user_id not in self.user_contexts:
            raise ValueError(f"Context not found for user: {user_id}")
        
        context = self.user_contexts[user_id]
        
        response = requests.post(
            f"{BASE_URL}/agent/chat",
            headers=headers,
            json={
                "product_id": product_id,
                "message": message,
                "context": context,
                "session_id": f"user_{user_id}"
            }
        )
        
        return response.json()

# Kullanım
context_mgr = ContextManager()

# Zengin kullanıcı verisi
user_data = {
    'name': 'John Doe',
    'email': 'john@acme.com',
    'company': 'Acme Corp',
    'role': 'CTO',
    'visit_count': 15,
    'pages_viewed': ['/pricing', '/features', '/integrations', '/docs'],
    'time_spent_seconds': 1800,
    'last_action': 'viewed_pricing_page',
    'current_plan': 'trial',
    'active_integrations': ['Salesforce', 'Slack'],
    'api_calls_last_month': 5000,
    'industry': 'fintech',
    'company_size': 250,
    'use_case': 'customer_analytics',
    'pain_points': ['data_silos', 'manual_reporting', 'scalability']
}

# Context oluştur
context = context_mgr.build_context('user_123', user_data)

# Context-aware sohbet
response = context_mgr.chat_with_context(
    'prod_123',
    'user_123',
    'Ölçeklenebilirlik konusunda endişelerim var'
)

print(f"Agent (context-aware): {response['response']}")
# Agent, kullanıcının pain point'lerini ve kullanım verilerini
# bilerek daha kişiselleştirilmiş cevap verecektir
```

---

## Daha Fazla Örnek

Daha fazla örnek ve kullanım senaryosu için:

- [GitHub Repository](https://github.com/yourcompany/compagent)
- [Example Projects](https://github.com/yourcompany/compagent-examples)
- [Community Recipes](https://community.compagent.com/recipes)

## Destek

Sorularınız için:
- Email: support@compagent.com
- Discord: https://discord.gg/compagent
- Docs: https://docs.compagent.com
