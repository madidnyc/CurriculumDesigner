from openai import AsyncOpenAI
from datetime import datetime
from pathlib import Path
import json
import asyncio
from models_final import CurriculumComponentType, CurriculumComponent, EvaluationScore, CurriculumEvaluation, CurriculumImprovement

class BaseCurriculumEvaluationAgent:
    def __init__(self):
        self.client = AsyncOpenAI()
        
    @property
    def learning_effectiveness_prompt(self) -> str:
        raise NotImplementedError
        
    @property
    def engagement_prompt(self) -> str:
        raise NotImplementedError
        
    @property
    def accessibility_prompt(self) -> str:
        raise NotImplementedError

    @property
    def standards_alignment_prompt(self) -> str:
        raise NotImplementedError

    @property
    def differentiation_prompt(self) -> str:
        raise NotImplementedError

    async def evaluate_aspect(self, aspect: str, component: CurriculumComponent) -> EvaluationScore:
        prompts = {
            "learning_effectiveness": self.learning_effectiveness_prompt,
            "engagement": self.engagement_prompt,
            "accessibility": self.accessibility_prompt,
            "standards_alignment": self.standards_alignment_prompt,
            "differentiation": self.differentiation_prompt
        }
        
        messages = [
            {"role": "system", "content": prompts[aspect]},
            {"role": "user", "content": f"Component: {component.model_dump_json()}"}
        ]

        completion = await self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            response_format=EvaluationScore
        )
        
        return completion.choices[0].message.parsed

class LearningObjectiveEvaluationAgent(BaseCurriculumEvaluationAgent):
    @property
    def learning_effectiveness_prompt(self) -> str:
        return """Evaluate the learning effectiveness of this learning objective. Consider:
- Is it clear and specific?
- Is it measurable?
- Is it aligned with the overall curriculum goals?
- Does it target an appropriate cognitive level?"""

    @property
    def engagement_prompt(self) -> str:
        return """Evaluate the engagement potential of this learning objective. Consider:
- Is it relevant to the learners?
- Does it inspire curiosity or interest?
- Is it challenging yet achievable?
- Does it connect to real-world applications?"""

    @property
    def accessibility_prompt(self) -> str:
        return """Evaluate the accessibility of this learning objective. Consider:
- Is it free from bias or discrimination?
- Can it be achieved by learners with diverse abilities?
- Is the language clear and understandable?
- Does it allow for multiple means of achievement?"""

    @property
    def standards_alignment_prompt(self) -> str:
        return """Evaluate how well the learning objective aligns with educational standards. Consider:
- Does it match relevant curriculum standards?
- Is it appropriate for the intended grade level or course?
- Does it support broader educational goals?
- Is it consistent with best practices in the field?"""

    @property
    def differentiation_prompt(self) -> str:
        return """Evaluate the differentiation potential of this learning objective. Consider:
- Can it be easily adapted for different skill levels?
- Does it allow for multiple learning styles?
- Can it be broken down into sub-objectives for struggling learners?
- Can it be extended for advanced learners?"""

# Similar classes for ContentSequenceEvaluationAgent, LearningActivityEvaluationAgent, 
# AssessmentEvaluationAgent, and ResourceRecommendationEvaluationAgent would be implemented here

class CurriculumEvaluator:
    def __init__(self, output_dir: Path):
        self.eval_dir = output_dir / "evaluations"
        self.eval_dir.mkdir(exist_ok=True)
        
        self.client = AsyncOpenAI()
        
        self.evaluation_agents = {
            CurriculumComponentType.LEARNING_OBJECTIVE: LearningObjectiveEvaluationAgent(),
            # Add other evaluation agents here
        }

    async def _evaluate_aspect(self, aspect: str, component: CurriculumComponent) -> EvaluationScore:
        print(f"🔍 Evaluating {aspect.replace('_', ' ')}...")
        
        agent = self.evaluation_agents[component.component_type]
        return await agent.evaluate_aspect(aspect, component)

    async def evaluate_component(self, component: CurriculumComponent) -> CurriculumEvaluation:
        print("\n📊 Starting parallel curriculum component evaluation...")
        
        tasks = {
            aspect: asyncio.create_task(self._evaluate_aspect(aspect, component))
            for aspect in ["learning_effectiveness", "engagement", "accessibility", "standards_alignment", "differentiation"]
        }
        
        results = await asyncio.gather(*tasks.values())
        evaluations = dict(zip(tasks.keys(), results))
        
        return CurriculumEvaluation(
            **evaluations,
            timestamp=datetime.now().isoformat()
        )

    async def improve_component(
        self,
        original_component: CurriculumComponent,
        evaluation: CurriculumEvaluation
    ) -> CurriculumImprovement:
        print("\n✏️ Generating curriculum component improvement based on evaluation...")
        
        eval_summary = {
            "learning_effectiveness": {
                "score": evaluation.learning_effectiveness.score,
                "suggestions": evaluation.learning_effectiveness.suggestions
            },
            "engagement": {
                "score": evaluation.engagement.score,
                "suggestions": evaluation.engagement.suggestions
            },
            "accessibility": {
                "score": evaluation.accessibility.score,
                "suggestions": evaluation.accessibility.suggestions
            },
            "standards_alignment": {
                "score": evaluation.standards_alignment.score,
                "suggestions": evaluation.standards_alignment.suggestions
            },
            "differentiation": {
                "score": evaluation.differentiation.score,
                "suggestions": evaluation.differentiation.suggestions
            }
        }
        
        messages = [
            {"role": "system", "content": "You are improving curriculum components based on specific evaluation feedback."},
            {"role": "user", "content": f"""
Original Component: {original_component.model_dump_json()}

Evaluation Feedback:
{json.dumps(eval_summary, indent=2)}

Please improve the component addressing the evaluation feedback while maintaining its original purpose and difficulty level.
"""}
        ]
        
        result = await self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            response_format=CurriculumImprovement
        )
        
        return result.choices[0].message.parsed

    def save_evaluation(self, evaluation: CurriculumEvaluation, component_id: str, component_type: CurriculumComponentType):
        """Save evaluation results to a JSON file"""
        print(f"\n💾 Saving evaluation results...")
        eval_path = self.eval_dir / component_type.value
        eval_path.mkdir(exist_ok=True)
        
        filepath = eval_path / f"{component_id}_evaluation.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evaluation.model_dump(), f, indent=2)
        print(f"✓ Evaluation saved to: {filepath}")
