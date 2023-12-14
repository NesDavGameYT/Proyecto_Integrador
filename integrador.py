import tkinter as tk
import mysql.connector
from tkinter import messagebox
from fpdf import FPDF
from PIL import Image, ImageTk
from PIL import Image, ImageDraw
import qrcode
import os

os.system("cls")

def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="NestorDavid",
        database="interphones"
    )

def crear_pdf_invitado(nombre, apellido_paterno, apellido_materno, departamento, correo):
    # Crear el código QR con la URL de Google
    url_google = "'https://www.google.com'"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_google)
    qr.make(fit=True)

    # Crear imagen PIL del código QR
    img_qr = qr.make_image(fill_color="black", back_color="white")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Configurar la posición de la primera imagen (izquierda)
    pdf.image("logo_tessfp.jpeg", x=10, y=8, w=40)
    # Configurar la posición de la segunda imagen (derecha)
    pdf.image("TecLogo.png", x=160, y=8, w=40)

    # Agregar información al PDF
    pdf.cell(200, 10, txt="Invitado", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"Apellido Paterno: {apellido_paterno}", ln=True)
    pdf.cell(200, 10, txt=f"Apellido Materno: {apellido_materno}", ln=True)
    pdf.cell(200, 10, txt=f"Departamento: {departamento}", ln=True)
    pdf.cell(200, 10, txt=f"Correo Electrónico: {correo}", ln=True)

    # Crear la carpeta "pdfs" si no existe
    pdf_folder = "pdfs"
    os.makedirs(pdf_folder, exist_ok=True)

    # Guardar el PDF en la carpeta "pdfs"
    pdf_path = os.path.join(pdf_folder, f"{nombre}_invitado.pdf")
    pdf.output(pdf_path)

    # Guardar la imagen del código QR en la carpeta "pdfs"
    img_qr_path = os.path.join(pdf_folder, f"{nombre}_qr.png")
    img_qr.save(img_qr_path)

    messagebox.showinfo("Éxito", f"Invitado ingresado correctamente. PDF creado: {pdf_path}\nCódigo QR creado: {img_qr_path}")
    
def ingresar_residente():
    # Lógica para el formulario de residentes
    formulario_residente = tk.Toplevel(ventana)
    formulario_residente.title("Ingresar Residente")
    formulario_residente.geometry("250x250")
    formulario_residente.configure(bg="#e6f7ff")

    # Campos de entrada
    nombre_label = tk.Label(formulario_residente, text="Nombre:", bg="#e6f7ff")
    nombre_label.pack()

    nombre_entry = tk.Entry(formulario_residente)
    nombre_entry.pack()

    apellido_paterno_label = tk.Label(formulario_residente, text="Apellido Paterno:", bg="#e6f7ff")
    apellido_paterno_label.pack()

    apellido_paterno_entry = tk.Entry(formulario_residente)
    apellido_paterno_entry.pack()

    apellido_materno_label = tk.Label(formulario_residente, text="Apellido Materno:", bg="#e6f7ff")
    apellido_materno_label.pack()

    apellido_materno_entry = tk.Entry(formulario_residente)
    apellido_materno_entry.pack()

    departamento_label = tk.Label(formulario_residente, text="Departamento:", bg="#e6f7ff")
    departamento_label.pack()

    departamento_entry = tk.Entry(formulario_residente)
    departamento_entry.pack()

    # Botón para guardar en la base de datos
    guardar_button = tk.Button(
        formulario_residente, text="Guardar",
        command=lambda: guardar_residente(
            nombre_entry.get(),
            apellido_paterno_entry.get(),
            apellido_materno_entry.get(),
            departamento_entry.get(),
            formulario_residente
        )
    )
    guardar_button.pack()

def guardar_residente(nombre, apellido_paterno, apellido_materno, departamento, formulario):
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="NestorDavid",
            database="interphones"
        )

        # Crear un cursor
        cursor = conexion.cursor()

        # Verificar si el residente ya existe
        consulta_verificar = "SELECT * FROM residentes WHERE nombre = %s"
        cursor.execute(consulta_verificar, (nombre,))
        residente_existente = cursor.fetchone()

        if residente_existente:
            # Si el residente ya existe, actualiza el contador
            consulta_actualizar = "UPDATE residentes SET contador = contador + 1 WHERE nombre = %s"
            cursor.execute(consulta_actualizar, (nombre,))
        else:
            # Si el residente no existe, inserta uno nuevo
            consulta_insertar = "INSERT INTO residentes (nombre, apellido_paterno, apellido_materno, numero_departamento, contador) VALUES (%s, %s, %s, %s, 1)"
            datos = (nombre, apellido_paterno, apellido_materno, departamento)
            cursor.execute(consulta_insertar, datos)

        # Confirmar la transacción
        conexion.commit()

        # Cerrar la conexión y destruir el formulario
        cursor.close()
        conexion.close()
        formulario.destroy()

        messagebox.showinfo("Éxito", "Residente ingresado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al ingresar el residente: {e}")


