import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from flask import Blueprint, render_template, request, jsonify
from io import BytesIO
import base64

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    result = None
    plot_image = None
    if request.method == "POST":
        try:
            # Get all input values and set default values if missing
            concrete_class = request.form.get("concrete_class") or 30  # Example default concrete class
            f_ck = int(concrete_class)
            f_yk_main = float(request.form.get("f_yk_main") or 500)  # Default 500 N/mm²
            f_yk_shear = float(request.form.get("f_yk_shear") or 500)
            gamma_c = float(request.form.get("gamma_c") or 1.5)
            alpha_cc = float(request.form.get("alpha_cc") or 0.85)
            gamma_s = float(request.form.get("gamma_s") or 1.15)
            min_cover = float(request.form.get("min_cover") or 30)
            cover_dev = float(request.form.get("cover_dev") or 10)
            c_nom = min_cover + cover_dev
            h = float(request.form.get("section_depth") or 500)
            b = float(request.form.get("section_width") or 300)
            d_w = float(request.form.get("d_w") or 0)

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
            y_c = sum(A_sc * (d / 2) for d, A_sc in compression_layers) / A_sc_total if A_sc_total > 0 else 0

            # Effective depths and further calculations
            d_eff = h - c_nom - d_w - y_t
            dc_eff = c_nom + d_w + y_c

            # Example calculation for demonstration
            section_type = "Doubly Reinforced" if A_sc_total > 0 else "Singly Reinforced"

            # Generate a section diagram as in your Windows app
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.add_patch(Rectangle((0, 0), b, h, fill=True, facecolor='lightblue', edgecolor='blue'))
            ax.add_patch(Rectangle((c_nom, c_nom), b - 2 * c_nom, h - 2 * c_nom, fill=False, edgecolor='red', linewidth=d_w / 10))

            for i, (d_s, A_s) in enumerate(tension_layers):
                y_position = c_nom + d_w + d_s / 2 + i * (d_s + 10)
                n_bars = int(A_s / (math.pi * (d_s ** 2) * 0.25))
                spacing = (b - 2 * (c_nom + d_w + d_s / 2)) / (n_bars - 1) if n_bars > 1 else 0
                for j in range(n_bars):
                    x_position = c_nom + d_w + d_s / 2 + j * spacing
                    ax.add_patch(Circle((x_position, y_position), d_s / 2, color='black'))

            for i, (d_sc, A_sc) in enumerate(compression_layers):
                y_position = h - (c_nom + d_w + d_sc / 2 + i * (d_sc + 10))
                n_bars = int(A_sc / (math.pi * (d_sc ** 2) * 0.25))
                spacing = (b - 2 * (c_nom + d_w + d_sc / 2)) / (n_bars - 1) if n_bars > 1 else 0
                for j in range(n_bars):
                    x_position = c_nom + d_w + d_sc / 2 + j * spacing
                    ax.add_patch(Circle((x_position, y_position), d_sc / 2, color='black'))

            plt.axis('equal')
            plt.axis('off')
            image_bytes = BytesIO()
            plt.savefig(image_bytes, format='png')
            plt.close(fig)
            image_bytes.seek(0)
            plot_image = base64.b64encode(image_bytes.read()).decode('utf-8')

            result = {
                "section_type": section_type,
                "effective_depth": d_eff,
                "dc_eff": dc_eff,
                # Add other calculated values here
            }

        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result, plot_image=plot_image)
