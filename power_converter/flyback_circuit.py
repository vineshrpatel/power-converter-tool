from PIL import Image, ImageDraw, ImageFont, ImageTk
from matplotlib import pyplot as plt
import io
import importlib.resources as pkg_resources
from power_converter import circuit_diagrams

def display_flyback_equations(img, font_size):
    """
    Displays equations below circuit diagram
    img       :  image with extra height added to display equations
    y_offset  :  height at which equations are to be added
    font_size :  font size of equations 
    ----
    Returns   :  img with formatted equations 
    """
    equations = [
        r"Equations used:",
        r"$D = \frac{V_{\text{out}}}{V_{\text{in}}+V_{\text{out}}}$",
        r"$I_{\text{load}} = \frac{V_{\text{out}}}{R_{\text{load}}}$",
        r"$N_S = \frac{V_{\text{out}}(1-D)N_P}{V_{\text{in}}D}\;\;\;\;\;(\text{assumption}\;N_P=1)$",
        r"$n = \frac{N_P}{N_S}$",
        r"$L_\text{P,crit} = \frac{n^2 (1-D)^2 R_{\text{load}}}{2f_s}$",
        r"$L_S = \frac{L_P}{n^2}$",
        r"$\Delta I_{L_P} = \frac{V_{in}D}{L_P,crit \cdot f}$",
        r"$\Delta I_{L_S} = \frac{V_{in}D}{L_S \cdot f}$",
        r"$V_\text{rev,Diode} = \frac{N_S \cdot V_{\text{in}}}{V_{\text{out}}}$",
        r"$C = \frac{D V_{\text{out}}}{\Delta V \cdot R_{\text{load}} \cdot f}$",
    ]

    # Equation font
    plt.rcParams.update({
    "text.usetex": False,  # Use Matplotlib's internal LaTeX engine
    "mathtext.fontset": "cm",  # Use Computer Modern font without external LaTeX
    "font.family": "STIXGeneral",
    "mathtext.default": "it",
    "figure.dpi": 600,  # Increase DPI (default is usually 100)
    "savefig.dpi": 600  # Increase saving DPI
    })

    y_offset = 25
    for equation in equations:
        fig = plt.figure(figsize=(6,1))
        fig.tight_layout(pad=0)
        fig.text(0.5, 0.5, equation, fontsize=font_size)

        # Save the figure to a memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, dpi=600)
        buf.seek(0)

        # Load the PNG from the buffer and paste to main image
        equation_image = Image.open(buf).convert("RGBA") # RGBA to keep transparency

        # Optional: adjust size while maintaining quality
        new_width = int(equation_image.size[0] * 0.25)  # Scale down if too large
        new_height = int(equation_image.size[1] * 0.25)
        equation_image = equation_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        img.paste(equation_image, (50, y_offset), equation_image) 
        y_offset += 40
        plt.close(fig)
    return img


def display_flyback(Vin, Lp, Ls, C, R_load, I_load, canvas):
    # Display circuit
    with pkg_resources.path(circuit_diagrams, 'flyback_circuit.png') as img_path:
        circuit = Image.open(img_path)
    
    # Add values to circuit image
    draw = ImageDraw.Draw(circuit)
    font = ImageFont.truetype("arial.ttf", 80)
    draw.text((80, 700), f"{Vin}V", fill=(0, 0, 0), font=font)  # Voltage source
    draw.text((600, 330), f"{Lp}H", fill=(0, 0, 0), font=font)  # Primary Inductor
    draw.text((1350, 430), f"{Ls}H", fill=(0, 0, 0), font=font)  # Secondary Inductor
    draw.text((1700, 650), f"{C}F", fill=(0, 0, 0), font=font)  # Capacitor
    draw.text((2700, 500), f"{R_load}Ω", fill=(0, 0, 0), font=font)  # Load Resistor
    draw.text((2700, 200), f"{I_load}A", fill=(0, 0, 0), font=font)  # Load Current

    # Resize both images
    scale_factor = 0.18
    circuit_width = int(circuit.width * scale_factor)
    circuit_height = int(circuit.height * scale_factor)
    circuit = circuit.resize((circuit_width, circuit_height), Image.Resampling.LANCZOS)

    eq_img = Image.new('RGB', (circuit.width, 500), color='white')
    eq_img = display_flyback_equations(eq_img, 10)

    # Convert both to PhotoImage
    circuit_photo = ImageTk.PhotoImage(circuit)
    eq_photo = ImageTk.PhotoImage(eq_img)

    # Store references to prevent garbage collection
    canvas.circuit_image = circuit_photo
    canvas.eq_image = eq_photo

    # Clear canvas
    canvas.delete("all")

    # Display circuit at top
    canvas.create_image(
        canvas.winfo_width()//2,  # Center horizontally
        0,                        # Align to top
        anchor="n",
        image=circuit_photo
    )

    # Display equations below circuit
    canvas.create_image(
        canvas.winfo_width()//2,  # Center horizontally
        circuit.height + 5,      # Position below circuit with small gap
        anchor="n",
        image=eq_photo
    )

    # Update canvas scroll region
    total_height = circuit.height + eq_img.height + 20  # Add some padding
    canvas.configure(scrollregion=(0, 0, circuit.width, total_height))