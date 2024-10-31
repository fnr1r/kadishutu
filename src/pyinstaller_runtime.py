import kadishutu.tools.depinstall.generic

def likelyness() -> float:
    return 0.0

for i in kadishutu.tools.depinstall.generic.INSTALL_HANDLERS:
    i.likelyness = likelyness

kadishutu.tools.depinstall.generic.INSTALL_HANDLERS = []

def get_install_handler():
    raise NotImplementedError(
        "Install handlers are unsupported on pyinstaller"
    )

kadishutu.tools.depinstall.generic.get_install_handler = get_install_handler


import kadishutu.gui.prompt_install

def handle_no_qt() -> int:
    from tkinter import messagebox
    messagebox.showerror(
        "kadishutu",
        "Something went wrong in the build process, making the GUI unusable."
    )
    return 1

kadishutu.gui.prompt_install.handle_no_qt = handle_no_qt
