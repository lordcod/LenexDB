import json
import traceback
import customtkinter as ctk
from lenexdb.registered import RegisteredDistance
from tkinter import messagebox as mb
from pathlib import Path
from processlogger import CTkProcessLogger
from loguru import logger

validate_types = [('Lenex file', ('.lxf', '.lef')),
                  ('XML file', '.xml')]
json_types = [('JSON file', '.json')]
default_data = {
    "styles": {
        "FREE": "Вольный стиль",
        "BACK": "На спине",
        "BREAST": "Брасс",
        "FLY": "Баттерфляй",
        "MEDLEY": "Комплекс"
    },
    "reversed_styles": {
        "Вольный стиль": "FREE",
        "На спине": "BACK",
        "Брасс": "BREAST",
        "Баттерфляй": "FLY",
        "Комплекс": "MEDLEY",
        "Комплексное плавание": "MEDLEY"
    },
    "location": {
        "lastname": 0,
        "firstname": 1,
        "gender": 2,
        "license": 3,
        "birthdate": 4,
        "club": 5,
        "stroke": 6,
        "distance": 7,
        "entrytime": 8
    },
    "replacement": {
        ".": "",
        " ": "",
        "взрослый": "",
        "разряд": "",
        "взр": "",
        "вз": "",
        "|": "I",
        "МС": "мс",
        "КМС": "кмс",
        "юношеский": "юн",
        "1": "I",
        "2": "II",
        "3": "III",
        "спортивный": "",
        "-ой": "",
        "-в": "",
        "-": ""
    }
}


def get_file_name(path: str) -> str:
    return Path(path).name


def on_create_logger(func):
    def wrapper(self: 'App', *args, **kwargs):
        try:
            self.create_ctk_logger()
            self.after(100, self.ctk_logger.focus)
        except TypeError:
            return

        result = func(self, *args, **kwargs)
        self.after(60000, self.hide_ctk_logger)
        return result
    return wrapper


