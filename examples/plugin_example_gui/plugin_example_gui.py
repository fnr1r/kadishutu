from kadishutu.gui.mainwindow import MainWindow

GUI_MAIN_BAK = MainWindow.__init__

def init(*args, **kwargs):
    GUI_MAIN_BAK(*args, **kwargs)
    from PySide6.QtWidgets import QMessageBox, QWidget
    QMessageBox.information(
        QWidget(),
        "Example GUI plugin loaded",
        "Plugin loading successful!",
        QMessageBox.StandardButton.Ok,
    )

MainWindow.__init__ = init
