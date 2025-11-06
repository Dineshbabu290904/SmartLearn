import streamlit as st
import os
from datetime import datetime
import json
import PyPDF2
import docx
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="AI Internship Task Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
        transition: all 0.3s;
    }
    .task-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-not-started {
        background-color: #ffc107;
        color: #000;
    }
    .status-in-progress {
        background-color: #17a2b8;
        color: #fff;
    }
    .status-completed {
        background-color: #28a745;
        color: #fff;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: 2rem;
    }
    .system-message {
        background-color: #fff3cd;
        text-align: center;
        font-style: italic;
    }
    .uploaded-file {
        background-color: #e8f5e9;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_files_content' not in st.session_state:
    st.session_state.uploaded_files_content = []
if 'current_task' not in st.session_state:
    st.session_state.current_task = None
if 'learning_mode' not in st.session_state:
    st.session_state.learning_mode = 'guided'
if 'tasks_status' not in st.session_state:
    st.session_state.tasks_status = {}

# Task Database
TASKS = [
    {
        'id': 1,
        'title': 'Python Basics: Variables and Data Types',
        'difficulty': 'Beginner',
        'description': 'Learn about Python variables, data types, and basic operations',
        'subtasks': [
            'Declare and use variables',
            'Work with strings and string methods',
            'Use numbers (int, float) and operations',
            'Practice type conversion'
        ],
        'learning_objectives': [
            'Understand variable assignment',
            'Master different data types',
            'Perform type conversions',
            'Apply basic operations'
        ]
    },
    {
        'id': 2,
        'title': 'Control Flow: Loops and Conditions',
        'difficulty': 'Beginner',
        'description': 'Master if-else statements, for loops, and while loops',
        'subtasks': [
            'Write if-else conditions',
            'Use for loops for iteration',
            'Implement while loops',
            'Apply break and continue statements'
        ],
        'learning_objectives': [
            'Make decisions with conditionals',
            'Iterate with for loops',
            'Control loop execution',
            'Handle edge cases'
        ]
    },
    {
        'id': 3,
        'title': 'Functions and Modules',
        'difficulty': 'Intermediate',
        'description': 'Create reusable functions and work with modules',
        'subtasks': [
            'Define and call functions',
            'Use parameters and return values',
            'Import and use modules',
            'Create your own module'
        ],
        'learning_objectives': [
            'Write modular code',
            'Understand scope',
            'Use built-in modules',
            'Create reusable components'
        ]
    },
    {
        'id': 4,
        'title': 'Data Structures: Lists and Dictionaries',
        'difficulty': 'Intermediate',
        'description': 'Work with Python lists, dictionaries, sets, and tuples',
        'subtasks': [
            'Perform list operations',
            'Use dictionary methods',
            'Work with sets and tuples',
            'Handle nested structures'
        ],
        'learning_objectives': [
            'Choose appropriate data structures',
            'Manipulate collections efficiently',
            'Understand mutability',
            'Work with complex data'
        ]
    },
    {
        'id': 5,
        'title': 'File Handling and I/O',
        'difficulty': 'Intermediate',
        'description': 'Read from and write to files, handle exceptions',
        'subtasks': [
            'Read text files',
            'Write to files',
            'Handle CSV and JSON',
            'Implement error handling'
        ],
        'learning_objectives': [
            'Perform file operations',
            'Parse different formats',
            'Handle exceptions gracefully',
            'Ensure data persistence'
        ]
    }
]

# System Prompts for different modes
SYSTEM_PROMPTS = {
    'guided': """You are an expert programming tutor for an internship task portal. Your role is to:

1. GUIDED LEARNING APPROACH:
   - Break down complex topics into digestible steps
   - Ask clarifying questions to assess understanding
   - Provide hints before giving full solutions
   - Encourage active learning and problem-solving
   - Use the Socratic method to guide discovery

2. STEP-BY-STEP INSTRUCTION:
   - Start with conceptual explanation
   - Show simple examples first
   - Build complexity gradually
   - Provide practice exercises
   - Verify understanding at each step

3. DOCUMENT ANALYSIS (RAG):
   - When documents are provided, analyze them thoroughly
   - Extract key concepts and exercises
   - Reference specific sections when explaining
   - Help users navigate through the material
   - Connect document content to practical tasks

4. INTERACTIVE FEEDBACK:
   - Review user's code attempts
   - Provide constructive feedback
   - Highlight what's correct before corrections
   - Suggest improvements incrementally
   - Celebrate progress and milestones

5. RESPONSE STYLE:
   - Be encouraging and supportive
   - Use clear, beginner-friendly language
   - Include code examples with explanations
   - Ask "Do you understand?" or "Would you like to try?" frequently
   - Adapt pace based on user responses

Remember: Your goal is to help interns LEARN, not just complete tasks. Guide them to discover solutions themselves.""",

    'direct': """You are an efficient AI assistant for an internship task portal. Your role is to:

1. DIRECT ASSISTANCE:
   - Provide clear, concise solutions
   - Show complete working code examples
   - Explain the reasoning briefly
   - Answer questions directly

2. DOCUMENT PROCESSING (RAG):
   - Extract relevant information from uploaded documents
   - Summarize key points
   - Answer specific questions about the content
   - Reference document sections accurately

3. TASK COMPLETION:
   - Help complete tasks efficiently
   - Provide best practices
   - Offer optimized solutions
   - Debug code issues quickly

4. RESPONSE STYLE:
   - Be clear and professional
   - Use proper code formatting
   - Include brief explanations
   - Provide complete examples

Focus on efficiency while ensuring understanding."""
}

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
        'content': ''
    }
    
    try:
        if file_type == 'application/pdf':
            content['content'] = extract_text_from_pdf(uploaded_file)
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            content['content'] = extract_text_from_docx(uploaded_file)
        elif file_type == 'text/plain':
            content['content'] = uploaded_file.read().decode('utf-8')
        elif file_type.startswith('image/'):
            # For images, we'll store the image data
            image = Image.open(uploaded_file)
            content['image'] = image
            content['content'] = f"[Image: {file_name}]"
        else:
            content['content'] = f"[Unsupported file type: {file_type}]"
    except Exception as e:
        content['content'] = f"[Error processing file: {str(e)}]"
    
    return content

