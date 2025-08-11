"""
Script para monitorear y verificar el estado de la base de datos Chroma
Permite verificar el estado, contenido y realizar consultas de diagnóstico
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_ollama_config, get_chroma_config, get_models_config
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class DatabaseMonitor:
    """Clase para monitorear el estado de la base de datos Chroma"""
    
    def __init__(self):
        """Inicializa el monitor de la base de datos"""
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
    
    def get_basic_stats(self):
        """Obtiene estadísticas básicas de la base de datos"""
        print("=" * 60)
        print("📊 ESTADÍSTICAS BÁSICAS DE LA BASE DE DATOS")
        print("=" * 60)
        
        try:
            # Obtener conteo de documentos
            count = self.chroma_client._collection.count()
            print(f"📄 Total de documentos: {count}")
            
            # Obtener metadatos de la colección
            collection = self.chroma_client._collection
            print(f"🏷️  Nombre de la colección: {collection.name}")
            print(f"📁 Directorio de persistencia: {self.config['persist_directory']}")
            
            # Verificar si hay documentos
            if count > 0:
                # Obtener algunos documentos de muestra
                results = self.chroma_client.get()
                if results and results['documents']:
                    print(f"📝 Primer documento (primeros 100 chars):")
                    print(f"   {results['documents'][0][:100]}...")
                    
                    # Mostrar metadatos del primer documento
                    if results['metadatas'] and results['metadatas'][0]:
                        print(f"🏷️  Metadatos del primer documento:")
                        for key, value in results['metadatas'][0].items():
                            print(f"   {key}: {value}")
                
                return True
            else:
                print("⚠️  La base de datos está vacía")
                return False
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return False
    
    def get_detailed_stats(self):
        """Obtiene estadísticas detalladas de la base de datos"""
        print("\n" + "=" * 60)
        print("🔍 ESTADÍSTICAS DETALLADAS")
        print("=" * 60)
        
        try:
            results = self.chroma_client.get()
            
            if not results or not results['documents']:
                print("⚠️  No hay documentos para analizar")
                return
            
            documents = results['documents']
            metadatas = results['metadatas'] or []
            ids = results['ids']
            
            print(f"📊 Análisis de {len(documents)} documentos:")
            
            # Estadísticas de longitud de documentos
            lengths = [len(doc) for doc in documents]
            avg_length = sum(lengths) / len(lengths)
            min_length = min(lengths)
            max_length = max(lengths)
            
            print(f"   📏 Longitud promedio: {avg_length:.1f} caracteres")
            print(f"   📏 Longitud mínima: {min_length} caracteres")
            print(f"   📏 Longitud máxima: {max_length} caracteres")
            
            # Análisis de metadatos
            if metadatas:
                print(f"\n🏷️  Análisis de metadatos:")
                
                # Contar fuentes únicas
                sources = set()
                for metadata in metadatas:
                    if metadata and 'source' in metadata:
                        sources.add(metadata['source'])
                
                print(f"   📁 Fuentes únicas: {len(sources)}")
                for source in sorted(sources):
                    print(f"      - {source}")
                
                # Contar páginas únicas
                pages = set()
                for metadata in metadatas:
                    if metadata and 'page' in metadata:
                        pages.add(metadata['page'])
                
                print(f"   📄 Páginas únicas: {len(pages)}")
                
                # Análisis de chunks por documento
                doc_chunks = {}
                for metadata in metadatas:
                    if metadata and 'source' in metadata:
                        source = metadata['source']
                        if source not in doc_chunks:
                            doc_chunks[source] = 0
                        doc_chunks[source] += 1
                
                print(f"\n📊 Chunks por documento:")
                for source, count in sorted(doc_chunks.items()):
                    print(f"   {source}: {count} chunks")
            
        except Exception as e:
            print(f"❌ Error al obtener estadísticas detalladas: {e}")
    
    def search_sample_queries(self):
        """Realiza búsquedas de muestra para verificar funcionamiento"""
        print("\n" + "=" * 60)
        print("🔍 PRUEBAS DE BÚSQUEDA")
        print("=" * 60)
        
        # Queries de prueba
        test_queries = [
            "YOLO",
            "detection",
            "model",
            "architecture",
            "performance",
            "training",
            "dataset"
        ]
        
        for query in test_queries:
            try:
                print(f"\n🔍 Búsqueda: '{query}'")
                results = self.chroma_client.similarity_search(query, k=2)
                
                if results:
                    for i, doc in enumerate(results, 1):
                        print(f"   Resultado {i}:")
                        print(f"      📝 {doc.page_content[:150]}...")
                        if hasattr(doc, 'metadata') and doc.metadata:
                            print(f"      🏷️  {doc.metadata}")
                else:
                    print(f"   ⚠️  No se encontraron resultados")
                    
            except Exception as e:
                print(f"   ❌ Error en búsqueda: {e}")
    
    def check_database_health(self):
        """Verifica la salud general de la base de datos"""
        print("\n" + "=" * 60)
        print("🏥 VERIFICACIÓN DE SALUD DE LA BASE DE DATOS")
        print("=" * 60)
        
        health_status = {
            "connection": False,
            "collection_exists": False,
            "has_documents": False,
            "embeddings_working": False,
            "search_working": False
        }
        
        # Verificar conexión
        try:
            count = self.chroma_client._collection.count()
            health_status["connection"] = True
            health_status["collection_exists"] = True
            health_status["has_documents"] = count > 0
            print(f"✅ Conexión a Chroma: OK")
            print(f"✅ Colección existe: OK")
            print(f"✅ Documentos presentes: {'SÍ' if count > 0 else 'NO'}")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
        
        # Verificar embeddings
        try:
            test_text = "test"
            vectors = self.embeddings.embed_query(test_text)
            if len(vectors) > 0:
                health_status["embeddings_working"] = True
                print(f"✅ Embeddings funcionando: OK ({len(vectors)} dimensiones)")
            else:
                print(f"❌ Embeddings no generaron vectores")
        except Exception as e:
            print(f"❌ Error en embeddings: {e}")
        
        # Verificar búsqueda
        if health_status["has_documents"]:
            try:
                results = self.chroma_client.similarity_search("test", k=1)
                if results:
                    health_status["search_working"] = True
                    print(f"✅ Búsqueda funcionando: OK")
                else:
                    print(f"⚠️  Búsqueda no retornó resultados")
            except Exception as e:
                print(f"❌ Error en búsqueda: {e}")
        else:
            print(f"⚠️  Búsqueda no probada (sin documentos)")
        
        # Resumen de salud
        print(f"\n📊 Estado general: {sum(health_status.values())}/{len(health_status)} OK")
        
        if all(health_status.values()):
            print("🎉 Base de datos en excelente estado")
        elif health_status["connection"] and health_status["collection_exists"]:
            print("⚠️  Base de datos funcional con algunos problemas menores")
        else:
            print("❌ Base de datos con problemas críticos")
        
        return health_status
    
    def export_database_info(self, filename=None):
        """Exporta información de la base de datos a un archivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"database_report_{timestamp}.json"
        
        print(f"\n📤 Exportando información a {filename}...")
        
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "config": {
                    "chroma": self.config,
                    "ollama": self.ollama_config,
                    "models": self.models_config
                },
                "stats": {},
                "health": {}
            }
            
            # Obtener estadísticas básicas
            count = self.chroma_client._collection.count()
            report["stats"]["total_documents"] = count
            
            if count > 0:
                results = self.chroma_client.get()
                documents = results['documents']
                metadatas = results['metadatas'] or []
                
                # Estadísticas de documentos
                lengths = [len(doc) for doc in documents]
                report["stats"]["avg_length"] = sum(lengths) / len(lengths)
                report["stats"]["min_length"] = min(lengths)
                report["stats"]["max_length"] = max(lengths)
                
                # Análisis de metadatos
                sources = set()
                pages = set()
                for metadata in metadatas:
                    if metadata and 'source' in metadata:
                        sources.add(metadata['source'])
                    if metadata and 'page' in metadata:
                        pages.add(metadata['page'])
                
                report["stats"]["unique_sources"] = list(sources)
                report["stats"]["unique_pages"] = len(pages)
            
            # Estado de salud
            report["health"] = self.check_database_health()
            
            # Guardar archivo
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Información exportada exitosamente a {filename}")
            
        except Exception as e:
            print(f"❌ Error al exportar información: {e}")
    
    def interactive_mode(self):
        """Modo interactivo para explorar la base de datos"""
        print("\n" + "=" * 60)
        print("🎮 MODO INTERACTIVO")
        print("=" * 60)
        print("Comandos disponibles:")
        print("  stats - Estadísticas básicas")
        print("  detailed - Estadísticas detalladas")
        print("  search <query> - Buscar documentos")
        print("  health - Verificar salud de la BD")
        print("  export - Exportar información")
        print("  quit - Salir")
        print("=" * 60)
        
        while True:
            try:
                command = input("\n🔍 Comando: ").strip().lower()
                
                if command == "quit" or command == "exit":
                    print("👋 ¡Hasta luego!")
                    break
                elif command == "stats":
                    self.get_basic_stats()
                elif command == "detailed":
                    self.get_detailed_stats()
                elif command == "health":
                    self.check_database_health()
                elif command == "export":
                    self.export_database_info()
                elif command.startswith("search "):
                    query = command[7:]  # Remover "search "
                    print(f"\n🔍 Búsqueda: '{query}'")
                    results = self.chroma_client.similarity_search(query, k=3)
                    for i, doc in enumerate(results, 1):
                        print(f"\nResultado {i}:")
                        print(f"📝 {doc.page_content[:200]}...")
                        if hasattr(doc, 'metadata') and doc.metadata:
                            print(f"🏷️  {doc.metadata}")
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
    print("🗄️  MONITOR DE BASE DE DATOS CHROMA")
    print("=" * 60)
    
    try:
        monitor = DatabaseMonitor()
        
        # Ejecutar verificaciones automáticas
        monitor.get_basic_stats()
        monitor.get_detailed_stats()
        monitor.search_sample_queries()
        monitor.check_database_health()
        
        # Preguntar si quiere modo interactivo
        print("\n" + "=" * 60)
        response = input("¿Quieres entrar al modo interactivo? (y/n): ").strip().lower()
        
        if response in ['y', 'yes', 'sí', 'si']:
            monitor.interactive_mode()
        else:
            print("✅ Verificación completada")
            
    except Exception as e:
        print(f"❌ Error al inicializar el monitor: {e}")
        print("Verifica que:")
        print("  - Chroma esté ejecutándose en localhost:8000")
        print("  - Ollama esté disponible en 172.16.1.37:11434")
        print("  - Los modelos nomic-embed-text y gpt-oss:20b estén instalados")

if __name__ == "__main__":
    main()
