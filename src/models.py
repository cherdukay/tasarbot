from dataclasses import dataclass
from typing import Dict
from enum import Enum
from datetime import datetime

class AnalysisType(Enum):
    RISK = "risk"
    RESOURCE = "resource"
    SWOT = "swot"
    TIMELINE = "timeline"
    ROADMAP = "roadmap"

@dataclass
class Project:
    name: str
    description: str
    created_at: str
    analyses: Dict = None
    id: int = None  # Veritabanı için id alanı eklendi

    def __post_init__(self):
        if self.analyses is None:
            self.analyses = {}
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "analyses": self.analyses
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            name=data['name'],
            description=data['description'],
            created_at=data['created_at'],
            analyses=data['analyses']
        )