def create_context_from_files():
    """Create context from uploaded files for RAG"""
    if not st.session_state.uploaded_files_content:
        return ""
    
    context = "\n\n=== UPLOADED DOCUMENTS CONTENT ===\n\n"
    for file_content in st.session_state.uploaded_files_content:
        context += f"--- {file_content['name']} ---\n"
        context += file_content['content'][:5000]  # Limit content length
        context += "\n\n"
    
    return context

def get_ai_response(user_message, context=""):
    """Get AI response using Groq API with RAG context"""
    try:
        from groq import Groq
        
        # Get API key from sidebar or session state
        api_key = st.session_state.get('groq_api_key', '')
        
        if not api_key:
            return "⚠️ Please enter your Groq API key in the sidebar to use AI features."
        
        client = Groq(api_key=api_key)
        
        # Prepare system prompt based on mode
        system_prompt = SYSTEM_PROMPTS[st.session_state.learning_mode]
        
        # Add current task context if available
        if st.session_state.current_task:
            task = next(t for t in TASKS if t['id'] == st.session_state.current_task)
            system_prompt += f"\n\nCURRENT TASK: {task['title']}\n"
            system_prompt += f"Description: {task['description']}\n"
            system_prompt += f"Subtasks: {', '.join(task['subtasks'])}\n"
        
        # Add document context for RAG
        if context:
            system_prompt += f"\n\n{context}"
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history (last 5 messages for context)
        for msg in st.session_state.messages[-5:]:
            if msg['role'] != 'system':
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="openai/gpt-oss-120b",  # or "llama2-70b-4096"
            temperature=0.7,
            max_tokens=2048,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ Error getting AI response: {str(e)}\n\nMake sure you have installed the Groq library: pip install groq"

