import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional
from app.signer import sign_xml_file, list_certificates
from app.sender import send_signed_xml
from app.unzipper import extract_zip_response
from app.verifier import remove_signature


class AppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Подпись и отправка XML")

        self.xml_path: Optional[Path] = None
        self.output_dir: Optional[Path] = None
        self.selected_thumbprint: Optional[str] = None

        self._build_gui()

    def _build_gui(self):
        tk.Button(self.root, text="Выбрать XML-файл", command=self.choose_xml).pack(pady=5)
        tk.Button(self.root, text="Выбрать папку для результата", command=self.choose_output_dir).pack(pady=5)
        tk.Button(self.root, text="Выбрать сертификат", command=self.choose_cert).pack(pady=5)

        self.cert_label = tk.Label(self.root, text="Сертификат не выбран", fg="darkred")
        self.cert_label.pack()

        tk.Button(self.root, text="Выполнить", command=self.submit).pack(pady=10)

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

    def choose_cert(self):
        try:
            certs = list_certificates()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить список сертификатов:\n{e}")
            return

        if not certs:
            messagebox.showerror("Ошибка", "Сертификаты не найдены в хранилище пользователя.")
            return

        win = tk.Toplevel(self.root)
        win.title("Выбор сертификата")

        listbox = tk.Listbox(win, width=100, height=10)
        for thumb, subj in certs:
            listbox.insert(tk.END, f"{subj} | {thumb}")
        listbox.pack(padx=10, pady=10)

        def on_select():
            index = listbox.curselection()
            if not index:
                return
            selected = certs[index[0]]
            self.selected_thumbprint = selected[0]
            self.cert_label.config(text=f"Выбран: {selected[1]}")
            win.destroy()

        tk.Button(win, text="Выбрать", command=on_select).pack(pady=5)

    def submit(self):
        if not self.xml_path or not self.output_dir:
            messagebox.showerror("Ошибка", "Выберите XML и папку перед запуском.")
            return
        if not self.selected_thumbprint:
            messagebox.showerror("Ошибка", "Выберите сертификат для подписи.")
            return

        url = "https://client.demo.nbki.msk:8082/products/B2BRUTDF"

        try:
            self.status_label.config(text="Подписываем XML...")
            signed_path = sign_xml_file(self.xml_path, self.output_dir, self.selected_thumbprint)

            self.status_label.config(text="Отправляем запрос на сервер...")
            zip_bytes = send_signed_xml(signed_path, url)

            self.status_label.config(text="Распаковываем ответ...")
            xml_extracted = extract_zip_response(zip_bytes, self.output_dir)

            if not xml_extracted:
                raise RuntimeError("В архиве не найден XML-файл.")

            self.status_label.config(text="Снимаем подпись с XML...")
            xml_clean = remove_signature(xml_extracted, self.output_dir)

            self.status_label.config(text=f"Готово! Сохранено: {xml_clean.name}")
            messagebox.showinfo("Успех", f"Обработка завершена.\nРезультат: {xml_clean}")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def run(self):
        self.root.mainloop()
