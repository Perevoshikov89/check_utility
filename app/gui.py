import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional, Tuple
from app.signer import sign_xml_file
from app.sender import send_signed_xml



class AppGUI:
    """
    Класс, реализующий графический интерфейс для выбора файла и папки.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Утилита подписи и отправки XML")

        self.xml_path: Optional[Path] = None
        self.output_dir: Optional[Path] = None

        self._build_gui()

    def _build_gui(self):
        # Кнопка выбора XML
        tk.Button(self.root, text="Выбрать XML-файл", command=self.choose_xml).pack(pady=5)

        # Кнопка выбора папки
        tk.Button(self.root, text="Выбрать папку для результата", command=self.choose_output_dir).pack(pady=5)

        # Кнопка запуска
        tk.Button(self.root, text="Выполнить", command=self.submit).pack(pady=10)

        # Инфо-лейбл
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack()

    def choose_xml(self):
        path = filedialog.askopenfilename(filetypes=[("XML файлы", "*.xml")])
        if path:
            self.xml_path = Path(path)
            self.status_label.config(text=f"Выбран файл: {self.xml_path.name}")

    def choose_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir = Path(path)
            self.status_label.config(text=f"Выбрана папка: {self.output_dir}")

    def submit(self):
        if not self.xml_path or not self.output_dir:
            messagebox.showerror("Ошибка", "Выберите XML и папку перед запуском.")
            return

        # Вызов основной логики (будет добавлено позже)
        messagebox.showinfo("Запуск", f"Начинаем обработку...\nФайл: {self.xml_path.name}")

        # Тут будет подключение основной цепочки
        # process_xml_request(self.xml_path, self.output_dir)
        from app.signer import sign_xml_file

        # внутри метода submit
        try:
            signed_path = sign_xml_file(self.xml_path, self.output_dir)
            self.status_label.config(text=f"Файл подписан: {signed_path.name}")
        except Exception as e:
            messagebox.showerror("Ошибка подписи", str(e))
            return

                # 1. Задать адрес запроса (временно хардкод)
        url = "https://example.com/api/send"  # <-- Заменим позже

        try:
            zip_bytes = send_signed_xml(signed_path, url)
            self.status_label.config(text=f"Ответ получен ({len(zip_bytes)} байт)")
        except Exception as e:
            messagebox.showerror("Ошибка отправки", str(e))
            return
            


    def run(self):
        self.root.mainloop()
