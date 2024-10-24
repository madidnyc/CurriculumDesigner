from openai import AsyncOpenAI
from datetime import datetime
from pathlib import Path
from typing import Optional
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
    # ... (keep all the existing methods) ...

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
