import os
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import print as rprint
from database import DatabaseManager
from models import Project, AnalysisType
from analyzer import ProjectAnalyzer
from dotenv import load_dotenv
load_dotenv()

class TasarBot:
    def __init__(self):
        self.console = Console()
        self.analyzer = ProjectAnalyzer()
        self.current_project = None
        self.db = DatabaseManager()

    def display_menu(self):
        self.console.clear()
        rprint(Panel.fit("🤖 [bold blue]TasarBot[/bold blue] - Proje Analiz Asistanı"))
        menu_items = [
            "[1] Yeni Proje Oluştur",
            "[2] Proje Yükle",
            "[3] Analiz Yap",
            "[4] Mevcut Projeyi Görüntüle",
            "[5] Projeyi Kaydet",
            "[6] Çıkış"
        ]
        for item in menu_items:
            rprint(item)

    def create_project(self):
        self.console.clear()
        rprint(Panel.fit("[bold green]Yeni Proje Oluştur[/bold green]"))
        
        name = Prompt.ask("Proje Adı")
        description = Prompt.ask("Proje Açıklaması")
        
        self.current_project = Project(name=name, description=description, created_at="")
        rprint("[green]✓ Proje başarıyla oluşturuldu![/green]")

    def perform_analysis(self):
        if not self.current_project:
            rprint("[red]Yüklü proje yok. Lütfen önce bir proje oluşturun veya yükleyin.[/red]")
            return

        analysis_options = {
            "1": AnalysisType.RISK,
            "2": AnalysisType.RESOURCE,
            "3": AnalysisType.SWOT,
            "4": AnalysisType.TIMELINE,
            "5": AnalysisType.ROADMAP
        }

        self.console.clear()
        rprint(Panel.fit("[bold yellow]Analiz Türünü Seçin[/bold yellow]"))
        for key, value in analysis_options.items():
            rprint(f"[{key}] {value.value.title()} Analizi")

        choice = Prompt.ask("Analiz türünü seçin", choices=list(analysis_options.keys()))
        
        with self.console.status("[bold green]Analiz oluşturuluyor..."):
            analysis = self.analyzer.analyze(self.current_project, analysis_options[choice])
            self.current_project.analyses[analysis_options[choice].value] = analysis

        self.console.clear()
        rprint(Panel(analysis, title=f"{analysis_options[choice].value.title()} Analizi"))
        input("\nDevam etmek için Enter'a basın...")

    def view_project(self):
        if not self.current_project:
            rprint("[red]Yüklü proje yok.[/red]")
            return

        self.console.clear()
        rprint(Panel.fit(f"""
        [bold blue]Proje Detayları[/bold blue]
        Adı: {self.current_project.name}
        Açıklama: {self.current_project.description}
        Oluşturulma Tarihi: {self.current_project.created_at}
        
        [bold green]Mevcut Analizler:[/bold green]
        {', '.join(self.current_project.analyses.keys()) if self.current_project.analyses else 'Yok'}
        """))
        input("\nDevam etmek için Enter'a basın...")

    def save_project(self):
        if not self.current_project:
            rprint("[red]Kaydedilecek proje yok.[/red]")
            return

        project_id = self.db.save_project(self.current_project)
        rprint(f"[green]✓ Proje ID ile kaydedildi: {project_id}[/green]")

    def load_project(self):
        projects = self.db.list_projects()
        if not projects:
            rprint("[red]Kayıtlı proje bulunamadı.[/red]")
            return

        rprint(Panel.fit("[bold yellow]Mevcut Projeler[/bold yellow]"))
        for pid, name in projects:
            rprint(f"[{pid}] {name}")

        project_id = Prompt.ask("Yüklenecek proje ID'sini girin", 
                            choices=[str(p[0]) for p in projects])
        
        data = self.db.load_project(project_id=int(project_id))
        if data:
            self.current_project = Project.from_dict(data)
            rprint("[green]✓ Proje başarıyla yüklendi![/green]")
        else:
            rprint("[red]Hata: Proje bulunamadı.[/red]")

    def run(self):
        while True:
            self.display_menu()
            choice = Prompt.ask("Bir seçenek seçin", choices=["1", "2", "3", "4", "5", "6"])
            
            actions = {
                "1": self.create_project,
                "2": self.load_project,
                "3": self.perform_analysis,
                "4": self.view_project,
                "5": self.save_project,
                "6": sys.exit
            }
            
            if choice == "6":
                if Confirm.ask("Çıkmak istediğinizden emin misiniz?"):
                    rprint("[yellow]Hoşçakalın! 👋[/yellow]")
                    break
            else:
                actions[choice]()

if __name__ == "__main__":
    bot = TasarBot()
    bot.run()