# Main App Layout
st.markdown('<h1 class="main-header">🎓 AI-Powered Internship Task Portal</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key Input
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.get('groq_api_key', ''),
        help="Enter your Groq API key. Get one at https://console.groq.com"
    )
    if groq_api_key:
        st.session_state.groq_api_key = groq_api_key
    
    st.divider()
    
    # Learning Mode Selection
    st.subheader("🧠 Learning Mode")
    learning_mode = st.radio(
        "Choose your learning approach:",
        options=['guided', 'direct'],
        format_func=lambda x: "🎯 Guided Learning (Step-by-step)" if x == 'guided' else "⚡ Direct Assistance (Quick help)",
        index=0 if st.session_state.learning_mode == 'guided' else 1
    )
    st.session_state.learning_mode = learning_mode
    
    if learning_mode == 'guided':
        st.info("📚 AI will guide you through learning step-by-step, asking questions and providing hints.")
    else:
        st.info("⚡ AI will provide direct solutions and quick assistance.")
    
    st.divider()
    
    # File Upload Section
    st.subheader("📁 Upload Learning Resources")
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, DOCX, TXT, Images)",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg']
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Check if file is already processed
            if not any(f['name'] == uploaded_file.name for f in st.session_state.uploaded_files_content):
                with st.spinner(f'Processing {uploaded_file.name}...'):
                    content = process_uploaded_file(uploaded_file)
                    st.session_state.uploaded_files_content.append(content)
                    st.success(f"✅ {uploaded_file.name} processed!")
    
    # Display uploaded files
    if st.session_state.uploaded_files_content:
        st.subheader("📎 Uploaded Files")
        for idx, file_content in enumerate(st.session_state.uploaded_files_content):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="uploaded-file">📄 {file_content["name"]}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.uploaded_files_content.pop(idx)
                    st.rerun()
    
    st.divider()
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("📊 View Progress"):
        st.session_state.show_progress = True

# Main Content Area
tab1, tab2, tab3 = st.tabs(["📋 Tasks", "💬 AI Assistant", "📈 Progress"])

# Tab 1: Tasks
with tab1:
    st.header("Available Internship Tasks")
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search tasks", placeholder="Search by title or description...")
    with col2:
        difficulty_filter = st.selectbox("Filter by difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
    
    # Display tasks
    for task in TASKS:
        # Apply filters
        if difficulty_filter != "All" and task['difficulty'] != difficulty_filter:
            continue
        if search_query and search_query.lower() not in task['title'].lower() and search_query.lower() not in task['description'].lower():
            continue
        
        # Get task status
        status = st.session_state.tasks_status.get(task['id'], 'not_started')
        
        with st.container():
            st.markdown('<div class="task-card">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.subheader(task['title'])
                st.write(task['description'])
            
            with col2:
                difficulty_color = {
                    'Beginner': '🟢',
                    'Intermediate': '🟡',
                    'Advanced': '🔴'
                }
                st.write(f"{difficulty_color.get(task['difficulty'], '⚪')} {task['difficulty']}")
            
            with col3:
                status_class = f"status-{status.replace('_', '-')}"
                status_text = status.replace('_', ' ').title()
                st.markdown(f'<span class="status-badge {status_class}">{status_text}</span>', unsafe_allow_html=True)
            
            # Expandable details
            with st.expander("📖 View Details"):
                st.write("**Subtasks:**")
                for subtask in task['subtasks']:
                    st.write(f"• {subtask}")
                
                st.write("\n**Learning Objectives:**")
                for objective in task['learning_objectives']:
                    st.write(f"✓ {objective}")
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("🎯 Start Learning", key=f"start_{task['id']}"):
                    st.session_state.current_task = task['id']
                    st.session_state.tasks_status[task['id']] = 'in_progress'
                    
                    # Add initial message
                    initial_message = f"""🎯 Great! Let's start working on: **{task['title']}**

**Description:** {task['description']}

**Subtasks to complete:**
{chr(10).join(f"{i+1}. {subtask}" for i, subtask in enumerate(task['subtasks']))}

{"🎓 I'll guide you through each step with explanations and practice exercises." if st.session_state.learning_mode == 'guided' else '⚡ I can help you complete this task efficiently. What would you like to work on?'}

Which subtask would you like to start with, or do you have any questions?"""
                    
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': initial_message,
                        'timestamp': datetime.now()
                    })
                    st.rerun()
            
            with col2:
                if st.button("✅ Mark Complete", key=f"complete_{task['id']}"):
                    st.session_state.tasks_status[task['id']] = 'completed'
                    st.success(f"🎉 Congratulations! Task '{task['title']}' completed!")
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: AI Assistant
with tab2:
    st.header("💬 AI Learning Assistant")
    
    # Display current task
    if st.session_state.current_task:
        current_task = next(t for t in TASKS if t['id'] == st.session_state.current_task)
        st.info(f"📌 **Current Task:** {current_task['title']}")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display messages
        for message in st.session_state.messages:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message">👤 <strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            elif message['role'] == 'assistant':
                st.markdown(f'<div class="chat-message assistant-message">🤖 <strong>AI Assistant:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message system-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Input area
    st.divider()
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your message...",
            height=100,
            placeholder="Ask a question, request help with code, or share your solution for feedback..."
        )
    
    with col2:
        st.write("")
        st.write("")
        send_button = st.button("📤 Send", use_container_width=True)
    
    # Quick prompts
    st.write("**Quick Prompts:**")
    quick_prompts_col = st.columns(4)
    
    quick_prompts = [
        "Explain this concept",
        "Show me an example",
        "Check my code",
        "Give me a hint"
    ]
    
    for idx, prompt in enumerate(quick_prompts):
        with quick_prompts_col[idx]:
            if st.button(prompt, key=f"quick_{idx}"):
                user_input = prompt
                send_button = True
    
    # Handle send
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Create context from uploaded files
        context = create_context_from_files()
        
        # Get AI response
        with st.spinner("🤔 AI is thinking..."):
            ai_response = get_ai_response(user_input, context)
        
        # Add AI response
        st.session_state.messages.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now()
        })
        
        st.rerun()

