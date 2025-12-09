from pymongo import MongoClient
import os
from urllib.parse import quote_plus
import time

def conectar_mongodb():
    max_retries = 3
    retry_delay = 2  # segundos
    
    for attempt in range(max_retries):
        try:
            print(f"🔗 Intentando conectar a MongoDB (intento {attempt + 1}/{max_retries})...")
            
            # OPCIÓN 1: Variable de entorno
            mongo_uri = os.environ.get('MONGO_URI')
            
            if not mongo_uri:
                # OPCIÓN 2: Construir manualmente
                username = os.environ.get('MONGO_USER', 'admin_sistema')
                password = os.environ.get('MONGO_PASS', '')
                cluster = os.environ.get('MONGO_CLUSTER', '')
                
                if not all([username, password, cluster]):
                    print("❌ Faltan variables de entorno para MongoDB")
                    return None
                
                encoded_username = quote_plus(username)
                encoded_password = quote_plus(password)
                mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster}/sistema_calificaciones?retryWrites=true&w=majority"
            
            print(f"📡 URI: mongodb+srv://{mongo_uri.split('@')[0].split('://')[1][:10]}...@{mongo_uri.split('@')[1].split('/')[0]}")
            
            # Conectar con timeout
            cliente = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=10000,  # 10 segundos
                connectTimeoutMS=10000,
                socketTimeoutMS=30000
            )
            
            # Probar conexión
            cliente.server_info()
            db = cliente['sistema_calificaciones']
            
            # Probar lectura básica
            db.maestros.count_documents({})
            
            print("✅ Conexión exitosa a MongoDB Atlas")
            return db
            
        except Exception as e:
            print(f"❌ Error en intento {attempt + 1}: {str(e)[:100]}")
            if attempt < max_retries - 1:
                print(f"⏳ Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                print("❌ Máximo de intentos alcanzado")
                return None
