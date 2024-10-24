import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Luna's Portfolio", layout="centered", page_icon=":star:")

@st.dialog("Contact Me")
def show_contact_form():
    st.write("Feel free to reach out to me through the following channels:")
    st.markdown("📧 Email: [luna.vayer@efrei.net](mailto:luna.vayer@efrei.net)")
    st.markdown("🔗 LinkedIn: [![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/luna-vayer)")


st.title("🌟 My Portfolio 🌟")

# About Me Section
st.header("About Me")
st.write("""
I am an aspiring professional with a growing expertise in Data Science, programming, and digital technologies.
I am currently pursuing an engineering degree in Computer Science and Digital Technologies at Efrei Paris, and I am passionate about implementing innovative solutions in the data field. I am looking for opportunities to apply my skills in a practical environment.
""")

if st.button("💬 Contact Me"):
    show_contact_form()


# Education Section
st.header("Education")
st.write("""
- **Efrei Paris**: Engineering in Computer Science and Digital Technologies  
**Specialization**: Digital Biology  
**Expected Graduation**: 2026
""")


# Work Experience Section
st.header("Work Experience")
with st.expander("Click to see the details of my work experiences", expanded=False):
    st.write("""
    - **Sephora (2023)**: 4-week commercial internship focused on customer service, stock management, and in-store assistance.
    - **Bel Ulzama (2022)**: 4-week internship involving document digitization and updates related to factory operations.
    """)

# Skills Section
st.header("Skills")
st.write("""
- **Programming**: Python, SQL
- **Data Science**
- **Digital Documentation and Management**
- **Tools**: Microsoft Office, Photoshop
""")


# Achievements Section
st.header("Achievements")
st.write("Here are some of my notable achievements:")
st.write("""
- **FarmN’Go (2023-2024)**: Developed a reservation application and a showcase website using Figma.
- **SQL Database Creation (2022-2023)**
- **Python 2D Game Development Project (2021-2022)**
""")


# Adding a timeline with the projects
st.subheader("Timeline of My Work")

iframe_code = """
<iframe src="https://cdn.knightlab.com/libs/timeline3/latest/embed/index.html?source=1UZOX-0n40RfiH3chPslMqjFh8hYeIdorP9TTJIRqNbs&font=Default&lang=en&initial_zoom=2&height=650" width="100%" height="650" webkitallowfullscreen mozallowfullscreen allowfullscreen frameborder="0"></iframe>
"""

components.html(iframe_code, height=600)                                


# Contact Section
st.header("Contact")
st.write("If you wish to get in touch with me, here are my contact details:")
st.markdown('''
- **LinkedIn**: [![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/luna-vayer)
- **Location**: Villejuif, France
''')


# CV Download Button
cv_file = "Luna Vayer - CV.pdf"
with open(cv_file, "rb") as f:
    st.download_button("Download My CV 📄", f, file_name="luna_cv.pdf")


# Strengths and Advantages Section
st.header("Strengths and Advantages")
st.write("""
I have strong analytical skills, excellent teamwork, and a great passion for learning new technologies. With a strong problem-solving mindset and autonomy, I am ready to take on challenges and deliver high-quality results.
""")

# Interests and Hobbies Section
st.header("Interests and Hobbies")
st.write("""
Outside of my studies, I have been involved in equestrian sports for nine years and actively contribute to my riding club. I also have a strong interest in technology and continue to explore new areas in digital innovation.
""")

# Availability Section
st.header("Availability")
st.write("I have secured a 20-week technical internship starting in November 2024.")


# References Section
st.header("References")
st.write("References are available upon request.")


st.markdown("""
<style>
    .stApp {
        padding: 10px;
        border-radius: 10px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #3c3326;
    }
    .stButton>button{
        background-color: #649B88;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stDownloadButton > button {
        background-color: #649B88;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stDownloadButton > button:hover {
        background-color: #83a697;
        color: white;
    }
    .stButton>button:hover {
        background-color: #83a697;
        color: white;
    }

    .st-emotion-cache-6qob1r { /* Sidebar background color */
        background-color: #649B88;
    }
    .st-emotion-cache-1rtdyuf{ /* Sidebar text portfolio color */
        color: white;
    }
    .st-emotion-cache-6tkfeg{
        color: white;
    }

            
    .st-emotion-cache-1f3w014{ /* Sidebar arrow color */
        color: black;
    }
                
    }
    .stExpander p {
        color: black;
    }
    .stExpander:hover p {
        color: #649B88; /* Change the text color of <p> inside expander on hover */
    }
    
    .stExpander:hover summary svg path:nth-of-type(2) {
        fill: #649B88; /* Change the color of the arrow on hover */
    }

</style>
""", unsafe_allow_html=True)

components.html("""
    <style>
    /* Custom style for vis.js items */
    .vis-item {
        background-color: #649B88 !important;
        border-color: #ff6666 !important;
        color: #649B88 !important;
    }
    </style>
    """, height=0)
