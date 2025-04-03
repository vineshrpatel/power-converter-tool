from power_converter import boost_gui
from power_converter import buck_gui
from power_converter import buckboost_gui
from power_converter import cuk_gui
from power_converter import zeta_gui
from power_converter import sepic_gui
from power_converter import flyback_gui
from power_converter import forward_gui
from power_converter import pushpull_gui
from power_converter import halfbridge_gui
from power_converter import fullbridge_gui

ans = boost_gui.run_boost_gui() # change for conveter to test
print(ans)