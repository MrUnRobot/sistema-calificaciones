#!/usr/bin/env python3
# start_app.py
import os
import sys

# Forzar puerto si no está en entorno
if not os.environ.get('PORT'):
    os.environ['PORT'] = '8080'
    print(f"⚠️  PORT no encontrado en variables de entorno")
    print(f"⚠️  Estableciendo PORT=8080 manualmente")

print(f"🚀 Puerto configurado: {os.environ['PORT']}")
print(f"🔗 MongoDB configurado: {'SÍ' if os.environ.get('MONGO_URI') else 'NO'}")

# Importar y ejecutar app
from app import app

if __name__ == '__main__':
    port = int(os.environ['PORT'])
    print(f"✅ Iniciando en http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
