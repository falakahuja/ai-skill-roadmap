import streamlit as st
from roadmap_generator import generate_roadmap
import re

# Page config
st.set_page_config(page_title="AI Skill Learning Roadmap", layout="wide")
st.title("🚀 AI-Powered Skill Development Roadmap")

# Inputs
role = st.text_input("Enter Skill Role (e.g., Frontend Developer, Backend Developer)")
experience = st.selectbox("Select Experience Level", ["Beginner", "Intermediate", "Advanced"])
weeks = st.slider("📅 Select Number of Weeks to Complete Roadmap", min_value=2, max_value=24, value=9)

if st.button("Generate Skill Roadmap"):
    if not role:
        st.warning("Please enter a skill role.")
    else:
        with st.spinner("Generating personalized roadmap..."):
            roadmap = generate_roadmap(role, experience, weeks)

        st.subheader(f"🗺️ {weeks}-Week Roadmap for {experience} {role}")

        try:
            # Split roadmap into week-wise blocks using regex
            week_blocks = re.split(r'(Week \d+:.*?)\n', roadmap, flags=re.IGNORECASE)

            for i in range(1, len(week_blocks), 2):
                week_title = week_blocks[i].strip()
                content = week_blocks[i + 1].strip()

                with st.expander(f"📅 {week_title}", expanded=True):
                    st.markdown(f"#### 📌 **{week_title}**")

                    # Split by sections: Tools, Concepts, Tasks, Project, Resources
                    sections = re.split(
                        r'(Tools/Technologies:|Concepts to Master:|Task \d+:|Project Idea \(Milestone\):|Optional Resources:)',
                        content
                    )

                    section_title = ''
                    for sec in sections:
                        sec = sec.strip()

                        if sec.endswith(":") or "Task" in sec:
                            section_title = sec
                        elif section_title:
                            # Display title and content nicely
                            st.markdown(f"**{section_title}**")
                            # Clean up extra asterisks
                            cleaned_text = re.sub(r'\*+', '', sec)
                            st.markdown(cleaned_text)
                            section_title = ''
        except Exception as e:
            st.error(f"⚠️ Error displaying roadmap: {e}")
