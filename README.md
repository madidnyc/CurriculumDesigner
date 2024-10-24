# AI Curriculum Design & Evaluation System

A sophisticated instructional design system that leverages AI to create, analyze, and optimize adaptive learning experiences.

## Overview

This system combines advanced curriculum design capabilities with comprehensive evaluation features to generate, assess, and improve educational content:

- Learning Objectives
- Content Sequences
- Learning Activities
- Assessments
- Resource Recommendations

## Key Features

### 1. Adaptive Curriculum Generation
- AI-powered learning path creation
- Dynamic content sequencing
- Personalized activity suggestions
- Automated assessment design
- Smart resource recommendations

### 2. Multi-Dimensional Curriculum Evaluation
Each curriculum component is evaluated across five key dimensions:

- **Learning Effectiveness**: Measures potential impact on learning outcomes
- **Engagement**: Analyzes student engagement potential
- **Accessibility**: Evaluates inclusive design elements
- **Standards Alignment**: Assesses alignment with educational standards
- **Differentiation**: Measures adaptability for diverse learners

### 3. Real-Time Optimization
- Continuous learning pathway adjustment
- AI-powered content adaptation
- Detailed improvement recommendations
- Performance analytics integration
- Learning outcome tracking

### 4. Curriculum Management
- Structured curriculum storage
- Evaluation results in JSON format
- Version control and iteration tracking
- Integration with major LMS platforms

## Getting Started

1. Install the required packages:
   ```
   pip install openai pydantic python-dotenv
   ```

2. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Run the main script:
   ```
   python curriculum_designer.py
   ```

## Usage

The system provides an interactive interface for curriculum design:

1. Choose the curriculum component type (Learning Objective, Content Sequence, Learning Activity, Assessment, or Resource Recommendation)
2. Enter the topic
3. Specify the desired difficulty level
4. Provide any additional context (optional)

The system will then:
- Generate the curriculum component
- Evaluate it across multiple dimensions
- Automatically improve if necessary
- Save all outputs to appropriate directories

## Project Structure

- `curriculum_designer.py`: Main script with curriculum design agents and assistant logic
- `models_final.py`: Pydantic models for data structures
- `curriculum_evaluator.py`: Curriculum evaluation and improvement logic

## Future Enhancements

- Implement more sophisticated learning pathway generation algorithms
- Enhance adaptation logic based on learner profiles and performance data
- Develop robust interfaces for LMS integration
- Create more detailed assessment design and analysis features
- Implement collaborative curriculum design features for multiple instructors
- Develop data visualization tools for curriculum effectiveness and learner progress

## Contributing

Contributions to improve and expand the AI Curriculum Design & Evaluation System are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
