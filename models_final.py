from pydantic import BaseModel
from enum import Enum
from typing import Optional, List, Dict

class CurriculumComponentType(Enum):
    LEARNING_OBJECTIVE = "learning_objective"
    CONTENT_SEQUENCE = "content_sequence"
    LEARNING_ACTIVITY = "learning_activity"
    ASSESSMENT = "assessment"
    RESOURCE_RECOMMENDATION = "resource_recommendation"

class CurriculumComponent(BaseModel):
    content: str
    component_type: CurriculumComponentType
    difficulty_level: str
    estimated_time: int  # in minutes
    prerequisites: List[str] = []

class EvaluationScore(BaseModel):
    reasoning: str
    score: float  # 0-10 scale
    suggestions: List[str]

class CurriculumEvaluation(BaseModel):
    learning_effectiveness: EvaluationScore
    engagement: EvaluationScore
    accessibility: EvaluationScore
    standards_alignment: EvaluationScore
    differentiation: EvaluationScore
    timestamp: str

class CurriculumImprovement(BaseModel):
    original_component: CurriculumComponent
    improved_component: CurriculumComponent
    changes_made: List[str]
    improvement_focus: List[str]

class LearnerProfile(BaseModel):
    learner_id: str
    knowledge_level: Dict[str, float]  # topic: proficiency (0-1)
    learning_style: str
    goals: List[str]
    completed_components: List[str]

class LearningPathway(BaseModel):
    learner_id: str
    components: List[CurriculumComponent]
    current_position: int
    completion_percentage: float

class LMSIntegration(BaseModel):
    lms_name: str
    api_endpoint: str
    authentication_token: str
    supported_features: List[str]
