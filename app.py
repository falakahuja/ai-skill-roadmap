import streamlit as st
from roadmap_generator import generate_roadmap
from scraper.course_scraper import get_coursera_courses
from scraper.project_scraper import get_project_ideas
from scraper.resource_scraper import get_community_resources
from utils.helper import validate_input
import re

# Page configuration
st.set_page_config(
    page_title="AI Skill Roadmap Generator",
    layout="wide",
    page_icon="🧠"
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        width: 100%;
    }
    .roadmap-week {
        background-color: #1e1e2f;
        color: #f5f5f5;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #4F46E5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .resource-card {
        background-color: #2c2c3c;
        color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .section-title {
        color: #4F46E5 !important;
        border-bottom: 2px solid #4F46E5;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def display_roadmap(roadmap: str):
    """Display formatted roadmap with proper link rendering"""
    if not roadmap:
        st.warning("No roadmap content was generated")
        return

    # Split by weeks
    week_sections = re.split(r'(### Week \d+)', roadmap)
    
    for i in range(1 if week_sections[0].strip() == "" else 0, len(week_sections), 2):
        if i+1 >= len(week_sections):
            continue

        week_header = week_sections[i].replace("###", "").strip()
        week_content = week_sections[i+1].strip()

        # Extract topic if exists
        topic = re.search(r'\*\*Topic\*\*:\s*(.*)', week_content)
        topic_text = f" — {topic.group(1)}" if topic else ""
        
        # Clean content and convert markdown links to HTML
        clean_content = re.sub(r'\*\*Topic\*\*:\s*.*', '', week_content)
        clean_content = clean_content.strip()
        
        # Convert markdown links to HTML
        clean_content = re.sub(
            r'\[([^\]]+)\]\(([^)]+)\)',
            r'<a href="\2" target="_blank">\1</a>',
            clean_content
        )

        # Display week using markdown to render links properly
        with st.container():
            st.markdown(f"""
            <div class="roadmap-week">
                <h3>{week_header}{topic_text}</h3>
                <div style="margin-left: 1em;">
            """, unsafe_allow_html=True)
            
            # Use st.markdown to render content with proper link handling
            st.markdown(clean_content, unsafe_allow_html=True)
            
            st.markdown("""
                </div>
            </div>
            """, unsafe_allow_html=True)

# ... (keep all your existing imports and CSS code) ...

def main():
    st.title("🧠 AI Skill Roadmap Generator")
    st.markdown("Get a personalized learning path for any tech skill")

    with st.form("skill_form"):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Skill/Role (e.g., Python Developer, Data Analyst)")
        with col2:
            experience = st.selectbox(
                "Your Current Level",
                ["Beginner", "Intermediate", "Advanced"]
            )

        weeks = st.slider(
            "Timeline (weeks)",
            min_value=2,
            max_value=16,
            value=8,
            help="How long do you want your learning plan to be?"
        )

        submitted = st.form_submit_button("Generate Roadmap")

    if submitted:
        col_roadmap, col_resources = st.columns([2, 1])  # 66% roadmap, 33% resources
        
        roadmap = generate_roadmap(role, experience, weeks)

        with col_roadmap:
            st.markdown("<h2 class='section-title'>📅 Your Learning Path</h2>", unsafe_allow_html=True)
            display_roadmap(roadmap)

        with col_resources:
            st.markdown("<h2 class='section-title'>🛠️ Learning Resources</h2>", unsafe_allow_html=True)
            
            # Added container with padding for better spacing
            with st.container():
                with st.expander("🎓 Recommended Courses", expanded=True):
                    courses = get_coursera_courses(role)
                    for course in courses[:3]:
                        st.markdown(f"""
                        <div class="resource-card">
                            <b>{course['title']}</b><br>
                            <small>{course['platform']}</small><br>
                            <a href="{course['url']}" target="_blank">View Course</a>
                        </div>
                        """, unsafe_allow_html=True)

                with st.expander("💡 Project Ideas", expanded=True):
                    projects = get_project_ideas(role, experience)
                    for project in projects[:3]:
                        st.markdown(f"""
                        <div class="resource-card">
                            {project}
                        </div>
                        """, unsafe_allow_html=True)

                with st.expander("👥 Community Resources", expanded=True):
                    resources = get_community_resources(role)
                    for resource in resources[:3]:
                        st.markdown(f"""
                        <div class="resource-card">
                            <b>{resource['type']}:</b> {resource['name']}<br>
                            <a href="{resource['url']}" target="_blank">Visit</a>
                        </div>
                        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()