# Tab 3: Progress
with tab3:
    st.header("📈 Learning Progress")
    
    # Calculate statistics
    total_tasks = len(TASKS)
    completed_tasks = sum(1 for status in st.session_state.tasks_status.values() if status == 'completed')
    in_progress_tasks = sum(1 for status in st.session_state.tasks_status.values() if status == 'in_progress')
    not_started_tasks = total_tasks - completed_tasks - in_progress_tasks
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total Tasks", total_tasks)
    with col2:
        st.metric("✅ Completed", completed_tasks)
    with col3:
        st.metric("🔄 In Progress", in_progress_tasks)
    with col4:
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("📊 Completion Rate", f"{completion_rate:.1f}%")
    
    # Progress bar
    st.progress(completion_rate / 100)
    
    st.divider()
    
    # Task breakdown
    st.subheader("Task Status Breakdown")
    
    for task in TASKS:
        status = st.session_state.tasks_status.get(task['id'], 'not_started')
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write(f"**{task['title']}**")
        
        with col2:
            status_emoji = {
                'not_started': '⚪',
                'in_progress': '🔵',
                'completed': '✅'
            }
            st.write(f"{status_emoji.get(status, '⚪')} {status.replace('_', ' ').title()}")
    
    st.divider()
    
    # Learning insights
    st.subheader("💡 Learning Insights")
    
    if completed_tasks > 0:
        st.success(f"🎉 Great progress! You've completed {completed_tasks} task{'s' if completed_tasks > 1 else ''}!")
    
    if in_progress_tasks > 0:
        st.info(f"🔄 You have {in_progress_tasks} task{'s' if in_progress_tasks > 1 else ''} in progress. Keep going!")
    
    if not_started_tasks > 0:
        st.warning(f"📋 {not_started_tasks} task{'s' if not_started_tasks > 1 else ''} waiting to be started.")
    
    # Conversation statistics
    if st.session_state.messages:
        st.divider()
        st.subheader("💬 Chat Statistics")
        
        user_messages = sum(1 for msg in st.session_state.messages if msg['role'] == 'user')
        ai_messages = sum(1 for msg in st.session_state.messages if msg['role'] == 'assistant')
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Messages", user_messages)
        with col2:
            st.metric("AI Responses", ai_messages)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🎓 AI-Powered Internship Task Portal | Built with Streamlit & Groq API</p>
    <p style='font-size: 0.9rem;'>Features: RAG Document Processing • Guided Learning • Step-by-Step Assistance • Progress Tracking</p>
</div>
""", unsafe_allow_html=True)