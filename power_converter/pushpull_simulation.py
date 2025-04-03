from PyLTSpice import SimCommander
import ltspice
import matplotlib.pyplot as plt
import os

def ltspice_pushpull_simulation(f, D, Vin, Lc, Lcoupling, C, R):

    AbsPath = os.path.dirname(os.path.realpath(__file__)) 
    # LTC = SimCommander(AbsPath + "\\boost_circuit.asc")

    # Full path to circuit file
    circuit_file = os.path.join(AbsPath, "ltspice_circuits", "pushpull_circuit.asc")
    raw_file = os.path.join(AbsPath, "ltspice_circuits", "pushpull_circuit_1.raw")
    
    # Initialize simulation
    LTC = SimCommander(circuit_file)

    T = 1/f
    ton = float(D)*T

    # LTC.add_instruction(".tran 0 1000m") # Simulates for 5ms with max timestep of 0.1µs

    # Set component values before running simulation
    LTC.set_component_value('V1', str(Vin))
    LTC.set_parameter('Lc', str(Lc))
    LTC.set_parameter('Ls', str(Lcoupling))
    LTC.set_component_value('C1', str(C))
    LTC.set_component_value('R1', str(R))
    LTC.set_component_value('V2', f'PULSE(0 5 {ton} 0 0 {T-ton} {T})')
    LTC.set_component_value('V3', f'PULSE(0 5 0 0 0 {ton} {T})')  # Format: PULSE(V1 V2 Tdelay Trise Tfall Ton Period)

    # Run simulation
    LTC.run()
    LTC.wait_completion()

    raw_file = os.path.join(AbsPath, "ltspice_circuits", "pushpull_circuit_1.raw")
    # l = ltspice.Ltspice('boost_circuit_1.raw')

    # Load and parse the raw file
    l = ltspice.Ltspice(raw_file)

    l.parse()

    # Extract wanted parameters
    time =  l.get_time()
    Vout = l.get_data("V(n004)")
    I_load = l.get_data("I(R1)")
    I_L = l.get_data("I(L5)")
    I_switch1 = l.get_data("Id(M1)")
    I_switch2 = l.get_data("Id(M2)")

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
    ax4 = fig.add_subplot(gs[2:4, 1])    # I_switch1
    ax5 = fig.add_subplot(gs[4:6, 1])    # I_switch2

    ax1.plot(time, Vout, '-r')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('$\\mathrm{V_{out}}$', fontsize=12)
    ax1.yaxis.set_major_locator(plt.LinearLocator(4))
    ax1.grid(True)

    ax3.plot(time, I_load, '-k')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('$\\mathrm{I_{load}}$', fontsize=12)
    ax3.yaxis.set_major_locator(plt.LinearLocator(4))
    ax3.grid(True)

    ax2.plot(time, I_L, '-g')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('$\\mathrm{I_L}$', fontsize=12)
    ax2.yaxis.set_major_locator(plt.LinearLocator(4))
    ax2.grid(True)

    ax4.plot(time, I_switch1, '-b')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('$\\mathrm{I_{switch1}}$', fontsize=12)
    ax4.yaxis.set_major_locator(plt.LinearLocator(4))
    ax4.grid(True)

    ax5.plot(time, I_switch2, '-b')
    ax5.set_xlabel('Time')
    ax5.set_ylabel('$\\mathrm{I_{switch2}}$', fontsize=12)
    ax5.yaxis.set_major_locator(plt.LinearLocator(4))
    ax5.grid(True)

    plt.tight_layout()
    
    return fig

# ltspice_pushpull_simulation(80e3, 0.37, 26, 10e-6, 20e-6, 89e-6, 10)