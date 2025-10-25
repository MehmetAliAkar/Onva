"""
Config Handler - Ürün yapılandırma yöneticisi
"""
from typing import Dict, Any, Optional, List
from groq import Groq
from core.config import settings
from core.logging import logger


class ConfigHandler:
    """
    Ürün yapılandırmasını yönetir
    - Kullanıcı gereksinimlerini analiz eder
    - Optimal yapılandırma önerir
    - Kurulum adımları oluşturur
    """
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        logger.info("ConfigHandler initialized with Groq")
    
    async def generate_configuration(
        self,
        product_id: str,
        user_inputs: Dict[str, Any],
        requirements: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Kullanıcı girdilerine göre yapılandırma oluştur
        
        Args:
            product_id: Ürün ID'si
            user_inputs: Kullanıcı girdi verileri
            requirements: Ek gereksinimler
            
        Returns:
            Yapılandırma detayları
        """
        try:
            # Build configuration based on inputs
            config = {
                "settings": self._build_settings(user_inputs),
                "setup_steps": self._generate_setup_steps(user_inputs),
                "pricing": self._calculate_pricing(user_inputs),
                "integrations": self._determine_integrations(user_inputs)
            }
            
            # Enhance with AI if requirements provided
            if requirements:
                ai_enhancements = await self._get_ai_recommendations(
                    product_id,
                    user_inputs,
                    requirements
                )
                config["ai_recommendations"] = ai_enhancements
            
            logger.info(f"Generated configuration for product: {product_id}")
            return config
            
        except Exception as e:
            logger.error(f"Error generating configuration: {str(e)}")
            raise
    
    async def analyze_requirements(
        self,
        product_id: str,
        requirements: List[str]
    ) -> Dict[str, Any]:
        """
        Müşteri gereksinimlerini analiz et
        
        Args:
            product_id: Ürün ID'si
            requirements: Gereksinim listesi
            
        Returns:
            Analiz ve öneriler
        """
        try:
            # Prepare prompt for AI analysis
            prompt = self._build_requirements_prompt(requirements)
            
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Sen bir SaaS ürün yapılandırma uzmanısın. Müşteri gereksinimlerini analiz ederek en uygun yapılandırmayı öneriyorsun."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "analysis": analysis,
                "recommendation": self._parse_recommendations(analysis),
                "score": self._calculate_compatibility_score(requirements)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing requirements: {str(e)}")
            raise
    
    def _build_settings(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Ayarları oluştur"""
        settings = {
            "deployment": {
                "type": user_inputs.get("deployment_type", "cloud"),
                "region": user_inputs.get("region", "eu-west-1"),
                "scale": user_inputs.get("scale", "standard")
            },
            "features": {
                "enabled": user_inputs.get("features", []),
                "customizations": user_inputs.get("customizations", {})
            },
            "security": {
                "authentication": user_inputs.get("auth_method", "oauth2"),
                "encryption": user_inputs.get("encryption", True)
            },
            "integrations": {
                "apis": user_inputs.get("api_integrations", []),
                "webhooks": user_inputs.get("webhooks", [])
            }
        }
        return settings
    
    def _generate_setup_steps(self, user_inputs: Dict[str, Any]) -> List[str]:
        """Kurulum adımlarını oluştur"""
        steps = [
            "1. Hesap oluşturma ve API anahtarı alma",
            "2. Gerekli bağımlılıkları yükleme",
            "3. Yapılandırma dosyasını düzenleme",
        ]
        
        # Add deployment-specific steps
        deployment = user_inputs.get("deployment_type", "cloud")
        if deployment == "on-premise":
            steps.append("4. Sunucu kurulumu ve yapılandırması")
            steps.append("5. Veritabanı bağlantısını ayarlama")
        else:
            steps.append("4. Cloud hesabını bağlama")
        
        # Add integration steps
        if user_inputs.get("api_integrations"):
            steps.append(f"{len(steps) + 1}. API entegrasyonlarını yapılandırma")
        
        steps.append(f"{len(steps) + 1}. Test ve doğrulama")
        steps.append(f"{len(steps) + 1}. Production'a geçiş")
        
        return steps
    
    def _calculate_pricing(self, user_inputs: Dict[str, Any]) -> float:
        """Tahmini fiyatlandırma hesapla"""
        base_price = 99.0  # Base monthly price
        
        # Scale multiplier
        scale = user_inputs.get("scale", "standard")
        scale_multiplier = {
            "small": 0.5,
            "standard": 1.0,
            "large": 2.0,
            "enterprise": 5.0
        }.get(scale, 1.0)
        
        # Feature count multiplier
        features = user_inputs.get("features", [])
        feature_cost = len(features) * 10.0
        
        # Integration multiplier
        integrations = user_inputs.get("api_integrations", [])
        integration_cost = len(integrations) * 20.0
        
        total = (base_price * scale_multiplier) + feature_cost + integration_cost
        
        return round(total, 2)
    
    def _determine_integrations(self, user_inputs: Dict[str, Any]) -> List[Dict[str, str]]:
        """Gerekli entegrasyonları belirle"""
        integrations = []
        
        api_integrations = user_inputs.get("api_integrations", [])
        for api in api_integrations:
            integrations.append({
                "name": api,
                "type": "api",
                "status": "pending"
            })
        
        webhooks = user_inputs.get("webhooks", [])
        for webhook in webhooks:
            integrations.append({
                "name": webhook,
                "type": "webhook",
                "status": "pending"
            })
        
        return integrations
    
    async def _get_ai_recommendations(
        self,
        product_id: str,
        user_inputs: Dict[str, Any],
        requirements: List[str]
    ) -> str:
        """AI destekli öneriler al"""
        try:
            prompt = f"""
Müşteri Girdileri: {user_inputs}
Gereksinimler: {', '.join(requirements)}

Bu bilgilere göre en uygun yapılandırma önerilerini liste halinde ver.
Her öneri için kısa açıklama ekle.
"""
            
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "SaaS yapılandırma uzmanısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=400
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting AI recommendations: {str(e)}")
            return "AI önerileri şu anda kullanılamıyor."
    
    def _build_requirements_prompt(self, requirements: List[str]) -> str:
        """Gereksinim analizi için prompt oluştur"""
        return f"""
Aşağıdaki müşteri gereksinimlerini analiz et:

{chr(10).join(f'- {req}' for req in requirements)}

Lütfen:
1. Her gereksinimi değerlendir
2. Uyumlu ürün özelliklerini belirle
3. Önerilen yapılandırmayı detaylandır
4. Potansiyel zorlukları ve çözümleri açıkla
"""
    
    def _parse_recommendations(self, analysis: str) -> Dict[str, Any]:
        """AI analizinden önerileri çıkar"""
        # Simple parsing - in production, use structured output
        return {
            "summary": analysis[:200] + "..." if len(analysis) > 200 else analysis,
            "full_analysis": analysis
        }
    
    def _calculate_compatibility_score(self, requirements: List[str]) -> float:
        """Uyumluluk skorunu hesapla"""
        # Simple scoring based on requirement count
        # In production, implement more sophisticated scoring
        base_score = 0.80
        requirement_bonus = min(len(requirements) * 0.02, 0.15)
        return min(base_score + requirement_bonus, 0.98)
