import streamlit as st
import os
import subprocess
import tempfile
from io import BytesIO

# Function to generate PDF from LaTeX code
def generate_pdf(latex_code):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Path for LaTeX file
        latex_file_path = os.path.join(tmpdirname, 'document.tex')

        # Write LaTeX code to file
        with open(latex_file_path, 'w') as f:
            f.write(latex_code)

        # Run pdflatex to generate the PDF
        try:
            subprocess.run(['pdflatex', latex_file_path], cwd=tmpdirname, check=True)
            
            # Read the generated PDF
            pdf_file_path = os.path.join(tmpdirname, 'document.pdf')
            with open(pdf_file_path, 'rb') as f:
                pdf_data = f.read()

            return pdf_data

        except subprocess.CalledProcessError:
            return None

# Streamlit app UI
def main():
    st.title("LaTeX to PDF Converter")
    st.write("Enter your LaTeX code below to convert it into a PDF.")
    
    # LaTeX code input
    latex_code = st.text_area("LaTeX Code", height=300)

    # Button to generate PDF
    if st.button("Generate PDF"):
        if latex_code:
            # Generate PDF from LaTeX code
            pdf_data = generate_pdf(latex_code)
            
            if pdf_data:
                # Provide PDF download link
                st.success("PDF generated successfully!")
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name="document.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Error generating PDF from LaTeX code. Please check the syntax.")
        else:
            st.warning("Please enter some LaTeX code.")

if __name__ == "__main__":
    main()
