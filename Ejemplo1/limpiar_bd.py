"""
Script de utilidad para limpiar y gestionar la base de datos Chroma
Permite eliminar documentos específicos o toda la base de datos
"""

import os
import shutil
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_chroma_config, get_ollama_config, get_models_config
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class DatabaseCleaner:
    """Clase para limpiar y gestionar la base de datos Chroma"""
    
    def __init__(self):
        """Inicializa el limpiador de la base de datos"""
        self.config = get_chroma_config()
        self.ollama_config = get_ollama_config()
        self.models_config = get_models_config()
        
        # Inicializar embeddings y cliente Chroma
        self.embeddings = OllamaEmbeddings(
            model=self.models_config["embedding_model"],
            base_url=self.ollama_config["base_url"]
        )
        
        self.chroma_client = Chroma(
            collection_name=self.config["collection_name"],
            embedding_function=self.embeddings,
            persist_directory=self.config["persist_directory"]
        )
    
    def mostrar_estado_actual(self):
        """Muestra el estado actual de la base de datos"""
        print("=" * 60)
        print("📊 ESTADO ACTUAL DE LA BASE DE DATOS")
        print("=" * 60)
        
        try:
            count = self.chroma_client._collection.count()
            print(f"📄 Total de documentos: {count}")
            
            if count > 0:
                results = self.chroma_client.get()
                sources = set()
                for metadata in results['metadatas']:
                    if metadata and 'source' in metadata:
                        sources.add(metadata['source'])
                
                print(f"📁 Fuentes únicas: {len(sources)}")
                for source in sorted(sources):
                    print(f"   - {os.path.basename(source)}")
                    
                return True
            else:
                print("⚠️  La base de datos está vacía")
                return False
                
        except Exception as e:
            print(f"❌ Error al obtener estado: {e}")
            return False
    
    def eliminar_coleccion_completa(self):
        """Elimina toda la colección de la base de datos"""
        print("\n🗑️ ELIMINANDO COLECCIÓN COMPLETA")
        print("=" * 60)
        
        try:
            count = self.chroma_client._collection.count()
            print(f"📄 Documentos a eliminar: {count}")
            
            if count > 0:
                # Eliminar toda la colección
                self.chroma_client.delete_collection()
                print("✅ Colección eliminada completamente")
                print("💡 Ahora puedes ejecutar 'python ejemplo1.py' para vectorizar nuevos documentos")
            else:
                print("ℹ️ La base de datos ya está vacía")
                
        except Exception as e:
            print(f"❌ Error al eliminar colección: {e}")
    
    def eliminar_documentos_por_fuente(self, nombre_archivo):
        """Elimina documentos de una fuente específica"""
        print(f"\n🗑️ ELIMINANDO DOCUMENTOS DE: {nombre_archivo}")
        print("=" * 60)
        
        try:
            results = self.chroma_client.get()
            
            if not results or not results['documents']:
                print("⚠️  No hay documentos para analizar")
                return
            
            # Encontrar documentos de la fuente específica
            documentos_a_eliminar = []
            for i, metadata in enumerate(results['metadatas']):
                if metadata and 'source' in metadata:
                    if nombre_archivo in metadata['source']:
                        documentos_a_eliminar.append(results['ids'][i])
            
            if documentos_a_eliminar:
                print(f"📄 Documentos encontrados: {len(documentos_a_eliminar)}")
                
                # Confirmar eliminación
                confirmacion = input(f"¿Eliminar {len(documentos_a_eliminar)} documentos? (y/n): ").strip().lower()
                
                if confirmacion in ['y', 'yes', 'sí', 'si']:
                    self.chroma_client.delete(ids=documentos_a_eliminar)
                    print(f"✅ {len(documentos_a_eliminar)} documentos eliminados")
                else:
                    print("❌ Operación cancelada")
            else:
                print(f"ℹ️ No se encontraron documentos de '{nombre_archivo}'")
                
        except Exception as e:
            print(f"❌ Error al eliminar documentos: {e}")
    
    def eliminar_directorio_datos(self):
        """Elimina el directorio completo de datos"""
        print("\n🗑️ ELIMINANDO DIRECTORIO DE DATOS")
        print("=" * 60)
        
        try:
            if os.path.exists(self.config["persist_directory"]):
                print(f"📁 Directorio a eliminar: {self.config['persist_directory']}")
                
                # Confirmar eliminación
                confirmacion = input("¿Eliminar directorio completo? (y/n): ").strip().lower()
                
                if confirmacion in ['y', 'yes', 'sí', 'si']:
                    shutil.rmtree(self.config["persist_directory"])
                    print(f"✅ Directorio {self.config['persist_directory']} eliminado")
                    print("💡 Reinicia Chroma con 'docker-compose restart' y ejecuta 'python ejemplo1.py'")
                else:
                    print("❌ Operación cancelada")
            else:
                print(f"ℹ️ El directorio {self.config['persist_directory']} no existe")
                
        except Exception as e:
            print(f"❌ Error al eliminar directorio: {e}")
    
    def hacer_backup(self):
        """Crea un backup de la base de datos"""
        print("\n💾 CREANDO BACKUP")
        print("=" * 60)
        
        try:
            if os.path.exists(self.config["persist_directory"]):
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_chroma_{timestamp}.tar.gz"
                
                print(f"📁 Creando backup: {backup_name}")
                
                # Crear backup
                import tarfile
                with tarfile.open(backup_name, "w:gz") as tar:
                    tar.add(self.config["persist_directory"], arcname="chroma_data")
                
                print(f"✅ Backup creado: {backup_name}")
                
                # Mostrar tamaño
                size = os.path.getsize(backup_name)
                print(f"📏 Tamaño: {size / (1024*1024):.2f} MB")
            else:
                print(f"ℹ️ No hay datos para hacer backup en {self.config['persist_directory']}")
                
        except Exception as e:
            print(f"❌ Error al crear backup: {e}")
    
    def modo_interactivo(self):
        """Modo interactivo para gestionar la base de datos"""
        print("\n" + "=" * 60)
        print("🎮 MODO INTERACTIVO - GESTIÓN DE BASE DE DATOS")
        print("=" * 60)
        print("Comandos disponibles:")
        print("  status - Mostrar estado actual")
        print("  clear-all - Eliminar toda la colección")
        print("  clear-dir - Eliminar directorio de datos")
        print("  clear-source <nombre> - Eliminar documentos por fuente")
        print("  backup - Crear backup")
        print("  quit - Salir")
        print("=" * 60)
        
        while True:
            try:
                command = input("\n🔧 Comando: ").strip().lower()
                
                if command == "quit" or command == "exit":
                    print("👋 ¡Hasta luego!")
                    break
                elif command == "status":
                    self.mostrar_estado_actual()
                elif command == "clear-all":
                    self.eliminar_coleccion_completa()
                elif command == "clear-dir":
                    self.eliminar_directorio_datos()
                elif command == "backup":
                    self.hacer_backup()
                elif command.startswith("clear-source "):
                    nombre = command[13:]  # Remover "clear-source "
                    self.eliminar_documentos_por_fuente(nombre)
                else:
                    print("❌ Comando no reconocido. Usa 'quit' para salir.")
                    
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🗑️ LIMPIADOR DE BASE DE DATOS CHROMA")
    print("=" * 60)
    
    try:
        cleaner = DatabaseCleaner()
        
        # Mostrar estado actual
        cleaner.mostrar_estado_actual()
        
        # Preguntar qué hacer
        print("\n" + "=" * 60)
        print("¿Qué quieres hacer?")
        print("1. Eliminar toda la colección")
        print("2. Eliminar directorio de datos")
        print("3. Eliminar documentos por fuente")
        print("4. Crear backup")
        print("5. Modo interactivo")
        print("6. Salir")
        
        opcion = input("\n🔧 Opción (1-6): ").strip()
        
        if opcion == "1":
            cleaner.eliminar_coleccion_completa()
        elif opcion == "2":
            cleaner.eliminar_directorio_datos()
        elif opcion == "3":
            nombre = input("📁 Nombre del archivo (ej: documento.pdf): ").strip()
            if nombre:
                cleaner.eliminar_documentos_por_fuente(nombre)
            else:
                print("❌ Nombre de archivo requerido")
        elif opcion == "4":
            cleaner.hacer_backup()
        elif opcion == "5":
            cleaner.modo_interactivo()
        elif opcion == "6":
            print("👋 ¡Hasta luego!")
        else:
            print("❌ Opción no válida")
            
    except Exception as e:
        print(f"❌ Error al inicializar el limpiador: {e}")
        print("Verifica que:")
        print("  - Chroma esté ejecutándose en localhost:8000")
        print("  - Ollama esté disponible en 172.16.1.37:11434")
        print("  - Los modelos nomic-embed-text y gpt-oss:20b estén instalados")

if __name__ == "__main__":
    main()
