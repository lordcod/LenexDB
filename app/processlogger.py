import customtkinter as ctk
from ctkloguru import LoguruWidget, setup_logger


class CTkProcessLogger(ctk.CTkToplevel):
    def __init__(self, *args, fg_color=None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.title("The parsing process")
        self.geometry("600x400")

        self.log_widget = LoguruWidget(
            self, show_scrollbar=False, color_mode='level', max_lines=1000)
        self.log_widget.pack(expand=True, fill=ctk.BOTH, padx=10, pady=10)
        setup_logger(self.log_widget)

    def clear(self):
        q = self.log_widget.queue
        with q.mutex:
            q.queue.clear()


if __name__ == '__main__':
    from loguru import logger
    toplevel = None

    def on_open():
        global toplevel
        if toplevel is None:
            toplevel = CTkProcessLogger(root)
            toplevel.log_widget.color_mode = 'full'
            logger.error('Full!')
            root.iconify()
            toplevel.focus()

    def on_close():
        global toplevel
        if toplevel is not None:
            toplevel.destroy()
            toplevel = None

    root = ctk.CTk()
    open = ctk.CTkButton(root, text='open', command=on_open)
    open.pack(pady=10, padx=10)
    close = ctk.CTkButton(root, text='close', command=on_close)
    close.pack(pady=10, padx=10)

    root.mainloop()
