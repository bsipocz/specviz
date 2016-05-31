import os
import logging

from ..ui.widgets.utils import ICON_PATH
from ..ui.widgets.plugin import Plugin
from ..core.comms import Dispatch, DispatchHandle
from ..ui.widgets.dialogs import TopAxisDialog, UnitChangeDialog

from astropy.units import Unit


class PlotToolsPlugin(Plugin):
    name = "Plot Tools"
    location = "hidden"
    _all_categories = {}

    def setup_ui(self):
        self._top_axis_dialog = TopAxisDialog()
        self._unit_change_dialog = UnitChangeDialog()

        # Change top axis
        self.button_axis_change = self.add_tool_button(
            description='Change top axis',
            icon_path=os.path.join(ICON_PATH, "Merge Vertical-48.png"),
            category='plot options',
            callback=self._top_axis_dialog.exec_,
            enabled=False)

        # Change top axis
        self.button_unit_change = self.add_tool_button(
            description='Change plot units',
            icon_path=os.path.join(ICON_PATH, "Merge Vertical-48.png"),
            category='plot options',
            callback=self._show_unit_change_dialog,
            enabled=False)

    def setup_connections(self):
        # On accept, change the displayed axis
        self._top_axis_dialog.accepted.connect(
            self._update_axis)

    def _show_unit_change_dialog(self):
        if self._unit_change_dialog.exec_():
            x_text = self._unit_change_dialog.disp_unit
            y_text = self._unit_change_dialog.flux_unit

            x_unit = y_unit = None

            try:
                x_unit = Unit(x_text) if x_text else None
            except ValueError as e:
                logging.error(e)

            try:
                y_unit = Unit(y_text) if y_text else None
            except ValueError as e:
                logging.error(e)

            self.change_units(x_unit, y_unit)

            self._plot_item.update()

    def _update_axis(self):
        if self.active_window is None:
            return

        self.active_window.update_axis(
            self.active_window._containers[0].layer,
            self._top_axis_dialog.combo_box_axis_mode.currentIndex(),
            redshift=self._top_axis_dialog.redshift,
            ref_wave=self._top_axis_dialog.ref_wave)

    @DispatchHandle.register_listener("on_activated_window")
    def toggle_enabled(self, window):
        if window:
            self.button_axis_change.setEnabled(True)
            self.button_unit_change.setEnabled(True)
        else:
            self.button_axis_change.setEnabled(False)
            self.button_unit_change.setEnabled(False)
