from flask import Blueprint, request, jsonify, render_template, send_file
from fpdf import FPDF
import tempfile
import os

bp = Blueprint("main", __name__)

# Concrete strength classes and their characteristic strengths
CONCRETE_STRENGTHS = {
    'C12/15': 12, 'C16/20': 16, 'C20/25': 20, 'C25/30': 25,
    'C30/37': 30, 'C35/45': 35
}

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    try:
        # Input parameters from the front end
        concrete_class = data["concreteClass"]
        fyk_main = float(data["fykMain"])  # Steel yield strength in N/mm²
        f_ck = CONCRETE_STRENGTHS.get(concrete_class, 25)  # Concrete strength in MPa

        # Section dimensions
        b = float(data.get("sectionWidth", 300))  # Section width in mm
        h = float(data.get("sectionDepth", 500))  # Section depth in mm
        d = h - 50  # Effective depth, assuming 50mm cover (adjust as needed)

        # Load data
        Mu = float(data.get("ultimateMoment", 100)) * 1e6  # Ultimate moment in Nmm

        # Lever arm approximation (for this example, using a typical value of 0.95d)
        z = 0.95 * d

        # Required area of steel (A_s) calculation
        A_s_req = Mu / (0.87 * fyk_main * z)  # Area of steel required

        # Prepare the result dictionary with output values
        result = {
            "Concrete Strength (f_ck)": f_ck,
            "Section Width (b)": b,
            "Section Depth (h)": h,
            "Effective Depth (d)": d,
            "Ultimate Moment (Mu)": Mu,
            "Lever Arm (z)": z,
            "Required Area of Steel (A_s_req)": round(A_s_req, 2)
        }
    
    except Exception as e:
        result = {"error": str(e)}
    
    return jsonify(result)

@bp.route("/save_pdf", methods=["POST"])
def save_pdf():
    data = request.json  # Receive calculation results data from front end
    try:
        # PDF generation with calculation results
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="RC Beam Design Calculation Results", ln=True, align='C')
        pdf.ln(10)
        
        for key, value in data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        # Save to a temporary file and return the PDF
        pdf_output_path = tempfile.mktemp(suffix=".pdf")
        pdf.output(pdf_output_path)
        
        return send_file(pdf_output_path, as_attachment=True, download_name="RC_Beam_Design.pdf", mimetype="application/pdf")

    except Exception as e:
        return jsonify({"error": str(e)})
