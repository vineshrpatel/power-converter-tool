from PyLTSpice import SimCommander
import ltspice
import matplotlib.pyplot as plt
import os

def ltspice_flyback_simulation(f, D, Vin, L1, L2, C, R):

    AbsPath = os.path.dirname(os.path.realpath(__file__)) 
    # LTC = SimCommander(AbsPath + "\\boost_circuit.asc")

    # Full path to circuit file
    circuit_file = os.path.join(AbsPath, "ltspice_circuits", "flyback_circuit.asc")
    raw_file = os.path.join(AbsPath, "ltspice_circuits", "flyback_circuit_1.raw")
    
    # Initialize simulation
    LTC = SimCommander(circuit_file)

    T = 1/f
    ton = float(D)*T

    # LTC.add_instruction(".tran 0 1000m") # Simulates for 5ms with max timestep of 0.1µs

    # Set component values before running simulation
    LTC.set_component_value('V1', str(Vin))
    LTC.set_component_value('L1', str(L1))
    LTC.set_component_value('L2', str(L2))
    LTC.set_component_value('C1', str(C))
    LTC.set_component_value('R1', str(R))
    LTC.set_component_value('V2', f'PULSE(0 5 0 0 0 {ton} {T})')  # Format: PULSE(V1 V2 Tdelay Trise Tfall Ton Period)

    # Run simulation
    LTC.run()
    LTC.wait_completion()

    raw_file = os.path.join(AbsPath, "ltspice_circuits", "flyback_circuit_1.raw")

    # Load and parse the raw file
    l = ltspice.Ltspice(raw_file)

    l.parse()

    # Extract wanted parameters
    time =  l.get_time()
    Vout = l.get_data("V(n003)")
    I_load = l.get_data("I(R1)")
    I_L1 = l.get_data("I(L1)")
    I_L2 = l.get_data("I(L2)")
    I_switch = l.get_data("Id(M1)")

    plt.rcParams.update({
    "text.usetex": False,
    "mathtext.fontset": "dejavusans",
    "font.family": "sans-serif",
    "figure.dpi": 100,
    "savefig.dpi": 100,
    "axes.labelsize": 10,    # Font size for x and y labels
    "axes.titlesize": 12,    # Font size for subplot titles
    "xtick.labelsize": 8,    # Font size for x-axis tick labels
    "ytick.labelsize": 8     # Font size for y-axis tick labels
    })


    fig = plt.figure(figsize=(6, 4))
    
    # Create a special grid layout with height ratios for better vertical spacing
    gs = plt.GridSpec(6, 2, figure=fig, width_ratios=[1 , 1], height_ratios=[1, 1, 1, 1, 1, 1])
    
    # Create subplots with specific positions
    ax1 = fig.add_subplot(gs[0:3, 0])    # Vout - spans first 3 rows
    ax2 = fig.add_subplot(gs[0:2, 1])    # I_L1
    ax3 = fig.add_subplot(gs[3:6, 0])    # I_load - spans last 3 rows
    ax4 = fig.add_subplot(gs[2:4, 1])    # I_L2
    ax5 = fig.add_subplot(gs[4:6, 1])    # I_switch

    ax1.plot(time, Vout, '-r')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('$\\mathrm{V_{out}}$')
    ax1.yaxis.set_major_locator(plt.LinearLocator(4))
    ax1.grid(True)

    ax3.plot(time, I_load, '-k')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('$\\mathrm{I_{load}}$', fontsize=12)
    ax3.yaxis.set_major_locator(plt.LinearLocator(4))
    ax3.grid(True)

    ax2.plot(time, I_L1, '-g')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('$\\mathrm{I_{L1}}$', fontsize=12)
    ax2.yaxis.set_major_locator(plt.LinearLocator(4))
    ax2.grid(True)

    ax4.plot(time, I_L2, '-g')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('$\\mathrm{I_{L2}}$', fontsize=12)
    ax4.yaxis.set_major_locator(plt.LinearLocator(4))
    ax4.grid(True)

    ax5.plot(time, I_switch, '-b')
    ax5.set_xlabel('Time')
    ax5.set_ylabel('$\\mathrm{I_{switch}}$', fontsize=12)
    ax5.yaxis.set_major_locator(plt.LinearLocator(4))
    ax5.grid(True)

    plt.tight_layout()
    
    return fig

# ltspice_flyback_simulation(12e3, 0.37, 10, 1e-6, 1e-6, 56e-9, 10)
# plt.show()