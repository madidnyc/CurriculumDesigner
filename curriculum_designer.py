from openai import AsyncOpenAI
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
import json
import asyncio

from models_final import (
    CurriculumComponentType, 
    CurriculumComponent, 
    CurriculumEvaluation, 
    CurriculumImprovement,
    LearnerProfile,
    LearningPathway
)
from curriculum_evaluator import CurriculumEvaluator

# ... rest of the file remains the same ...

class CurriculumDesigner:
    def __init__(self):
        self.client = AsyncOpenAI()

    # ... (keep all the existing methods) ...

    async def generate_component_async(
        self,
        topic: str,
        component_type: CurriculumComponentType,
        difficulty: str,
        additional_context: Optional[str] = None,
        auto_improve: bool = False
    ) -> Tuple[CurriculumComponent, CurriculumEvaluation, Optional[CurriculumImprovement]]:
        print(f"\n🔧 Generating {component_type.value} for '{topic}'...")
        
        messages = [
            {"role": "system", "content": "You are an AI curriculum designer specializing in creating high-quality educational components."},
            {"role": "user", "content": f"""
Create a {component_type.value} for the topic: {topic}
Difficulty level: {difficulty}
Additional context: {additional_context or 'None provided'}

Please generate a curriculum component that is:
1. Aligned with the topic and difficulty level
2. Engaging and relevant to learners
3. Clear and well-structured
4. Adaptable to different learning styles

Respond with a JSON object representing a CurriculumComponent with the following fields:
- content: str
- component_type: str (one of: learning_objective, content_sequence, learning_activity, assessment, resource_recommendation)
- difficulty_level: str
- estimated_time: int (in minutes)
- prerequisites: list of strings (optional)

Ensure your response is a valid JSON object.
"""}
        ]

        result = await self.client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        try:
            component_data = json.loads(result.choices[0].message.content)
            component = CurriculumComponent(
                content=component_data['content'],
                component_type=CurriculumComponentType(component_data['component_type']),
                difficulty_level=component_data['difficulty_level'],
                estimated_time=component_data['estimated_time'],
                prerequisites=component_data.get('prerequisites')
            )
            print("✅ Component generated successfully.")
        except json.JSONDecodeError:
            print("❌ Failed to parse JSON response. Using raw content instead.")
            component = CurriculumComponent(
                content=result.choices[0].message.content,
                component_type=component_type,
                difficulty_level=difficulty,
                estimated_time=30,  # Default to 30 minutes
                prerequisites=None
            )
        
        evaluator = CurriculumEvaluator(Path("generated_content"))
        evaluation = await evaluator.evaluate_component(component)
        
        improvement = None
        if auto_improve:
            improvement = await evaluator.improve_component(component, evaluation)
        
        return component, evaluation, improvement

    # ... (rest of the class remains unchanged)

    def _display_results(self, result: CurriculumComponent, evaluation: CurriculumEvaluation, improvement: Optional[CurriculumImprovement], component_type: CurriculumComponentType, topic: str):
        print("\n📊 Evaluation Results:")
        print(f"Component Type: {component_type.value}")
        print(f"Topic: {topic}")
        print(f"\nContent:\n{result.content}")
        print(f"\nDifficulty Level: {result.difficulty_level}")
        print(f"Estimated Time: {result.estimated_time} minutes")
        if result.prerequisites:
            print(f"Prerequisites: {', '.join(result.prerequisites)}")
        
        print("\nEvaluation Scores:")
        for aspect, score in evaluation.model_dump().items():
            if aspect != 'timestamp':
                print(f"{aspect.replace('_', ' ').title()}: {score['score']}/10")
                print(f"  Reasoning: {score['reasoning']}")
                if score['suggestions']:
                    print("  Suggestions:")
                    for suggestion in score['suggestions']:
                        print(f"    - {suggestion}")
        
        if improvement:
            print("\nImprovement Suggestions:")
            for change in improvement.changes_made:
                print(f"- {change}")
            print("\nImproved Content:")
            print(improvement.improved_component.content)

    async def interactive_design_async(self):
        print("\n🤖 === Curriculum Designer ===")
        
        print("\n📝 Available component types:")
        for i, component_type in enumerate(CurriculumComponentType, 1):
            print(f"{i}. {component_type.value.replace('_', ' ').title()}")
        
        while True:
            try:
                choice = int(input("\n🔍 Select component type (enter number): "))
                if 1 <= choice <= len(CurriculumComponentType):
                    component_type = list(CurriculumComponentType)[choice - 1]
                    break
                print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        topic = input("\n📋 Enter the topic: ").strip()
        difficulty = input("\n🎚️ Enter the difficulty level (beginner/intermediate/advanced): ").strip().lower()
        additional_context = input("\n📌 Enter any additional context (press Enter to skip): ").strip()
        
        print("\n🚀 Starting curriculum component generation process...")
        result, evaluation, improvement = await self.generate_component_async(
            topic=topic,
            component_type=component_type,
            difficulty=difficulty,
            additional_context=additional_context,
            auto_improve=True
        )
        
        self._display_results(result, evaluation, improvement, component_type, topic)
        return result, evaluation, improvement

    def interactive_design(self):
        return asyncio.run(self.interactive_design_async())

# Add this block at the end of the file
if __name__ == "__main__":
    designer = CurriculumDesigner()
    
    while True:
        designer.interactive_design()
        
        if input("\nWould you like to design more curriculum components? (y/n): ").lower() != 'y':
            print("\nThank you for using the Curriculum Designer!")
            break
