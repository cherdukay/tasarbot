from typing import Dict
import anthropic
import os
from models import AnalysisType, Project

class ProjectAnalyzer:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def generate_prompt(self, project: Project, analysis_type: AnalysisType) -> str:
        base_prompt = f"""
        Proje Adı: {project.name}
        Proje Açıklaması: {project.description}
        
        Lütfen bu projeyi analiz edin ve aşağıdaki yön için ayrıntılı bilgiler sağlayın: {analysis_type.value}
        
        Yanıtınızı net bölümler halinde madde işaretleriyle biçimlendirin.
        Belirli öneriler ve uygulanabilir maddeler ekleyin.
        """
        
        analysis_prompts = {
            AnalysisType.RISK: "Teknik riskler, yönetim riskleri ve risk azaltma stratejilerine odaklanın.",
            AnalysisType.RESOURCE: "Gerekli kaynakları, optimizasyon önerilerini ve maliyet tahminlerini analiz edin.",
            AnalysisType.SWOT: "Uygulanabilir içgörülerle ayrıntılı bir SWOT analizi sağlayın.",
            AnalysisType.TIMELINE: "Ana aşamalar ve tahmini sürelerle bir proje zaman çizelgesi oluşturun.",
            AnalysisType.ROADMAP: "Plan A (İdeal), Plan B (Orta) ve Plan C (Minimal) senaryolarını geliştirin."
        }
        
        return base_prompt + "\n" + analysis_prompts.get(analysis_type, "")

    def analyze(self, project: Project, analysis_type: AnalysisType) -> str:
        prompt = self.generate_prompt(project, analysis_type)
        
        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.6,
            system="Proje yönetimi konusunda uzman bir asistansınız ve ayrıntılı proje analizi konusunda uzmansınız. Yanıtlarınızda her zaman Türkçe dilini kullanın.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return message.content[0].text

    def perform_all_analyses(self, project: Project) -> Dict:
        results = {}
        for analysis_type in AnalysisType:
            results[analysis_type.value] = self.analyze(project, analysis_type)
        return results