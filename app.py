from flask import Flask
import win32print
import win32ui
from PIL import Image, ImageWin

app = Flask(__name__)

# Fungsi untuk mencetak teks ke printer thermal
def print_text(printer_name, text):
    try:
        # Membuka printer
        printer = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(printer, 2)

        # Membuat DC untuk printer
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)

        # Menulis dokumen cetak
        hdc.StartDoc("My Thermal Print")
        hdc.StartPage()

        # Menambahkan teks
        hdc.TextOut(100, 100, text)  # Koordinat X, Y dan teks yang akan dicetak 

        # Menyelesaikan pencetakan halaman
        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()

        win32print.ClosePrinter(printer)
    except Exception as e:
        print(f"Error during print: {e}")
        raise

# Route Flask untuk mencetak
@app.route("/", methods=["GET"])
def print_page():
    # Nama printer thermal Anda
    printer_name = "EPSON TM-T88IV Receipt"  # Ganti dengan nama printer thermal Anda

    # Teks yang akan dicetak
    text = "Hello, World! from Flask (Thermal Printer)"

    try:
        # Mencetak teks
        print_text(printer_name, text)
        return "Pencetakan selesai!"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Menjalankan Flask di port 9999
    app.run(debug=True, host="0.0.0.0", port=9999)
