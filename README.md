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

## Installation

After cloning the repository:
```
pip install "dist\power_converter-0.1.0-py3-none-any.whl"
```

## Example Usage

```
from power_converter import boost_gui

boost_gui.run_boost_gui()
```

Note, for other converters replace 'boost' with the converter name (lowercase with no spaces)