def ingresar_invitado():
    # Lógica para el formulario de invitados
    formulario_invitado = tk.Toplevel(ventana)
    formulario_invitado.title("Ingresar Invitado")
    formulario_invitado.geometry("250x250")
    formulario_invitado.configure(bg="#e6f7ff")

    # Campos de entrada
    nombre_label = tk.Label(formulario_invitado, text="Nombre:", bg="#e6f7ff")
    nombre_label.pack()

    nombre_entry = tk.Entry(formulario_invitado)
    nombre_entry.pack()

    apellido_paterno_label = tk.Label(formulario_invitado, text="Apellido Paterno:", bg="#e6f7ff")
    apellido_paterno_label.pack()

    apellido_paterno_entry = tk.Entry(formulario_invitado)
    apellido_paterno_entry.pack()

    apellido_materno_label = tk.Label(formulario_invitado, text="Apellido Materno:", bg="#e6f7ff")
    apellido_materno_label.pack()

    apellido_materno_entry = tk.Entry(formulario_invitado)
    apellido_materno_entry.pack()
    
    departamento_label = tk.Label(formulario_invitado, text="Departamento:", bg="#e6f7ff")
    departamento_label.pack()

    departamento_entry = tk.Entry(formulario_invitado)
    departamento_entry.pack()

    correo_label = tk.Label(formulario_invitado, text="Correo Electrónico:", bg="#e6f7ff")
    correo_label.pack()

    correo_entry = tk.Entry(formulario_invitado)
    correo_entry.pack()

    # Botón para guardar en la base de datos
    guardar_button = tk.Button(
        formulario_invitado, text="Guardar",
        command=lambda: guardar_invitado(
            nombre_entry.get(),
            apellido_paterno_entry.get(),
            apellido_materno_entry.get(),
            departamento_entry.get(),
            correo_entry.get(),
            formulario_invitado
        )
    )
    guardar_button.pack()

def guardar_invitado(nombre, apellido_paterno, apellido_materno, departamento, correo, formulario):
    try:
        connection = conectar_base_datos()
        cursor = connection.cursor()

        consulta = "INSERT INTO invitados (nombre, apellido_paterno, apellido_materno, numero_departamento, correo_electronico) VALUES (%s, %s, %s, %s, %s)"
        datos = (nombre, apellido_paterno, apellido_materno, departamento, correo)
        cursor.execute(consulta, datos)

        connection.commit()

        cursor.close()
        connection.close()
        formulario.destroy()

        # Llamar a la función para crear el PDF
        crear_pdf_invitado(nombre, apellido_paterno, apellido_materno, departamento, correo)
    except Exception as e:
        messagebox.showerror("Error", f"Error al ingresar el invitado: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Bienvenido")

# Configurar tamaño y color de fondo
ventana.geometry("250x250")  # Ajusta el tamaño según tus necesidades
ventana.configure(bg="#e6f7ff")  # Color de fondo azul suave

# Espaciador superior
espaciador_superior = tk.Label(ventana, text="", height=2, bg="#e6f7ff")
espaciador_superior.pack()

# Etiqueta de bienvenida
bienvenida_label = tk.Label(ventana, text="¡Bienvenido!", bg="#e6f7ff")
bienvenida_label.pack()

# Espaciador entre la etiqueta y los botones
espaciador_medio = tk.Label(ventana, text="", height=1, bg="#e6f7ff")
espaciador_medio.pack()

# Botón para ingresar como residente
residente_button = tk.Button(ventana, text="Ingresar como Residente", command=ingresar_residente)
residente_button.pack()

# Espaciador entre los botones
espaciador_entre_botones = tk.Label(ventana, text="", height=1, bg="#e6f7ff")
espaciador_entre_botones.pack()

# Botón para ingresar como invitado
invitado_button = tk.Button(ventana, text="Ingresar como Invitado", command=ingresar_invitado)
invitado_button.pack()

# Espaciador inferior
espaciador_inferior = tk.Label(ventana, text="", height=2, bg="#e6f7ff")
espaciador_inferior.pack()

# Iniciar el bucle principal
ventana.mainloop()
