import io
import fitz  # PyMuPDF
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')

    if request.method == "POST":
        file = request.files.get("myFile")
        
        if not file or file.filename == '':
            return "Nincs fájl kiválasztva", 400

        try:
            input_pdf_bytes = file.read()
            doc = fitz.open(stream=input_pdf_bytes, filetype="pdf")
            
            blank_pages = []
            for page_num, page in enumerate(doc):
                if not page.get_text().strip() and not page.get_images():
                    blank_pages.append(page_num)

            for page_num in reversed(blank_pages):
                doc.delete_page(page_num)

            output_buffer = io.BytesIO()
            doc.save(output_buffer)
            doc.close()
            output_buffer.seek(0)

            return send_file(
                output_buffer,
                as_attachment=True,
                download_name=f"tiszta_{file.filename}",
                mimetype='application/pdf'
            )
        except Exception as e:
            return f"Error processing PDF: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)