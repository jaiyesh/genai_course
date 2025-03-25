import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Oil & Gas Knowledge Base",
    page_icon="⛽",
    layout="wide"
)

# Initialize OpenAI client
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_KEY)

# Create prompt template
prompt_template_petroleum = PromptTemplate(
    input_variables=["topic"],
    template="You are a Petroleum engineer. Can you tell me about {topic}?"
)

def generate_pdf(topic, content):
    # Create a BytesIO object to store the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for the 'Flowables' (elements) of the document
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Create custom heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12
    )
    
    # Create custom body style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leading=16
    )
    
    # Add title
    elements.append(Paragraph(f"Oil & Gas Knowledge Base Report", title_style))
    elements.append(Spacer(1, 20))
    
    # Add topic
    elements.append(Paragraph(f"Topic: {topic}", heading_style))
    elements.append(Spacer(1, 20))
    
    # Add content
    elements.append(Paragraph(content, body_style))
    
    # Add timestamp
    elements.append(Spacer(1, 30))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generated on: {timestamp}", body_style))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    return pdf

# Streamlit UI
st.title("⛽ Oil & Gas Knowledge Base")
st.write("Get detailed information about various topics in the oil and gas industry.")

# User input
topic = st.text_input("Enter a topic from the oil and gas industry:", 
                     placeholder="e.g., Hydraulic Fracturing, Reservoir Engineering, Well Logging")

if st.button("Generate Information"):
    if topic:
        with st.spinner("Generating information..."):
            # Format the prompt
            formatted_prompt = prompt_template_petroleum.format(topic=topic)
            
            # Generate response
            response = client.predict(formatted_prompt)
            
            # Display the response
            st.markdown("### Generated Information:")
            st.write(response)
            
            # Generate PDF
            pdf = generate_pdf(topic, response)
            
            # Create download button
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf,
                file_name=f"oil_gas_report_{topic.lower().replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Please enter a topic first!")

# Add some helpful information
with st.sidebar:
    st.header("About")
    st.write("""
    This application uses AI to generate detailed information about various topics in the oil and gas industry.
    Simply enter a topic and click 'Generate Information' to get started.
    You can also download the generated information as a PDF report.
    """)
    
    st.header("Example Topics")
    st.write("""
    - Hydraulic Fracturing
    - Reservoir Engineering
    - Well Logging
    - Enhanced Oil Recovery
    - Drilling Operations
    - Production Engineering
    - Petroleum Geology
    - Well Testing
    """) 