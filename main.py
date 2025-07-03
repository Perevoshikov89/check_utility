from app.gui import AppGUI
from app.signer import sign_xml_file
from app.sender import send_signed_xml
from app.unzipper import extract_zip_response
from app.verifier import remove_signature
from pathlib import Path
from tkinter import messagebox


class AppGUIExtended(AppGUI):
    def submit(self):
        if not self.xml_path or not self.output_dir:
            messagebox.showerror("Ошибка", "Выберите XML и папку перед запуском.")
            return
        if not self.selected_thumbprint:
            messagebox.showerror("Ошибка", "Выберите сертификат для подписи.")
            return

        # Замените на ваш рабочий URL
        url = "https://client.demo.nbki.msk:8082/products/B2BRUTDF"

        try:
            self.status_label.config(text="Подписываем XML...")
            signed_path = sign_xml_file(self.xml_path, self.output_dir, self.selected_thumbprint)

            self.status_label.config(text="Отправляем запрос...")
            zip_bytes = send_signed_xml(signed_path, url, self.output_dir)

            self.status_label.config(text="Распаковываем ответ...")
            xml_extracted = extract_zip_response(zip_bytes, self.output_dir)

            if not xml_extracted:
                raise RuntimeError("В архиве не найден XML-файл.")

            self.status_label.config(text="Удаляем подпись...")
            xml_clean = remove_signature(xml_extracted, self.output_dir)

            self.status_label.config(text=f"Готово: {xml_clean.name}")
            messagebox.showinfo("Успех", f"Обработка завершена.\nРезультат: {xml_clean}")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    gui = AppGUIExtended()
    gui.run()
