"""
Test script - Groq API bağlantısını test et
"""
import os
from dotenv import load_dotenv
from groq import Groq

# .env dosyasını yükle
load_dotenv()

def test_groq_connection():
    """Groq API bağlantısını test et"""
    
    print("🔍 Groq API bağlantısı test ediliyor...")
    print("-" * 50)
    
    # API key kontrolü
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("❌ HATA: GROQ_API_KEY ayarlanmamış!")
        print("\n📝 Yapılması gerekenler:")
        print("1. .env dosyasını açın")
        print("2. GROQ_API_KEY=gsk_your_actual_key_here şeklinde güncelleyin")
        print("3. Groq API key almak için: https://console.groq.com/")
        return False
    
    print(f"✅ API Key bulundu: {api_key[:10]}...{api_key[-4:]}")
    
    # Model kontrolü
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    print(f"✅ Model: {model}")
    
    # Groq client oluştur
    try:
        client = Groq(api_key=api_key)
        print("✅ Groq client oluşturuldu")
    except Exception as e:
        print(f"❌ Client oluşturma hatası: {e}")
        return False
    
    # Test mesajı gönder
    print("\n📤 Test mesajı gönderiliyor...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Sen yardımcı bir asistansın. Kısa ve net cevaplar ver."
                },
                {
                    "role": "user",
                    "content": "Merhaba! Sadece 'Bağlantı başarılı!' de."
                }
            ],
            temperature=0.5,
            max_tokens=50
        )
        
        answer = response.choices[0].message.content
        print(f"✅ Yanıt alındı: {answer}")
        
        # İstatistikler
        print("\n📊 İstatistikler:")
        print(f"   - Model: {response.model}")
        if hasattr(response, 'usage'):
            print(f"   - Token kullanımı: {response.usage.total_tokens}")
            print(f"   - Prompt tokens: {response.usage.prompt_tokens}")
            print(f"   - Completion tokens: {response.usage.completion_tokens}")
        
        print("\n✅ TEST BAŞARILI! Groq API çalışıyor.")
        return True
        
    except Exception as e:
        print(f"❌ API çağrısı hatası: {e}")
        print("\n🔧 Olası çözümler:")
        print("1. API key'in doğru olduğundan emin olun")
        print("2. İnternet bağlantınızı kontrol edin")
        print("3. Groq servisinin çalıştığını kontrol edin: https://status.groq.com/")
        return False


def test_saas_agent_scenario():
    """SaaS agent senaryosunu test et"""
    
    print("\n" + "=" * 50)
    print("🤖 SaaS Agent Senaryosu Testi")
    print("=" * 50)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("⚠️  API key ayarlanmamış, senaryo testi atlanıyor.")
        return False
    
    client = Groq(api_key=api_key)
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # Senaryo: Müşteri ürün hakkında soru soruyor
    print("\n👤 Müşteri: 'Ürününüzün fiyatlandırma modelleri nelerdir?'")
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """Sen bir SaaS ürün satış uzmanısın. 
                    
Ürün: Analytics Pro - Gelişmiş veri analizi platformu
Fiyatlandırma:
- Basic: $99/ay (100 kullanıcı, temel özellikler)
- Pro: $299/ay (500 kullanıcı, gelişmiş özellikler, API)
- Enterprise: $999/ay (sınırsız kullanıcı, tüm özellikler, özel destek)

Müşteriye profesyonel ve yardımcı bir şekilde bilgi ver."""
                },
                {
                    "role": "user",
                    "content": "Ürününüzün fiyatlandırma modelleri nelerdir?"
                }
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        agent_response = response.choices[0].message.content
        print(f"\n🤖 Agent: {agent_response}")
        
        print("\n✅ SENARYO TESTİ BAŞARILI!")
        return True
        
    except Exception as e:
        print(f"❌ Senaryo testi hatası: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🚀 COMPAGENT - GROQ API TEST")
    print("=" * 50 + "\n")
    
    # Test 1: Bağlantı testi
    connection_ok = test_groq_connection()
    
    # Test 2: Senaryo testi (sadece bağlantı başarılıysa)
    if connection_ok:
        test_saas_agent_scenario()
    
    print("\n" + "=" * 50)
    print("Test tamamlandı!")
    print("=" * 50 + "\n")
