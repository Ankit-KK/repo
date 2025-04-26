from flask import Flask, request, send_file
import os
import subprocess
import tempfile

app = Flask(__name__)

@app.route('/convert_latex', methods=['POST'])
def convert_latex():
    # Get LaTeX code from the request
    latex_code = request.form.get('latex_code')

    if not latex_code:
        return "No LaTeX code provided", 400

    # Create a temporary directory to store the LaTeX file
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Path for the LaTeX file
        latex_file_path = os.path.join(tmpdirname, 'resume.tex')
        
        # Write the LaTeX code to the file
        with open(latex_file_path, 'w') as f:
            f.write(latex_code)

        # Run pdflatex to generate the PDF
        try:
            subprocess.run(['pdflatex', latex_file_path], cwd=tmpdirname, check=True)

            # Send the generated PDF back to the user
            pdf_path = os.path.join(tmpdirname, 'resume.pdf')
            return send_file(pdf_path, as_attachment=True)

        except subprocess.CalledProcessError:
            return "Error generating PDF from LaTeX", 500

if __name__ == '__main__':
    app.run(debug=True)
