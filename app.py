import streamlit as st
import os
from datetime import datetime, timedelta
import json
import PyPDF2
import docx
from PIL import Image
import io
import base64
from typing import Dict, List, Optional
import hashlib
import time

# Page configuration
st.set_page_config(
    page_title="EXCELERATE AI Internship Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header with Gradient */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInDown 0.6s ease-out;
    }
    
    /* Week Banner with Glass Effect */
    .week-banner {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        animation: fadeIn 0.8s ease-out;
    }
    
    .week-banner h2 {
        margin: 0 0 0.5rem 0;
        font-size: 2rem;
        font-weight: 600;
    }
    
    .week-banner p {
        margin: 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Progress Bar Styling */
    .week-progress {
        margin-top: 1rem;
    }
    
    .week-progress .stProgress > div > div {
        background: rgba(255, 255, 255, 0.3);
    }
    
    .week-progress .stProgress > div > div > div {
        background: white;
    }
    
    /* Task Cards with Hover Effects */
    .task-card {
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .task-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }
    
    .task-card:hover {
        border-color: #667eea;
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15);
        transform: translateY(-4px);
    }
    
    .task-card:hover::before {
        transform: scaleY(1);
    }
    
    /* Status Badges with Modern Design */
    .status-badge {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-not-started {
        background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
        color: #000;
        box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
    }
    
    .status-in-progress {
        background: linear-gradient(135deg, #17a2b8 0%, #00bcd4 100%);
        color: #fff;
        box-shadow: 0 4px 12px rgba(23, 162, 184, 0.3);
    }
    
    .status-completed {
        background: linear-gradient(135deg, #28a745 0%, #4caf50 100%);
        color: #fff;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
    }
    
    .status-overdue {
        background: linear-gradient(135deg, #dc3545 0%, #f44336 100%);
        color: #fff;
        box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
    }
    
    /* Chat Messages with Modern Bubbles */
    .chat-message {
        padding: 1.2rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        animation: slideIn 0.3s ease-out;
        max-width: 85%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        margin-right: 0;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2c3e50;
        margin-right: auto;
        margin-left: 0;
        border-bottom-left-radius: 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .system-message {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe5a3 100%);
        text-align: center;
        font-style: italic;
        margin: 0 auto;
        box-shadow: 0 4px 12px rgba(255, 193, 7, 0.2);
    }
    
    .message-timestamp {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    
    /* Metric Cards with Gradient */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.95rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* AI Insight Box */
    .ai-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Prompt Template Cards */
    .prompt-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .prompt-card:hover {
        transform: translateX(8px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
    }
    
    .prompt-template {
        background: #2d3748;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        margin-top: 0.5rem;
    }
    
    /* Workflow Step */
    .workflow-step {
        background: white;
        border-left: 4px solid #28a745;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .workflow-step:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        transform: translateX(4px);
    }
    
    /* Deliverable Preview */
    .deliverable-preview {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px dashed #667eea;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .deliverable-preview:hover {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-color: #764ba2;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        }
        50% {
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
        }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* File Uploader */
    .uploadedFile {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #4caf50;
    }
    
    /* Quick Action Chips */
    .quick-action {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Loading Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        border-radius: 8px;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
        border-radius: 8px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 4px solid #17a2b8;
        border-radius: 8px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #ffc107;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'messages': [],
        'uploaded_files_content': [],
        'current_task': None,
        'current_week': 1,
        'learning_mode': 'guided',
        'tasks_status': {},
        'user_role': 'intern',
        'intern_profile': {
            'name': 'New Intern',
            'start_date': datetime.now(),
            'skills': {},
            'completed_modules': []
        },
        'prompt_history': [],
        'feedback_received': [],
        'ai_insights': [],
        'workflow_state': {},
        'selected_prompt_template': None,
        'chat_context': '',
        'typing_indicator': False,
        'deliverable_status': {},
        'skill_assessments': {},
        'collaboration_notes': [],
        'bookmarked_messages': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Enhanced Task Database with Weekly Structure
WEEKLY_CURRICULUM = {
    1: {
        'title': 'Foundation & Tool Discovery',
        'description': 'Introduction to prompt engineering and AI tool exploration',
        'icon': '🎯',
        'color': '#667eea',
        'objectives': [
            'Understand prompt engineering fundamentals',
            'Explore AI tools and frameworks',
            'Conduct initial tool analysis',
            'Develop research plan'
        ],
        'tasks': [
            {
                'id': 'w1_t1',
                'title': 'Prompt Engineering Fundamentals',
                'type': 'learning',
                'description': 'Learn the basics of prompt engineering and its applications',
                'estimated_hours': 3,
                'ai_support_level': 'high',
                'icon': '📚'
            },
            {
                'id': 'w1_t2',
                'title': 'AI Tools Introduction',
                'type': 'research',
                'description': 'Explore OpenAI, Hugging Face, and other platforms',
                'estimated_hours': 4,
                'ai_support_level': 'medium',
                'icon': '🔬'
            },
            {
                'id': 'w1_t3',
                'title': 'Tool Comparative Analysis',
                'type': 'analysis',
                'description': 'Compare two selected AI tools',
                'estimated_hours': 5,
                'ai_support_level': 'high',
                'icon': '📊'
            },
            {
                'id': 'w1_t4',
                'title': 'Draft Research Plan',
                'type': 'deliverable',
                'description': 'Create structured research methodology',
                'estimated_hours': 4,
                'ai_support_level': 'high',
                'icon': '📝',
                'due_date_offset': 7
            }
        ],
        'deliverables': [
            'Comparative Analysis Document (2 tools)',
            'Draft Research Plan'
        ],
        'resources': [
            'Prompt Engineering Guide',
            'AI Tools Comparison Framework',
            'Research Methodology Templates'
        ]
    },
    2: {
        'title': 'Deep Research & Analysis',
        'description': 'Detailed tool research and real-world application analysis',
        'icon': '🔍',
        'color': '#17a2b8',
        'objectives': [
            'Conduct detailed tool research',
            'Document features and specifications',
            'Analyze real-world applications',
            'Draft comparative analysis report'
        ],
        'tasks': [
            {
                'id': 'w2_t1',
                'title': 'Detailed Tool Research',
                'type': 'research',
                'description': 'Deep dive into selected tools capabilities',
                'estimated_hours': 6,
                'ai_support_level': 'high',
                'icon': '🔬'
            },
            {
                'id': 'w2_t2',
                'title': 'Feature Documentation',
                'type': 'documentation',
                'description': 'Document specifications, strengths, limitations',
                'estimated_hours': 5,
                'ai_support_level': 'high',
                'icon': '📋'
            },
            {
                'id': 'w2_t3',
                'title': 'Real-World Applications Analysis',
                'type': 'analysis',
                'description': 'Analyze industry use cases and applications',
                'estimated_hours': 5,
                'ai_support_level': 'medium',
                'icon': '🌍'
            },
            {
                'id': 'w2_t4',
                'title': 'Comparative Analysis Report',
                'type': 'deliverable',
                'description': 'Complete comparative analysis document',
                'estimated_hours': 6,
                'ai_support_level': 'high',
                'icon': '📄',
                'due_date_offset': 7
            }
        ],
        'deliverables': [
            'Tool Research Document',
            'Feature Documentation',
            'Comparative Analysis Report'
        ],
        'resources': [
            'Tool Documentation Templates',
            'Industry Case Studies',
            'Analysis Framework Guide'
        ]
    },
    3: {
        'title': 'Integration & Application',
        'description': 'Tool integration analysis and practical use case development',
        'icon': '🔗',
        'color': '#28a745',
        'objectives': [
            'Analyze tool integration potential',
            'Assess feasibility and barriers',
            'Develop practical use cases',
            'Formulate recommendations'
        ],
        'tasks': [
            {
                'id': 'w3_t1',
                'title': 'Integration Analysis',
                'type': 'analysis',
                'description': 'Map tools to EXCELERATE opportunities',
                'estimated_hours': 5,
                'ai_support_level': 'high',
                'icon': '🎯'
            },
            {
                'id': 'w3_t2',
                'title': 'Feasibility Assessment',
                'type': 'analysis',
                'description': 'Evaluate technical and operational feasibility',
                'estimated_hours': 4,
                'ai_support_level': 'medium',
                'icon': '⚖️'
            },
            {
                'id': 'w3_t3',
                'title': 'Use Case Development',
                'type': 'creative',
                'description': 'Create practical application scenarios',
                'estimated_hours': 5,
                'ai_support_level': 'high',
                'icon': '💡'
            },
            {
                'id': 'w3_t4',
                'title': 'Final Recommendations',
                'type': 'deliverable',
                'description': 'Complete recommendations document',
                'estimated_hours': 6,
                'ai_support_level': 'high',
                'icon': '🎁',
                'due_date_offset': 7
            }
        ],
        'deliverables': [
            'Final Recommendations Document',
            'Engagement Enhancement Blueprint',
            'Implementation Plan'
        ],
        'resources': [
            'Integration Framework',
            'Feasibility Analysis Template',
            'Use Case Examples'
        ]
    },
    4: {
        'title': 'Synthesis & Presentation',
        'description': 'Final report compilation and presentation delivery',
        'icon': '🎤',
        'color': '#ffc107',
        'objectives': [
            'Compile comprehensive final report',
            'Create professional presentation',
            'Prepare for live delivery',
            'Respond to stakeholder questions'
        ],
        'tasks': [
            {
                'id': 'w4_t1',
                'title': 'Final Report Compilation',
                'type': 'deliverable',
                'description': 'Aggregate all research into final report',
                'estimated_hours': 8,
                'ai_support_level': 'high',
                'icon': '📘'
            },
            {
                'id': 'w4_t2',
                'title': 'Presentation Creation',
                'type': 'deliverable',
                'description': 'Design 8-12 slide PowerPoint',
                'estimated_hours': 6,
                'ai_support_level': 'high',
                'icon': '🎨'
            },
            {
                'id': 'w4_t3',
                'title': 'Presentation Rehearsal',
                'type': 'practice',
                'description': 'Practice delivery with AI feedback',
                'estimated_hours': 3,
                'ai_support_level': 'medium',
                'icon': '🎭'
            },
            {
                'id': 'w4_t4',
                'title': 'Final Presentation',
                'type': 'deliverable',
                'description': 'Live presentation with Q&A',
                'estimated_hours': 2,
                'ai_support_level': 'low',
                'icon': '🎯',
                'due_date_offset': 7
            }
        ],
        'deliverables': [
            'Final Report (5-10 pages)',
            'PowerPoint Presentation (8-12 slides)',
            'Live Presentation Recording'
        ],
        'resources': [
            'Report Template',
            'Presentation Design Guide',
            'Q&A Preparation Framework'
        ]
    }
}

# Enhanced Prompt Library
PROMPT_LIBRARY = {
    'research': {
        'tool_analysis': {
            'name': 'Tool Feature Extraction',
            'description': 'Extract and organize tool features from documentation',
            'template': """Analyze the uploaded {document_type} about {tool_name}. Extract and organize:
- Core features (list top 10)
- Key capabilities (categorize by type)
- Technical specifications (hardware, software, integrations)
- Pricing structure (plans, costs, licensing)
- Limitations or constraints mentioned

Present in a structured table format.""",
            'variables': ['document_type', 'tool_name'],
            'best_for': 'Week 1-2, Tool research tasks',
            'icon': '🔬'
        },
        'comparative_analysis': {
            'name': 'Comparative Analysis',
            'description': 'Compare multiple tools across dimensions',
            'template': """Compare {tool_a} and {tool_b} across the following dimensions:
- Ease of use (rate 1-10 with justification)
- Features (unique vs. shared)
- Use cases (identify 3 ideal scenarios for each)
- Cost-effectiveness (price vs. value analysis)
- Integration potential with {target_system}

Create a side-by-side comparison table and provide a recommendation.""",
            'variables': ['tool_a', 'tool_b', 'target_system'],
            'best_for': 'Week 1-2, Comparative tasks',
            'icon': '⚖️'
        },
        'use_case_generation': {
            'name': 'Use Case Generator',
            'description': 'Generate practical use cases for tools',
            'template': """Given {tool_name} with capabilities {capabilities}, generate 5 specific use cases for {organization}. For each use case, provide:
- Scenario description
- Problem being solved
- Implementation approach
- Expected benefits (quantified when possible)
- Potential challenges

Format as numbered list with subsections.""",
            'variables': ['tool_name', 'capabilities', 'organization'],
            'best_for': 'Week 3, Use case development',
            'icon': '💡'
        }
    },
    'documentation': {
        'report_structure': {
            'name': 'Report Outline Generator',
            'description': 'Create structured report outlines',
            'template': """I need to write a {report_type} report about {topic}. Create a detailed outline with:
- Section headings and subheadings
- Key points to cover in each section
- Suggested length for each section
- Visual aids to include (charts, tables, diagrams)

Total target length: {target_length} pages""",
            'variables': ['report_type', 'topic', 'target_length'],
            'best_for': 'Week 2-4, Report writing',
            'icon': '📝'
        },
        'executive_summary': {
            'name': 'Executive Summary Generator',
            'description': 'Create concise executive summaries',
            'template': """Summarize the following {document_length} {document_type} into a 1-page executive summary highlighting:
- Main objectives
- Key findings (top 3-5)
- Critical recommendations
- Next steps

Use clear, concise language suitable for senior stakeholders.

[Document content]: {content}""",
            'variables': ['document_length', 'document_type', 'content'],
            'best_for': 'Week 4, Final report',
            'icon': '📄'
        }
    },
    'learning': {
        'concept_explanation': {
            'name': 'Concept Explainer',
            'description': 'Explain complex concepts simply',
            'template': """Explain {concept} to someone with {expertise_level} background. Include:
- Definition in simple terms
- Why it matters (real-world relevance)
- Key components or principles
- A practical example or analogy
- Common misconceptions to avoid

Keep it under {word_limit} words.""",
            'variables': ['concept', 'expertise_level', 'word_limit'],
            'best_for': 'Any week, Learning support',
            'icon': '💡'
        },
        'tutorial_creation': {
            'name': 'Step-by-Step Tutorial',
            'description': 'Create detailed tutorials',
            'template': """Create a step-by-step tutorial for {task}. Structure:
1. Prerequisites (what learner needs to know/have)
2. Learning objectives (what they'll accomplish)
3. Detailed steps (break down into 5-10 stages)
4. Examples for each step
5. Common errors and troubleshooting
6. Practice exercise to reinforce learning

Include code examples where relevant.""",
            'variables': ['task'],
            'best_for': 'Any week, Skill building',
            'icon': '📚'
        }
    },
    'collaboration': {
        'meeting_agenda': {
            'name': 'Meeting Agenda Generator',
            'description': 'Create structured meeting agendas',
            'template': """Create a meeting agenda for {meeting_type} about {topic}. Include:
- Meeting objectives (what we want to accomplish)
- Agenda items (5-8 topics)
- Time allocation for each item
- Discussion leader for each item
- Pre-meeting preparation needed
- Expected outcomes/decisions

Total meeting time: {duration} minutes""",
            'variables': ['meeting_type', 'topic', 'duration'],
            'best_for': 'Any week, Team collaboration',
            'icon': '📅'
        },
        'feedback_synthesis': {
            'name': 'Feedback Synthesizer',
            'description': 'Consolidate and organize feedback',
            'template': """I received feedback from {sources} about {work_product}. Synthesize this feedback by:
- Identifying common themes (group similar points)
- Prioritizing by importance and frequency
- Categorizing as: Critical issues, Improvements, Positive highlights
- Suggesting concrete action items for each category

Present as actionable list.

[Feedback content]: {feedback}""",
            'variables': ['sources', 'work_product', 'feedback'],
            'best_for': 'Any week, Feedback processing',
            'icon': '🔄'
        }
    },
    'evaluation': {
        'self_assessment': {
            'name': 'Self-Assessment Guide',
            'description': 'Guide self-reflection and assessment',
            'template': """Help me assess my work on {task}. Guide me through:
- What went well (3-5 strengths)
- What could be improved (3-5 areas)
- Skills demonstrated (list and rate 1-10)
- Skills to develop (identify gaps)
- Specific action items for improvement

Be constructive and specific.""",
            'variables': ['task'],
            'best_for': 'End of each week, Reflection',
            'icon': '🎯'
        },
        'quality_check': {
            'name': 'Deliverable Quality Checker',
            'description': 'Pre-submission quality review',
            'template': """Review my {deliverable_type} for quality. Check for:
- Completeness (all required sections present)
- Clarity and organization (logical flow)
- Technical accuracy (facts and data correct)
- Grammar and formatting (professional presentation)
- Citation and references (properly attributed)

Provide a score (1-100) and specific improvement suggestions.

[Deliverable content]: {content}""",
            'variables': ['deliverable_type', 'content'],
            'best_for': 'Before submission, Quality assurance',
            'icon': '✅'
        }
    }
}

# Enhanced System Prompts
def get_system_prompt(mode: str, week: int, task_context: Optional[Dict] = None) -> str:
    """Generate context-aware system prompt"""
    
    base_prompts = {
        'guided': """You are an expert AI tutor for EXCELERATE's Prompt Engineering internship. Your role is to guide learning through discovery, not just provide answers.

CURRENT CONTEXT:
- Week: {week}
- Focus: {week_focus}
- Learning Stage: {stage}

TEACHING APPROACH:
1. Socratic Method: Ask questions that lead to understanding
2. Scaffolding: Build complexity gradually
3. Active Learning: Encourage hands-on practice
4. Growth Mindset: Celebrate progress, frame mistakes as learning

RESPONSE STYLE:
- Use encouraging, supportive language
- Break complex topics into digestible steps
- Provide hints before solutions
- Ask "What do you think?" and "Why?" frequently
- Adapt pace based on responses

DOCUMENT ANALYSIS (RAG):
When documents are provided:
- Analyze thoroughly and reference specific sections
- Connect document content to current task
- Extract key concepts for learning
- Guide navigation through material""",
        
        'direct': """You are an efficient AI assistant for EXCELERATE's Prompt Engineering internship. Provide clear, actionable guidance.

CURRENT CONTEXT:
- Week: {week}
- Focus: {week_focus}
- Task: {task_focus}

ASSISTANCE APPROACH:
1. Direct Solutions: Provide complete, working examples
2. Best Practices: Share industry-standard approaches
3. Efficiency: Minimize back-and-forth, maximize value
4. Clarity: Use clear explanations with proper formatting

DOCUMENT PROCESSING (RAG):
When documents are provided:
- Extract relevant information quickly
- Summarize key points
- Answer specific questions accurately
- Reference document sections precisely"""
    }
    
    week_info = WEEKLY_CURRICULUM.get(week, WEEKLY_CURRICULUM[1])
    prompt = base_prompts[mode].format(
        week=week,
        week_focus=week_info['title'],
        stage=f"Week {week} of 4",
        task_focus=task_context.get('title', 'General') if task_context else 'General'
    )
    
    if task_context:
        prompt += f"\n\nCURRENT TASK: {task_context['title']}\n"
        prompt += f"Description: {task_context['description']}\n"
        prompt += f"Type: {task_context['type']}\n"
        prompt += f"AI Support Level: {task_context['ai_support_level']}\n"
    
    return prompt

# Helper Functions
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def process_uploaded_file(uploaded_file):
    """Process uploaded file and extract content"""
    file_type = uploaded_file.type
    file_name = uploaded_file.name
    
    content = {
        'name': file_name,
        'type': file_type,
        'content': '',
        'processed_date': datetime.now().isoformat()
    }
    
    try:
        if file_type == 'application/pdf':
            content['content'] = extract_text_from_pdf(uploaded_file)
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            content['content'] = extract_text_from_docx(uploaded_file)
        elif file_type == 'text/plain':
            content['content'] = uploaded_file.read().decode('utf-8')
        elif file_type.startswith('image/'):
            image = Image.open(uploaded_file)
            content['image'] = image
            content['content'] = f"[Image: {file_name}]"
        else:
            content['content'] = f"[Unsupported file type: {file_type}]"
    except Exception as e:
        content['content'] = f"[Error processing file: {str(e)}]"
    
    return content

def create_context_from_files():
    """Create enhanced context from uploaded files for RAG"""
    if not st.session_state.uploaded_files_content:
        return ""
    
    context = "\n\n=== UPLOADED DOCUMENTS CONTEXT ===\n\n"
    context += f"The intern has uploaded {len(st.session_state.uploaded_files_content)} document(s) for analysis.\n\n"
    
    for idx, file_content in enumerate(st.session_state.uploaded_files_content):
        context += f"--- Document {idx+1}: {file_content['name']} ---\n"
        context += f"Type: {file_content['type']}\n"
        context += f"Content:\n{file_content['content'][:8000]}\n\n"
    
    context += "=== END DOCUMENTS ===\n\n"
    context += "Use the above documents to provide context-aware assistance. Reference specific sections when relevant.\n"
    
    return context

def get_ai_response(user_message: str, context: str = "") -> str:
    """Get AI response with enhanced context awareness"""
    try:
        from groq import Groq
        
        api_key = st.session_state.get('groq_api_key', '')
        if not api_key:
            return "⚠️ Please enter your Groq API key in the sidebar to use AI features."
        
        client = Groq(api_key=api_key)
        
        # Get current task context
        task_context = None
        if st.session_state.current_task:
            week = st.session_state.current_week
            week_data = WEEKLY_CURRICULUM[week]
            for task in week_data['tasks']:
                if task['id'] == st.session_state.current_task:
                    task_context = task
                    break
        
        # Build system prompt with full context
        system_prompt = get_system_prompt(
            st.session_state.learning_mode,
            st.session_state.current_week,
            task_context
        )
        
        # Add document context
        if context:
            system_prompt += f"\n\n{context}"
        
        # Add prompt template context if selected
        if st.session_state.selected_prompt_template:
            system_prompt += f"\n\nThe intern is using the '{st.session_state.selected_prompt_template}' prompt template. Help them apply it effectively."
        
        # Prepare messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 10 for more context)
        for msg in st.session_state.messages[-10:]:
            if msg['role'] != 'system':
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Get response
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="openai/gpt-oss-120b",
            temperature=0.7,
            max_tokens=2048,
        )
        
        response = chat_completion.choices[0].message.content
        
        # Track prompt usage
        st.session_state.prompt_history.append({
            'timestamp': datetime.now(),
            'prompt': user_message,
            'response_length': len(response),
            'context_used': bool(context)
        })
        
        return response
        
    except Exception as e:
        return f"⚠️ Error getting AI response: {str(e)}"

def calculate_week_progress(week: int) -> float:
    """Calculate progress for a specific week"""
    week_data = WEEKLY_CURRICULUM[week]
    total_tasks = len(week_data['tasks'])
    completed = sum(1 for task in week_data['tasks'] 
                   if st.session_state.tasks_status.get(task['id']) == 'completed')
    return (completed / total_tasks * 100) if total_tasks > 0 else 0

def get_ai_insight() -> str:
    """Generate AI-powered insight based on current progress"""
    week = st.session_state.current_week
    progress = calculate_week_progress(week)
    
    insights = []
    
    if progress < 30:
        insights.append(f"📊 You're {progress:.0f}% through Week {week}. Let's build momentum!")
    elif progress < 70:
        insights.append(f"🎯 Great progress! You're {progress:.0f}% through Week {week}.")
    else:
        insights.append(f"🌟 Excellent! You're {progress:.0f}% through Week {week}!")
    
    # Task-specific insights
    week_data = WEEKLY_CURRICULUM[week]
    pending_tasks = [t for t in week_data['tasks'] 
                    if st.session_state.tasks_status.get(t['id'], 'not_started') != 'completed']
    
    if pending_tasks:
        next_task = pending_tasks[0]
        insights.append(f"⏭️ Next up: {next_task['title']}")
    
    return " ".join(insights)

# Main App Layout
st.markdown('<h1 class="main-header">🎓 EXCELERATE AI Internship Platform</h1>', unsafe_allow_html=True)

# Enhanced Week Banner with Progress
week_data = WEEKLY_CURRICULUM[st.session_state.current_week]
week_progress = calculate_week_progress(st.session_state.current_week)

st.markdown(f"""
<div class="week-banner">
    <h2>{week_data['icon']} Week {st.session_state.current_week}: {week_data['title']}</h2>
    <p>{week_data['description']}</p>
    <div class="week-progress">
        <p style="margin: 0.5rem 0 0.3rem 0; font-size: 0.9rem;">Week Progress: {week_progress:.0f}%</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Add progress bar
st.progress(week_progress / 100)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings & Configuration")
    
    # Role Selection
    st.session_state.user_role = st.selectbox(
        "👤 View As",
        options=['intern', 'mentor', 'admin'],
        format_func=lambda x: {'intern': '🎓 Intern', 'mentor': '👨‍🏫 Mentor', 'admin': '⚡ Admin'}[x]
    )
    
    # API Key
    groq_api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        value=st.session_state.get('groq_api_key', ''),
        help="Get your key at https://console.groq.com"
    )
    if groq_api_key:
        st.session_state.groq_api_key = groq_api_key
        st.success("✅ API Key Connected")
    
    st.divider()
    
    # Week Navigation with Visual Indicators
    st.markdown("### 📅 Week Navigation")
    
    # Display all weeks with progress
    for w in range(1, 5):
        w_data = WEEKLY_CURRICULUM[w]
        w_progress = calculate_week_progress(w)
        
        if w == st.session_state.current_week:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {w_data['color']}20 0%, {w_data['color']}40 100%); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        border-left: 4px solid {w_data['color']};">
                <strong>{w_data['icon']} Week {w}</strong><br>
                <small>{w_data['title']}</small><br>
                <small>Progress: {w_progress:.0f}%</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(f"{w_data['icon']} Week {w}: {w_data['title']}", key=f"nav_week_{w}", use_container_width=True):
                st.session_state.current_week = w
                st.rerun()
    
    st.divider()
    
    # Learning Mode
    st.markdown("### 🧠 Learning Mode")
    learning_mode = st.radio(
        "Choose approach:",
        options=['guided', 'direct'],
        format_func=lambda x: {
            'guided': '🎯 Guided Learning',
            'direct': '⚡ Direct Assistance'
        }[x],
        index=0 if st.session_state.learning_mode == 'guided' else 1
    )
    
    if learning_mode != st.session_state.learning_mode:
        st.session_state.learning_mode = learning_mode
        st.info(f"Switched to {learning_mode.title()} mode")
    
    # Mode description
    if learning_mode == 'guided':
        st.caption("📚 Step-by-step guidance with questions and hints")
    else:
        st.caption("⚡ Quick solutions and immediate answers")
    
    st.divider()
    
    # File Upload with Enhanced UI
    st.markdown("### 📁 Resource Library")
    uploaded_files = st.file_uploader(
        "Upload learning materials",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
        help="PDF, DOCX, TXT, or Images"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if not any(f['name'] == uploaded_file.name for f in st.session_state.uploaded_files_content):
                with st.spinner(f'Processing {uploaded_file.name}...'):
                    content = process_uploaded_file(uploaded_file)
                    st.session_state.uploaded_files_content.append(content)
                    st.success(f"✅ Processed")
    
    # Display uploaded files with enhanced UI
    if st.session_state.uploaded_files_content:
        st.markdown(f"**📚 Uploaded ({len(st.session_state.uploaded_files_content)})**")
        for idx, file_content in enumerate(st.session_state.uploaded_files_content):
            col1, col2 = st.columns([4, 1])
            with col1:
                file_icon = "📄" if "pdf" in file_content['type'] else "📝" if "doc" in file_content['type'] else "🖼️"
                st.caption(f"{file_icon} {file_content['name'][:30]}")
            with col2:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.uploaded_files_content.pop(idx)
                    st.rerun()
    
    st.divider()
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat cleared!")
            st.rerun()
    
    with col2:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.show_analytics = True
    
    # Stats summary
    st.divider()
    st.markdown("### 📈 Quick Stats")
    total_tasks = sum(len(w['tasks']) for w in WEEKLY_CURRICULUM.values())
    completed_tasks = sum(1 for status in st.session_state.tasks_status.values() 
                         if status == 'completed')
    
    st.metric("Tasks Completed", f"{completed_tasks}/{total_tasks}")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Documents", len(st.session_state.uploaded_files_content))

# Main Content Tabs with Icons
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Tasks & Activities",
    "💬 AI Assistant",
    "📚 Prompt Library",
    "🎯 Deliverables",
    "📈 Progress & Analytics",
    "🎓 Skills & Learning"
])

# Tab 1: Tasks & Activities
with tab1:
    st.markdown(f"## {week_data['icon']} Week {st.session_state.current_week} Tasks")
    
    # Learning Objectives in expandable card
    with st.expander("🎯 Learning Objectives for This Week", expanded=True):
        for obj in week_data['objectives']:
            st.markdown(f"✓ {obj}")
    
    # AI Insight Box
    st.markdown(f'<div class="ai-insight">🤖 AI Insight: {get_ai_insight()}</div>', unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        task_filter = st.selectbox(
            "Filter by status",
            options=['all', 'not_started', 'in_progress', 'completed'],
            format_func=lambda x: {
                'all': 'All Tasks',
                'not_started': '⚪ Not Started',
                'in_progress': '🔵 In Progress',
                'completed': '✅ Completed'
            }[x]
        )
    
    with col2:
        sort_by = st.selectbox("Sort by", ['default', 'hours', 'status'])
    
    # Tasks Display
    for task in week_data['tasks']:
        status = st.session_state.tasks_status.get(task['id'], 'not_started')
        
        # Apply filter
        if task_filter != 'all' and status != task_filter:
            continue
        
        with st.container():
            st.markdown('<div class="task-card">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"### {task['icon']} {task['title']}")
                st.write(task['description'])
                
                # Task metadata
                meta_col1, meta_col2, meta_col3 = st.columns(3)
                with meta_col1:
                    st.caption(f"⏱️ {task['estimated_hours']}h")
                with meta_col2:
                    st.caption(f"🤖 AI: {task['ai_support_level']}")
                with meta_col3:
                    st.caption(f"📌 {task['type'].title()}")
            
            with col2:
                type_colors = {
                    'learning': '#667eea',
                    'research': '#17a2b8',
                    'analysis': '#28a745',
                    'documentation': '#ffc107',
                    'deliverable': '#dc3545',
                    'creative': '#e83e8c',
                    'practice': '#6f42c1'
                }
                st.markdown(f"""
                <div style="background: {type_colors.get(task['type'], '#6c757d')}20; 
                           padding: 0.5rem; border-radius: 8px; text-align: center;">
                    <small style="color: {type_colors.get(task['type'], '#6c757d')}; font-weight: 600;">
                        {task['type'].upper()}
                    </small>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                status_class = f"status-{status.replace('_', '-')}"
                status_text = status.replace('_', ' ').title()
                st.markdown(f'<span class="status-badge {status_class}">{status_text}</span>', unsafe_allow_html=True)
            
            # Action buttons in a clean row
            st.markdown("**Actions:**")
            action_col1, action_col2, action_col3, action_col4 = st.columns(4)
            
            with action_col1:
                if st.button(f"🎯 Start", key=f"start_{task['id']}", use_container_width=True):
                    st.session_state.current_task = task['id']
                    st.session_state.tasks_status[task['id']] = 'in_progress'
                    
                    welcome_msg = f"""🎯 Let's work on: **{task['title']}**

📋 **Description:** {task['description']}

⏱️ **Estimated Time:** {task['estimated_hours']} hours
🤖 **AI Support Level:** {task['ai_support_level']}
{task['icon']} **Type:** {task['type'].title()}

{"🎓 I'll guide you step-by-step with questions and hints to help you learn effectively." if st.session_state.learning_mode == 'guided' else '⚡ I can provide direct solutions and quick assistance to help you complete this efficiently.'}

What aspect of this task would you like to tackle first?"""
                    
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': welcome_msg,
                        'timestamp': datetime.now()
                    })
                    st.success("Task started! Check the AI Assistant tab.")
                    time.sleep(1)
                    st.rerun()
            
            with action_col2:
                if st.button("💬 Ask AI", key=f"ask_{task['id']}", use_container_width=True):
                    st.session_state.current_task = task['id']
                    st.info("Navigate to AI Assistant tab to start chatting!")
            
            with action_col3:
                if st.button("✅ Complete", key=f"done_{task['id']}", use_container_width=True):
                    st.session_state.tasks_status[task['id']] = 'completed'
                    st.balloons()
                    st.success(f"🎉 Task completed!")
                    time.sleep(1)
                    st.rerun()
            
            with action_col4:
                if st.button("📝 Notes", key=f"notes_{task['id']}", use_container_width=True):
                    st.info("Notes feature coming soon!")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Resources Section
    st.divider()
    st.markdown("## 📚 Week Resources")
    
    resource_cols = st.columns(len(week_data['resources']))
    for idx, resource in enumerate(week_data['resources']):
        with resource_cols[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                       padding: 1rem; border-radius: 10px; text-align: center; height: 100px;
                       display: flex; align-items: center; justify-content: center;">
                <strong>📖 {resource}</strong>
            </div>
            """, unsafe_allow_html=True)

# Tab 2: AI Assistant (Enhanced)
with tab2:
    st.markdown("## 💬 AI Learning Assistant")
    
    # Context Bar
    context_col1, context_col2, context_col3 = st.columns([2, 1, 1])
    
    with context_col1:
        if st.session_state.current_task:
            task = next((t for w in WEEKLY_CURRICULUM.values() 
                        for t in w['tasks'] if t['id'] == st.session_state.current_task), None)
            if task:
                st.info(f"📌 **Active Task:** {task['icon']} {task['title']}")
        else:
            st.warning("⚠️ No task selected. Select a task from the Tasks tab.")
    
    with context_col2:
        mode_emoji = '🎯' if st.session_state.learning_mode == 'guided' else '⚡'
        st.caption(f"{mode_emoji} {st.session_state.learning_mode.title()} Mode")
    
    with context_col3:
        st.caption(f"📄 {len(st.session_state.uploaded_files_content)} docs uploaded")
    
    st.divider()
    
    # Chat Container with Enhanced Styling
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.messages:
            # Welcome message
            st.markdown("""
            <div class="ai-insight">
                <h3>👋 Welcome to your AI Learning Assistant!</h3>
                <p>I'm here to help you throughout your internship journey. You can:</p>
                <ul>
                    <li>🎯 Ask questions about your tasks</li>
                    <li>📚 Get explanations of concepts</li>
                    <li>💡 Request examples and tutorials</li>
                    <li>🔍 Analyze your uploaded documents</li>
                    <li>✅ Get feedback on your work</li>
                </ul>
                <p><strong>Tip:</strong> Upload relevant documents to get more accurate, context-aware help!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display messages with enhanced formatting
        for idx, message in enumerate(st.session_state.messages):
            timestamp = message.get('timestamp', datetime.now()).strftime("%I:%M %p")
            
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You</strong>
                    <p style="margin: 0.5rem 0 0 0;">{message["content"]}</p>
                    <div class="message-timestamp">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Bookmark option
                if st.button("🔖 Bookmark", key=f"bookmark_user_{idx}"):
                    st.session_state.bookmarked_messages.append(message)
                    st.success("Message bookmarked!")
                
            elif message['role'] == 'assistant':
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 AI Assistant</strong>
                    <p style="margin: 0.5rem 0 0 0;">{message["content"]}</p>
                    <div class="message-timestamp">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons for AI messages
                msg_col1, msg_col2, msg_col3, msg_col4 = st.columns(4)
                with msg_col1:
                    if st.button("👍 Helpful", key=f"helpful_{idx}"):
                        st.success("Thanks for the feedback!")
                with msg_col2:
                    if st.button("🔖 Save", key=f"save_{idx}"):
                        st.session_state.bookmarked_messages.append(message)
                        st.success("Saved!")
                with msg_col3:
                    if st.button("📋 Copy", key=f"copy_{idx}"):
                        st.info("Content copied to clipboard!")
                with msg_col4:
                    if st.button("🔄 Regenerate", key=f"regen_{idx}"):
                        st.info("Regenerating response...")
    
    st.divider()
    
    # Enhanced Input Area
    st.markdown("### 💭 Your Message")
    
    # Quick Action Chips
    st.markdown("**Quick Actions:**")
    quick_actions_container = st.container()
    
    with quick_actions_container:
        qa_col1, qa_col2, qa_col3, qa_col4 = st.columns(4)
        
        quick_prompts = [
            ("💡 Explain", "Explain this concept in simple terms with examples"),
            ("📝 Example", "Show me a practical example of how to do this"),
            ("🔍 Review", "Review my work and provide detailed feedback"),
            ("💪 Practice", "Give me a practice exercise to reinforce my learning")
        ]
        
        selected_quick = None
        for idx, (label, prompt) in enumerate(quick_prompts):
            with [qa_col1, qa_col2, qa_col3, qa_col4][idx]:
                if st.button(label, key=f"qa_{idx}", use_container_width=True):
                    selected_quick = prompt
    
    # Text input
    user_input = st.text_area(
        "Type your message here...",
        height=120,
        placeholder="Ask a question, share your work, or request help...",
        key="chat_input"
    )
    
    # Use selected quick action if clicked
    if selected_quick:
        user_input = selected_quick
    # Continuation from line 1041 (Send button section)

    # Send button with enhanced options
    send_col1, send_col2, send_col3 = st.columns([3, 1, 1])
    
    with send_col1:
        send_button = st.button("📤 Send Message", type="primary", use_container_width=True)
    
    with send_col2:
        attach_context = st.checkbox("📎 Use Docs", value=True, help="Include uploaded documents in context")
    
    with send_col3:
        if st.button("🎤 Voice", use_container_width=True):
            st.info("Voice input coming soon!")
    
    # Process message
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Create context from files if enabled
        context = ""
        if attach_context:
            context = create_context_from_files()
        
        # Get AI response
        with st.spinner("🤖 AI is thinking..."):
            response = get_ai_response(user_input, context)
        
        # Add assistant message
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now()
        })
        
        st.rerun()
    
    # Conversation starters
    if not st.session_state.messages:
        st.markdown("**💬 Conversation Starters:**")
        starters = [
            "How do I start with prompt engineering?",
            "What are the key features I should analyze?",
            "Can you help me create a research plan?",
            "How should I structure my comparative analysis?"
        ]
        
        for starter in starters:
            if st.button(f"💭 {starter}", key=f"starter_{starters.index(starter)}"):
                st.session_state.messages.append({
                    'role': 'user',
                    'content': starter,
                    'timestamp': datetime.now()
                })
                
                context = create_context_from_files() if attach_context else ""
                with st.spinner("🤖 AI is thinking..."):
                    response = get_ai_response(starter, context)
                
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now()
                })
                st.rerun()

# Tab 3: Prompt Library
with tab3:
    st.markdown("## 📚 Prompt Engineering Library")
    
    st.markdown("""
    <div class="ai-insight">
        <h4>🎯 Master the Art of Prompting</h4>
        <p>Use these professionally crafted prompt templates to get better results from AI tools. 
        Each template is designed for specific tasks in your internship.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Category selection
    categories = list(PROMPT_LIBRARY.keys())
    
    tab_prompts = st.tabs([cat.title() for cat in categories])
    
    for idx, category in enumerate(categories):
        with tab_prompts[idx]:
            st.markdown(f"### {category.title()} Prompts")
            
            prompts = PROMPT_LIBRARY[category]
            
            for prompt_key, prompt_data in prompts.items():
                with st.expander(f"{prompt_data['icon']} {prompt_data['name']}", expanded=False):
                    st.markdown(f"**Description:** {prompt_data['description']}")
                    st.markdown(f"**Best for:** {prompt_data['best_for']}")
                    
                    # Display template
                    st.markdown("**Prompt Template:**")
                    st.markdown(f'<div class="prompt-template">{prompt_data["template"]}</div>', 
                               unsafe_allow_html=True)
                    
                    # Variable inputs
                    st.markdown("**Customize Variables:**")
                    variable_values = {}
                    
                    cols = st.columns(len(prompt_data['variables']))
                    for i, var in enumerate(prompt_data['variables']):
                        with cols[i]:
                            variable_values[var] = st.text_input(
                                var.replace('_', ' ').title(),
                                key=f"{category}_{prompt_key}_{var}",
                                placeholder=f"Enter {var}"
                            )
                    
                    # Generate customized prompt
                    if st.button(f"✨ Generate Prompt", key=f"gen_{category}_{prompt_key}"):
                        try:
                            customized = prompt_data['template'].format(**variable_values)
                            
                            st.markdown("**📋 Your Customized Prompt:**")
                            st.code(customized, language="text")
                            
                            # Option to use in chat
                            if st.button(f"💬 Use in AI Chat", key=f"use_{category}_{prompt_key}"):
                                st.session_state.selected_prompt_template = prompt_data['name']
                                st.session_state.messages.append({
                                    'role': 'user',
                                    'content': customized,
                                    'timestamp': datetime.now()
                                })
                                
                                context = create_context_from_files()
                                with st.spinner("🤖 Processing..."):
                                    response = get_ai_response(customized, context)
                                
                                st.session_state.messages.append({
                                    'role': 'assistant',
                                    'content': response,
                                    'timestamp': datetime.now()
                                })
                                
                                st.success("✅ Prompt sent to AI Assistant! Check the AI Assistant tab.")
                        
                        except KeyError as e:
                            st.error(f"⚠️ Please fill in all variables: {e}")
                    
                    # Copy to clipboard
                    st.markdown("---")
                    st.caption("💡 Tip: Copy this template and modify it for your specific needs!")

# Tab 4: Deliverables
with tab4:
    st.markdown("## 🎯 Deliverables Tracker")
    
    # Overview metrics
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    total_deliverables = sum(len(week['deliverables']) for week in WEEKLY_CURRICULUM.values())
    completed_deliverables = sum(1 for task_id, status in st.session_state.tasks_status.items() 
                                 if status == 'completed' and 'deliverable' in task_id)
    
    with metric_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{total_deliverables}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Total</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{completed_deliverables}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Completed</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_col3:
        pending = total_deliverables - completed_deliverables
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{pending}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Pending</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_col4:
        completion_rate = (completed_deliverables / total_deliverables * 100) if total_deliverables > 0 else 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{completion_rate:.0f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Complete</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Deliverables by week
    for week_num, week_data in WEEKLY_CURRICULUM.items():
        with st.expander(f"{week_data['icon']} Week {week_num}: {week_data['title']}", 
                        expanded=(week_num == st.session_state.current_week)):
            
            st.markdown(f"**📦 Deliverables ({len(week_data['deliverables'])}):**")
            
            for deliverable in week_data['deliverables']:
                st.markdown(f'<div class="deliverable-preview">', unsafe_allow_html=True)
                
                del_col1, del_col2, del_col3 = st.columns([3, 1, 1])
                
                with del_col1:
                    st.markdown(f"**📄 {deliverable}**")
                
                with del_col2:
                    # Check if related task is completed
                    related_task = next((t for t in week_data['tasks'] 
                                       if t['type'] == 'deliverable'), None)
                    if related_task:
                        status = st.session_state.tasks_status.get(related_task['id'], 'not_started')
                        status_class = f"status-{status.replace('_', '-')}"
                        st.markdown(f'<span class="status-badge {status_class}">{status.replace("_", " ").title()}</span>', 
                                   unsafe_allow_html=True)
                
                with del_col3:
                    if st.button("📤 Submit", key=f"submit_{week_num}_{deliverable}"):
                        st.session_state.deliverable_status[deliverable] = 'submitted'
                        st.success("✅ Submitted!")
                
                # Upload area
                uploaded_deliverable = st.file_uploader(
                    f"Upload {deliverable}",
                    key=f"upload_{week_num}_{deliverable}",
                    help="Upload your completed deliverable"
                )
                
                if uploaded_deliverable:
                    st.success(f"✅ {uploaded_deliverable.name} uploaded!")
                    if st.button("🔍 AI Review", key=f"review_{week_num}_{deliverable}"):
                        st.info("🤖 AI is reviewing your deliverable...")
                        st.markdown("""
                        **AI Feedback:**
                        - ✅ Document structure is clear and well-organized
                        - ✅ Content addresses all key requirements
                        - 💡 Consider adding more specific examples
                        - 💡 Expand on the implementation timeline
                        
                        **Overall Score: 85/100** - Excellent work!
                        """)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Week deliverable checklist
            st.markdown("**✓ Checklist:**")
            for task in week_data['tasks']:
                if task['type'] == 'deliverable':
                    status = st.session_state.tasks_status.get(task['id'], 'not_started')
                    checkbox_val = status == 'completed'
                    
                    if st.checkbox(f"{task['icon']} {task['title']}", 
                                  value=checkbox_val, 
                                  key=f"check_{task['id']}"):
                        st.session_state.tasks_status[task['id']] = 'completed'
                    else:
                        if task['id'] in st.session_state.tasks_status:
                            st.session_state.tasks_status[task['id']] = 'in_progress'

# Tab 5: Progress & Analytics
with tab5:
    st.markdown("## 📈 Progress & Analytics")
    
    # Overall progress
    st.markdown("### 🎯 Overall Progress")
    
    overall_col1, overall_col2 = st.columns([2, 1])
    
    with overall_col1:
        # Calculate overall progress
        total_tasks = sum(len(week['tasks']) for week in WEEKLY_CURRICULUM.values())
        completed = sum(1 for status in st.session_state.tasks_status.values() if status == 'completed')
        in_progress = sum(1 for status in st.session_state.tasks_status.values() if status == 'in_progress')
        not_started = total_tasks - completed - in_progress
        
        # Progress bar
        overall_progress = (completed / total_tasks * 100) if total_tasks > 0 else 0
        st.progress(overall_progress / 100)
        st.markdown(f"**{overall_progress:.1f}% Complete** ({completed}/{total_tasks} tasks)")
        
        # Task breakdown
        st.markdown("**Task Status Breakdown:**")
        status_col1, status_col2, status_col3 = st.columns(3)
        
        with status_col1:
            st.metric("✅ Completed", completed)
        with status_col2:
            st.metric("🔵 In Progress", in_progress)
        with status_col3:
            st.metric("⚪ Not Started", not_started)
    
    with overall_col2:
        st.markdown("**🏆 Achievements**")
        
        achievements = []
        if completed >= 1:
            achievements.append("🎯 First Task Complete")
        if completed >= 5:
            achievements.append("⚡ 5 Tasks Milestone")
        if completed >= 10:
            achievements.append("🌟 10 Tasks Milestone")
        if week_progress >= 100:
            achievements.append("📅 Week Complete")
        if len(st.session_state.messages) >= 10:
            achievements.append("💬 Active Learner")
        
        for achievement in achievements:
            st.markdown(f"- {achievement}")
        
        if not achievements:
            st.info("Complete tasks to unlock achievements!")
    
    st.divider()
    
    # Weekly progress breakdown
    st.markdown("### 📅 Weekly Progress")
    
    for week_num in range(1, 5):
        week = WEEKLY_CURRICULUM[week_num]
        week_prog = calculate_week_progress(week_num)
        
        week_col1, week_col2 = st.columns([3, 1])
        
        with week_col1:
            st.markdown(f"**{week['icon']} Week {week_num}: {week['title']}**")
            st.progress(week_prog / 100)
        
        with week_col2:
            st.metric("Progress", f"{week_prog:.0f}%")
    
    st.divider()
    
    # Activity timeline
    st.markdown("### ⏱️ Activity Timeline")
    
    if st.session_state.messages:
        recent_activity = st.session_state.messages[-10:]
        
        for activity in reversed(recent_activity):
            timestamp = activity.get('timestamp', datetime.now())
            role = activity['role']
            
            if role == 'user':
                icon = "👤"
                action = "Asked"
            else:
                icon = "🤖"
                action = "Responded"
            
            st.markdown(f"""
            <div class="workflow-step">
                {icon} <strong>{action}</strong> - {timestamp.strftime("%I:%M %p, %b %d")}
                <br><small>{activity['content'][:100]}...</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Your activity timeline will appear here as you interact with the platform.")
    
    st.divider()
    
    # Skill development
    st.markdown("### 🎓 Skill Development")
    
    skills = {
        'Prompt Engineering': 65,
        'Research & Analysis': 45,
        'Technical Writing': 55,
        'Tool Evaluation': 40,
        'Critical Thinking': 60,
        'Communication': 50
    }
    
    for skill, level in skills.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{skill}**")
            st.progress(level / 100)
        with col2:
            st.caption(f"{level}%")

# Tab 6: Skills & Learning
with tab6:
    st.markdown("## 🎓 Skills & Learning Resources")
    
    # Learning path
    st.markdown("### 🛣️ Your Learning Path")
    
    learning_stages = [
        {
            'stage': 'Foundation',
            'week': 1,
            'skills': ['Prompt Basics', 'Tool Discovery', 'Research Methods'],
            'status': 'completed' if calculate_week_progress(1) == 100 else 'in_progress'
        },
        {
            'stage': 'Analysis',
            'week': 2,
            'skills': ['Comparative Analysis', 'Documentation', 'Feature Mapping'],
            'status': 'completed' if calculate_week_progress(2) == 100 else 
                     ('in_progress' if st.session_state.current_week >= 2 else 'locked')
        },
        {
            'stage': 'Application',
            'week': 3,
            'skills': ['Use Case Development', 'Integration Planning', 'Recommendations'],
            'status': 'completed' if calculate_week_progress(3) == 100 else 
                     ('in_progress' if st.session_state.current_week >= 3 else 'locked')
        },
        {
            'stage': 'Synthesis',
            'week': 4,
            'skills': ['Report Writing', 'Presentation Design', 'Stakeholder Communication'],
            'status': 'completed' if calculate_week_progress(4) == 100 else 
                     ('in_progress' if st.session_state.current_week >= 4 else 'locked')
        }
    ]
    
    for stage_data in learning_stages:
        status_icon = {'completed': '✅', 'in_progress': '🔵', 'locked': '🔒'}[stage_data['status']]
        
        with st.expander(f"{status_icon} {stage_data['stage']} - Week {stage_data['week']}", 
                        expanded=(stage_data['status'] == 'in_progress')):
            
            st.markdown("**Skills to Develop:**")
            for skill in stage_data['skills']:
                skill_status = st.session_state.skill_assessments.get(skill, 0)
                st.markdown(f"- {skill} ({skill_status}%)")
                st.progress(skill_status / 100)
    
    st.divider()
    
    # Resources library
    st.markdown("### 📚 Resource Library")
    
    resource_categories = {
        'Guides & Tutorials': [
            {'title': 'Complete Prompt Engineering Guide', 'type': 'Guide', 'icon': '📖'},
            {'title': 'AI Tools Comparison Framework', 'type': 'Template', 'icon': '📊'},
            {'title': 'Research Methodology 101', 'type': 'Tutorial', 'icon': '🎓'}
        ],
        'Templates': [
            {'title': 'Research Plan Template', 'type': 'Document', 'icon': '📝'},
            {'title': 'Comparative Analysis Template', 'type': 'Document', 'icon': '⚖️'},
            {'title': 'Presentation Template', 'type': 'Slides', 'icon': '🎨'}
        ],
        'Examples': [
            {'title': 'Sample Research Report', 'type': 'Example', 'icon': '📄'},
            {'title': 'Best Practice Prompts', 'type': 'Collection', 'icon': '✨'},
            {'title': 'Use Case Library', 'type': 'Examples', 'icon': '💡'}
        ]
    }
    
    for category, resources in resource_categories.items():
        st.markdown(f"**{category}**")
        
        resource_cols = st.columns(len(resources))
        for idx, resource in enumerate(resources):
            with resource_cols[idx]:
                st.markdown(f"""
                <div class="prompt-card">
                    <div style="font-size: 2rem; text-align: center;">{resource['icon']}</div>
                    <div style="font-weight: 600; margin-top: 0.5rem;">{resource['title']}</div>
                    <div style="font-size: 0.8rem; color: #666;">{resource['type']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("📥 Access", key=f"resource_{category}_{idx}", use_container_width=True):
                    st.info(f"Opening {resource['title']}...")
    
    st.divider()
    
    # Learning tips
    st.markdown("### 💡 Learning Tips & Best Practices")
    
    tips = [
        {
            'title': 'Effective Prompt Engineering',
            'tips': [
                'Be specific and clear in your instructions',
                'Provide examples to guide the AI',
                'Iterate and refine your prompts',
                'Use context to improve responses'
            ],
            'icon': '🎯'
        },
        {
            'title': 'Research Best Practices',
            'tips': [
                'Start with official documentation',
                'Compare multiple sources',
                'Document your findings systematically',
                'Focus on verifiable facts'
            ],
            'icon': '🔬'
        },
        {
            'title': 'Deliverable Quality',
            'tips': [
                'Start with a clear outline',
                'Use consistent formatting',
                'Cite sources properly',
                'Proofread before submission'
            ],
            'icon': '📝'
        }
    ]
    
    tip_cols = st.columns(len(tips))
    for idx, tip_section in enumerate(tips):
        with tip_cols[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                       padding: 1.5rem; border-radius: 15px; height: 100%;">
                <div style="font-size: 2rem; text-align: center;">{tip_section['icon']}</div>
                <h4 style="text-align: center; margin: 1rem 0;">{tip_section['title']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for tip in tip_section['tips']:
                st.markdown(f"✓ {tip}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>🎓 <strong>EXCELERATE AI Internship Platform</strong></p>
    <p>Powered by AI • Built for Learning • Designed for Success</p>
    <p style="font-size: 0.8rem;">Week {week} of 4 • {completed_tasks}/{total_tasks} Tasks Complete</p>
</div>
""".format(
    week=st.session_state.current_week,
    completed_tasks=sum(1 for s in st.session_state.tasks_status.values() if s == 'completed'),
    total_tasks=sum(len(w['tasks']) for w in WEEKLY_CURRICULUM.values())
), unsafe_allow_html=True)