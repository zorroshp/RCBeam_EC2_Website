import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from flask import Blueprint, render_template, request, send_file, jsonify
from io import BytesIO
from fpdf import FPDF

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    result = None
    plot_image = None
    if request.method == "POST":
        try:
            # Get all input values
            concrete_class = request.form.get("concrete_class")
            f_ck = int(concrete_class)  # Adjust based on the form options
            f_yk_main = float(request.form.get("f_yk_main"))
            f_yk_shear = float(request.form.get("f_yk_shear"))
            gamma_c = float(request.form.get("gamma_c"))
            alpha_cc = float(request.form.get("alpha_cc"))
            gamma_s = float(request.form.get("gamma_s"))
            min_cover = float(request.form.get("min_cover"))
            cover_dev = float(request.form.get("cover_dev"))
            c_nom = min_cover + cover_dev
            h = float(request.form.get("section_depth"))
            b = float(request.form.get("section_width"))
            d_w = float(request.form.get("d_w")) if request.form.get("d_w") else 0

            # Get reinforcement data
            tension_layers = []
            for i in range(1, 7):
                diameter = request.form.get(f"tension_diameter_{i}")
                number = request.form.get(f"tension_number_{i}")
                if diameter and number:
                    tension_layers.append((float(diameter), int(number)))

            compression_layers = []
            for i in range(1, 7):
                diameter = request.form.get(f"compression_diameter_{i}")
                number = request.form.get(f"compression_number_{i}")
                if diameter and number:
                    compression_layers.append((float(diameter), int(number)))

            # Calculate the reinforcement areas
            A_s_total = sum(math.pi * (d ** 2) * 0.25 * n for d, n in tension_layers)
            y_t = sum(A_s * (d / 2) for d, A_s in tension_layers) / A_s_total if A_s_total > 0 else 0

            A_sc_total = sum(math.pi * (d ** 2) * 0.25 * n for d, n in compression_layers)
            y_c = sum(A_s * (d / 2) for d, A_s in compression_layers) / A_sc_total if A_sc_total > 0 else 0

            # Effective depths and further calculations
            d_eff = h - c_nom - d_w - y_t
            dc_eff = c_nom + d_w + y_c

            # ... (Include all calculation logic from your Windows app's `calculate` function)

            # Generate a section diagram as in your Windows app
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.add_patch(Rectangle((0, 0), b, h, fill=True, facecolor='lightblue', edgecolor='blue'))
            ax.add_patch(Rectangle((c_nom, c_nom), b - 2 * c_nom, h - 2 * c_nom, fill=False, edgecolor='red', linewidth=d_w / 10))

            for i, (d_s, A_s) in enumerate(tension_layers):
                # Calculate spacing and positions for the circles (similar to Windows app)
                # Code for plotting circles for tension and compression bars

            # Save figure to bytes
            image_bytes = BytesIO()
            plt.savefig(image_bytes, format='png')
            plt.close(fig)
            image_bytes.seek(0)
            plot_image = image_bytes.read()

            result = {
                "section_type": "Doubly Reinforced" if A_sc_total > 0 else "Singly Reinforced",
                "effective_depth": d_eff,
                # Add other calculated values here
            }

        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result, plot_image=plot_image)
