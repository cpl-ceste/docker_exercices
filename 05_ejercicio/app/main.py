from flask import Flask, request
import logging
import sys

# Configuración de logs para que salgan por stdout (Docker logs)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - HONEYPOT ALERT - %(message)s')
logger = logging.getLogger()

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def catch_all(path):
    # Simulamos un error genérico pero registramos todo el intento de acceso
    headers = dict(request.headers)
    body = request.get_data(as_text=True)
    
    log_entry = (
        f"Intento de acceso detectado | "
        f"IP: {request.remote_addr} | "
        f"Metodo: {request.method} | "
        f"Path: /{path} | "
        f"User-Agent: {headers.get('User-Agent', 'Unknown')} | "
        f"Payload: {body}"
    )
    logger.info(log_entry)
    
    # 500 Internal Server Error para confundir al atacante/scanner
    return "Internal Billing System Error - Contact Administrator", 500

if __name__ == '__main__':
    # Ejecutamos en puerto 8080 (no privilegiado)
    app.run(host='0.0.0.0', port=8080)
