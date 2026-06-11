import os
import base64
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

# Asegurar que la carpeta para guardar las capturas existe
CARPETA_CAPTURAS = os.path.join(os.getcwd(), 'capturas')
if not os.path.exists(CARPETA_CAPTURAS):
    os.makedirs(CARPETA_CAPTURAS)

@app.route('/')
def index():
    # Renderiza la página web del laboratorio
    return render_template('laboratorio.html')

@app.route('/guardar_captura', methods=['POST'])
def guardar_captura():
    try:
        # Obtener los datos JSON enviados por el navegador
        datos = request.get_json()
        imagen_b64 = datos.get('imagen') # Viene como "data:image/jpeg;base64,..."

        if imagen_b64:
            # Limpiar la cabecera del formato Base64
            encabezado, contenido_b64 = imagen_b64.split(',')[1], imagen_b64.split(',')[1]
            
            # Decodificar los datos binarios de la imagen
            datos_imagen = base64.b64decode(contenido_b64)
            
            # Generar un nombre único basado en la fecha y hora actual
            nombre_archivo = f"captura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            ruta_completa = os.path.join(CARPETA_CAPTURAS, nombre_archivo)
            
            # Guardar el archivo en el disco del servidor
            with open(ruta_completa, 'wb') as f:
                f.write(datos_imagen)
                
            print(f"[+] Nueva captura almacenada en el servidor: {nombre_archivo}")
            return jsonify({"status": "success", "message": "Imagen guardada"}), 200
            
        return jsonify({"status": "error", "message": "No se recibieron datos de imagen"}), 400
    except Exception as e:
        print(f"[-] Error al guardar la captura: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Lanzamos en el puerto 80. Admite conexiones desde cualquier IP (0.0.0.0)
    # NOTA: En Windows ejecutar como Administrador, en Linux usar 'sudo python3 app.py'
    app.run(host='0.0.0.0', port=80, debug=True)