class App(ctk.CTk):
    def __init__(self, data: dict):
        super().__init__()

        self.data = data
        self.location = data['location']
        self.replacement = data['replacement']
        self.file_xlsx = None
        self.file_lxf = None
        self.file_config = None
        self.ctk_logger = None

        self.geometry("620x500")
        self.resizable(False, False)

        self.files_view = ctk.CTkTabview(
            self, width=580, height=120)
        self.files_view.grid(row=0, column=0, padx=20,
                             pady=(0, 0), sticky="nsew")
        for n in ['Process', 'Files', 'Config']:
            self.files_view.add(n)
            self.files_view.tab(n).grid_columnconfigure(0, weight=0)

        self.info_file_lxf = ctk.CTkLabel(self.files_view.tab('Files'),
                                          text='No chosen file')
        self.info_file_lxf.grid(row=0, column=0, padx=20)
        self.button_file_lxf = ctk.CTkButton(self.files_view.tab('Files'),
                                             text="Open file (LXF, LEF)",
                                             command=self.click_open_file_lxf)
        self.button_file_lxf.grid(row=1, column=0, padx=20)

        self.info_file_xlsx = ctk.CTkLabel(self.files_view.tab('Files'),
                                           text='No chosen file', height=10)
        self.info_file_xlsx.grid(row=0, column=1, padx=20)
        self.button_file_xlsx = ctk.CTkButton(self.files_view.tab('Files'),
                                              text="Open file (XLSX)",
                                              command=self.click_open_file_xlsx)
        self.button_file_xlsx.grid(row=1, column=1, padx=20)

        self.button_saved_file_lxf = ctk.CTkButton(self.files_view.tab('Files'),
                                                   text="Save file (LXF, LEF)",
                                                   state='disabled',
                                                   command=self.click_save_file_lxf)
        self.button_saved_file_lxf.grid(row=1, column=2, padx=20)

        self.info_config_import = ctk.CTkLabel(self.files_view.tab('Config'),
                                               text='Default',
                                               width=210)
        self.info_config_import.grid(row=0, column=0, padx=30)
        self.button_config_import = ctk.CTkButton(self.files_view.tab('Config'),
                                                  text="Import config",
                                                  command=self.click_import_config,
                                                  width=210)
        self.button_config_import.grid(row=1, column=0, padx=30)

        self.button_config_export = ctk.CTkButton(self.files_view.tab('Config'),
                                                  text="Export config",
                                                  command=self.click_export_config,
                                                  width=210)
        self.button_config_export.grid(
            row=1, column=1, padx=30)

        self.button_start = ctk.CTkButton(self.files_view.tab('Process'),
                                          text="Start!",
                                          command=self.click_start,
                                          state='disabled',
                                          width=210)
        self.button_start.grid(row=0, column=0, padx=30, pady=(10, 10))

        self.button_add = ctk.CTkButton(self.files_view.tab('Process'),
                                        text="Add!",
                                        command=self.click_update,
                                        state='disabled',
                                        width=210)
        self.button_add.grid(row=0, column=1, padx=30, pady=(10, 10))

        self.tabs_frame = ctk.CTkFrame(
            self, width=540, height=550)
        self.tabs_frame.grid(row=1, column=0, padx=20,
                             pady=(10, 0), sticky="nsew")
        self.tabview = ctk.CTkTabview(self.tabs_frame, width=350, height=275)
        self.tabview.grid(row=1, padx=115, pady=(10, 20), sticky="nsew")
        for n in ['Replacement', 'Config']:
            self.tabview.add(n)
            self.tabview.tab(n).grid_columnconfigure(0, weight=0)

        self.box = ctk.CTkScrollableFrame(self.tabview.tab(
            'Replacement'), width=275, height=80)
        self.box.grid(padx=10, pady=5)
        self.entries = []
        for i, (a, b) in enumerate(self.replacement.items()):
            args = self._create_entry_box(self.box, i, a, b)
            self.entries.append(args)
        self.box_ent_add = ctk.CTkButton(
            self.box, width=100, text='Добавить', command=self.click_create_entry)
        self.box_ent_add.grid(row=len(self.entries),
                              columnspan=2, pady=10, padx=(15, 0))
        self.box_ent_save = ctk.CTkButton(
            self.box, width=100, text='Сохранить', state='disabled', command=self.click_save_replacement)
        self.box_ent_save.grid(row=len(self.entries), column=2,
                               columnspan=2, pady=10, padx=(15, 0))

        self.labels_replacement = {}
        for i, n in enumerate(self.location.keys()):
            label = ctk.CTkLabel(
                self.tabview.tab('Config'),
                text=n
            )
            label.grid(row=i//3*2, column=i % 3, padx=(25, 0), pady=(10, 0))
            entry = ctk.CTkEntry(self.tabview.tab(
                'Config'), width=70)
            entry.insert(0, self.location.get(n))
            entry.grid(row=i//3*2+1, column=i % 3, padx=(25, 0), pady=0)
            entry.configure(validate='all', validatecommand=(self.register(self.validate_location_config), '%P'))
            entry.bind("<KeyRelease>", self.update_text_config)
            self.labels_replacement[n] = entry

    def create_ctk_logger(self):
        if self.ctk_logger and self.ctk_logger.winfo_exists():
            self.ctk_logger.clear()
            self.ctk_logger.focus()
            return
        self.ctk_logger = CTkProcessLogger(self)
        self.ctk_logger.clear()

    def hide_ctk_logger(self):
        if not self.ctk_logger:
            return
        self.ctk_logger.destroy()
        self.ctk_logger = None

    def update_config(self):
        self.register
        for n, entry in self.labels_replacement.items():
            entry.delete(0, len(entry.get()))
            entry.insert(0, self.location.get(n))

        for args in self.entries:
            for el in args:
                el.destroy()

        self.entries = []
        for i, (a, b) in enumerate(self.replacement.items()):
            args = self._create_entry_box(self.box, i, a, b)
            self.entries.append(args)
        self.box_ent_add.grid(row=len(self.entries),
                              columnspan=2, pady=10, padx=(15, 0))
        self.box_ent_save.grid(row=len(self.entries), column=2,
                               columnspan=2, pady=10, padx=(15, 0))
        self.box_ent_save.configure(state='disabled')

    def validate_location_config(self, text):
        return not text or (text.isdigit() and int(text) < 100)

    def update_text_config(self, *args):
        for n, entry in self.labels_replacement.items():
            s = entry.get()
            if not s:
                continue
            self.location[n] = int(s)
        self.data['location'] = self.location

    def _create_entry_box(self, box, i, a, b):
        on_edit = lambda *args: self.box_ent_save.configure(state='normal')
        label_i = ctk.CTkLabel(box, text=i+1)
        label_i.grid(row=i, column=0, padx=(10, 0))

        label_a = ctk.CTkEntry(box, width=90)
        label_a.insert(0, a)
        label_a.grid(row=i, column=1, padx=(10, 0))
        label_a.bind("<KeyRelease>", on_edit)

        label_b = ctk.CTkEntry(box, width=90)
        label_b.insert(0, b)
        label_b.grid(row=i, column=2, padx=(10, 0))
        label_b.bind("<KeyRelease>", on_edit)

        button_d = ctk.CTkButton(
            box, text='DEL', width=25)
        button_d.grid(row=i, column=3, padx=(10, 0))
        button_d.configure(command=self.click_delete_entry(button_d))

        return label_i, label_a, label_b, button_d

    def click_save_replacement(self):
        self.replacement.clear()
        for _, but_a, but_b, _ in self.entries:
            self.replacement[but_a.get()] = but_b.get()
        self.box_ent_save.configure(state='disabled')

    def click_create_entry(self):
        args = self._create_entry_box(self.box, len(self.entries), '', '')
        self.entries.append(args)
        self.box_ent_add.grid(row=len(self.entries),
                              columnspan=2, pady=10, padx=(15, 0))
        self.box_ent_save.grid(row=len(self.entries), column=2,
                               columnspan=2, pady=10, padx=(15, 0))
        self.box_ent_save.configure(state='normal')

    def click_delete_entry(self, but):
        def on_():
            nonlocal but
            print(but)
            i = but.grid_info().get('row')
            args = self.entries.pop(i)
            for el in args:
                el.destroy()

            for n, args in enumerate(self.entries[i:], start=i):
                args[0].configure(text=n+1)
                for a in args:
                    a.grid(row=n)
            self.box_ent_save.configure(state='normal')
        return on_

    def click_import_config(self):
        file = ctk.filedialog.askopenfilename(
            filetypes=json_types,
            initialfile=self.file_config)
        if not file:
            return

        self.file_config = file
        data = json.load(open(file, "rb+"))
        self.data = data
        self.location = data['location']
        self.replacement = data['replacement']
        self.update_config()
        self.info_config_import.configure(text=get_file_name(file))

    def click_export_config(self):
        file = ctk.filedialog.asksaveasfilename(
            filetypes=json_types)
        if not file:
            return

        data = {
            **self.data,
            'location': self.location,
            'replacement': self.replacement
        }
        with open(file, 'wb+') as f:
            f.write(json.dumps(data, ensure_ascii=False).encode())

    def click_open_file_lxf(self):
        file = ctk.filedialog.askopenfilename(
            filetypes=validate_types,
            initialfile=self.file_lxf)
        if not file:
            return

        self.file_lxf = file
        self.button_start.configure(state='normal' if self.file_lxf is not None
                                    and self.file_xlsx is not None else 'disabled')
        self.info_file_lxf.configure(text=get_file_name(file))

    def click_open_file_xlsx(self):
        file = ctk.filedialog.askopenfilename(
            filetypes=[('XLSX', '.xlsx')],
            initialfile=self.file_xlsx)
        if not file:
            return

        self.file_xlsx = file
        self.button_start.configure(state='normal' if self.file_lxf is not None
                                    and self.file_xlsx is not None else 'disabled')
        self.info_file_xlsx.configure(text=get_file_name(file))

    def click_save_file_lxf(self):
        file = ctk.filedialog.asksaveasfilename(
            filetypes=validate_types)
        if not file:
            return
        if '.' not in file:
            file += '.lxf'

        self.parser.bapi.save(file)
        self.button_saved_file_lxf.configure(state='disabled')
        mb.showinfo(
            'Успешно',
            'Файл успешно сохранен!'
        )

    @on_create_logger
    def click_start(self):
        try:
            self.parser = RegisteredDistance(
                self.file_lxf, self.file_xlsx, self.data)
            self.parser.logger = logger
            self.parser.parse()
        except Exception:
            err = traceback.format_exc()
            mb.showerror(
                'Exception', 'Check if all the cells match the columns!\n'+err)
        else:
            self.button_saved_file_lxf.configure(state='normal')
            self.button_add.configure(state='normal')
            logger.info('Файл готов к импорту!')
            self.ctk_logger.focus()

    @on_create_logger
    def click_update(self):
        if self.parser.bapi.filename != self.file_lxf:
            self.button_add.configure(state='disabled')
            return

        try:
            self.parser = RegisteredDistance.base_init(
                self.parser.bapi, self.file_xlsx, self.data)
            self.parser.add_elements()
            self.parser.parse()
        except Exception as exc:
            err = traceback.format_exception(exc)
            mb.showerror(
                'Exception', 'Check if all the cells match the columns!\n'+err)
        else:
            self.button_saved_file_lxf.configure(state='normal')
            self.button_add.configure(state='normal')
            logger.info('Файл готов к импорту!')
            self.ctk_logger.focus()


try:
    try:
        data = json.load(open("data.json", "rb"))
    except (FileNotFoundError, json.JSONDecodeError):
        open("data.json", "w+").write(json.dumps(default_data))
        data = default_data
    app = App(data)
    app.mainloop()
except BaseException:
    traceback.print_exc()
    input()
