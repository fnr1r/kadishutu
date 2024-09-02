import kadishutu.gui.prompt_install


def handle_no_qt() -> int:
    from tkinter import messagebox
    messagebox.showerror(
        "kadishutu",
        "Something went wrong in the build process, making the GUI unusable."
    )
    return 1


kadishutu.gui.prompt_install.handle_no_qt = handle_no_qt
