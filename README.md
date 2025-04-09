# Power Converter Tool

A GUI to aid with DC-DC power converter component sizing based on user inputs. Pre-defined equations are used for the converter topology considered to size components, update a circuit schematic of the toplogy and verify calculations with graphs produced from LTSpice simulations.

The package covers the majority of non-isolated and isolated DC-DC converter topologies, of which are seen below:
- Non-isolated converters 
    - Buck
    - Boost
    - Buck-Boost
    - Ćuk
    - Zeta
    - SEPIC
- Isolated converters
    - Flyback
    - Forward
    - Pushpull
    - Halfbridge
    - Fullbridge

## Notes

All LTSpice simulations use the BSC060N10NS3 MOSFET which has $V_{DS}=100 V$. Please note the simulation may still run using higher voltages but is not representative of the real-world device.<br>

All LTSpice simulations use the UPSC600 Schottky didoe which has $V_{breakdown} = 600 V$.


## Installation

Note, in Windows you may need to temporarily disable Git's check for post-checkout hooks to pip install the package.
```
set "GIT_CLONE_PROTECTION_ACTIVE=false" && git clone https://github.com/vineshrpatel/power-converter-tool
```

After cloning the repository:
```
pip install "power-converter-tool\dist\power_converter-0.1.1-py3-none-any.whl"
```

## Example Usage

```
from power_converter import boost_gui

boost_gui.run_boost_gui()
```

Note, for other converters replace 'boost' with the converter name (lowercase with no spaces)

## Acknowledgement

I acknowledge the use of ChatGPT, Claude, and Gemini in the development of aspects of python scripts for this project.