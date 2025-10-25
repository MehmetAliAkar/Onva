"""
QA Processor - Soru-cevap işleme motoru
"""
from typing import Dict, Any, Optional, List
from groq import Groq
from core.config import settings
from core.logging import logger


class QAProcessor:
    """
    Kullanıcı sorularını işler ve cevaplayıcı
    - Groq/LLM ile entegrasyon
    - Context-aware yanıtlar
    - Güven skoru hesaplama
    """
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.conversation_history: Dict[str, List[Dict]] = {}
        logger.info("QAProcessor initialized with Groq")
    
    def process_query(
        self,
        query: str,
        context: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Process a query with optional context and system prompt
        
        Args:
            query: User's question
            context: Relevant context from documents
            system_prompt: Custom system prompt for the agent
            
        Returns:
            Generated response
        """
        try:
            # Build messages
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add context to user message if available
            user_message = query
            if context:
                user_message = f"Context:\n{context}\n\nQuestion: {query}"
            
            messages.append({"role": "user", "content": user_message})
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."
    
    async def process_question(
        self,
        question: str,
        product_knowledge: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Soruyu işle ve cevap üret
        
        Args:
            question: Kullanıcı sorusu
            product_knowledge: Ürün bilgi tabanı
            context: Ek bağlam bilgisi
            session_id: Oturum ID'si
            
        Returns:
            Cevap ve metadata
        """
        try:
            # Prepare context for LLM
            system_prompt = self._build_system_prompt(product_knowledge)
            user_context = self._prepare_context(question, context, session_id)
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_context}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            # Calculate confidence score
            confidence = self._calculate_confidence(response)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(question, product_knowledge)
            
            # Store conversation history
            if session_id:
                self._update_history(session_id, question, answer)
            
            return {
                "answer": answer,
                "confidence": confidence,
                "suggestions": suggestions,
                "config_suggestion": self._extract_config_hints(answer, product_knowledge)
            }
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {
                "answer": "Üzgünüm, şu anda bu soruyu cevaplayamıyorum. Lütfen daha sonra tekrar deneyin.",
                "confidence": 0.0,
                "suggestions": [],
                "config_suggestion": None
            }
    
    def _build_system_prompt(self, product_knowledge: Dict[str, Any]) -> str:
        """System prompt oluştur"""
        product_name = product_knowledge.get("name", "Ürün")
        description = product_knowledge.get("description", "")
        features = product_knowledge.get("features", [])
        
        prompt = f"""Sen bir SaaS ürün satış ve destek uzmanısın. 
        
Ürün Bilgileri:
- İsim: {product_name}
- Açıklama: {description}
- Özellikler: {', '.join(features) if features else 'Belirtilmemiş'}

Görevin:
1. Müşteri sorularını profesyonel ve yardımcı bir şekilde cevaplamak
2. Ürün özelliklerini net bir şekilde açıklamak
3. Teknik soruları detaylı yanıtlamak
4. Gerektiğinde ürün yapılandırma önerileri sunmak
5. Satış sürecini desteklemek

Kurallar:
- Her zaman kibar ve profesyonel ol
- Bilmediğin şeyleri uydurmak yerine "Bu konuda detaylı bilgi almak için destek ekibimizle iletişime geçebilirsiniz" de
- Müşteri ihtiyaçlarını anlamaya çalış
- Somut örnekler ver
"""
        return prompt
    
    def _prepare_context(
        self,
        question: str,
        context: Optional[Dict[str, Any]],
        session_id: Optional[str]
    ) -> str:
        """Kullanıcı context'i hazırla"""
        context_parts = [f"Soru: {question}"]
        
        if context:
            context_parts.append(f"\nEk Bilgiler: {context}")
        
        if session_id and session_id in self.conversation_history:
            history = self.conversation_history[session_id][-3:]  # Son 3 mesaj
            if history:
                context_parts.append("\nÖnceki Konuşma:")
                for h in history:
                    context_parts.append(f"K: {h['question']}")
                    context_parts.append(f"C: {h['answer']}")
        
        return "\n".join(context_parts)
    
    def _calculate_confidence(self, response: Any) -> float:
        """Cevap güven skorunu hesapla"""
        # Simple confidence calculation based on response
        # In production, implement more sophisticated scoring
        try:
            # Check if response has finish_reason
            if hasattr(response.choices[0], 'finish_reason'):
                if response.choices[0].finish_reason == 'stop':
                    return 0.85
            return 0.70
        except:
            return 0.50
    
    def _generate_suggestions(
        self,
        question: str,
        product_knowledge: Dict[str, Any]
    ) -> List[str]:
        """İlgili soru önerileri oluştur"""
        # Generate related questions based on the topic
        suggestions = [
            "Fiyatlandırma modelleri nelerdir?",
            "Entegrasyon seçenekleri hakkında bilgi alabilir miyim?",
            "Kurulum süreci nasıl işliyor?",
            "Teknik destek nasıl sağlanıyor?"
        ]
        return suggestions[:3]
    
    def _extract_config_hints(
        self,
        answer: str,
        product_knowledge: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Cevaptan yapılandırma ipuçları çıkar"""
        # TODO: Implement intelligent config extraction
        # For now, return None
        return None
    
    def _update_history(
        self,
        session_id: str,
        question: str,
        answer: str
    ):
        """Konuşma geçmişini güncelle"""
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        self.conversation_history[session_id].append({
            "question": question,
            "answer": answer
        })
        
        # Keep only last 10 exchanges
        if len(self.conversation_history[session_id]) > 10:
            self.conversation_history[session_id] = \
                self.conversation_history[session_id][-10:]
