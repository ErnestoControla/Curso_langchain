"""
Script para visualizar y analizar los índices de la base de datos Chroma
Proporciona información detallada sobre la estructura de índices y su rendimiento
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_ollama_config, get_chroma_config, get_models_config
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

class IndexAnalyzer:
    """Clase para analizar índices de la base de datos Chroma"""
    
    def __init__(self):
        """Inicializa el analizador de índices"""
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
    
    def mostrar_informacion_basica_indices(self):
        """Muestra información básica sobre los índices"""
        print("=" * 60)
        print("🔍 INFORMACIÓN BÁSICA DE ÍNDICES")
        print("=" * 60)
        
        try:
            collection = self.chroma_client._collection
            
            print(f"🏷️  Nombre de la colección: {collection.name}")
            print(f"📁 Directorio de persistencia: {self.config['persist_directory']}")
            
            # Información del cliente
            print(f"\n🔧 Configuración del cliente:")
            print(f"   - Host: {self.config['host']}")
            print(f"   - Puerto: {self.config['port']}")
            print(f"   - Modelo de embeddings: {self.models_config['embedding_model']}")
            
            # Información de la colección
            print(f"\n📊 Información de la colección:")
            count = collection.count()
            print(f"   - Total de documentos: {count}")
            
            if count > 0:
                # Obtener información de metadatos
                results = collection.get()
                if results and results['metadatas']:
                    print(f"   - Documentos con metadatos: {len([m for m in results['metadatas'] if m])}")
                    
                    # Analizar metadatos únicos
                    metadata_keys = set()
                    for metadata in results['metadatas']:
                        if metadata:
                            metadata_keys.update(metadata.keys())
                    
                    print(f"   - Campos de metadatos: {len(metadata_keys)}")
                    for key in sorted(metadata_keys):
                        print(f"      - {key}")
                
                # Información de embeddings
                if results and results['embeddings']:
                    embedding_dim = len(results['embeddings'][0]) if results['embeddings'] else 0
                    print(f"   - Dimensión de embeddings: {embedding_dim}")
                    
        except Exception as e:
            print(f"❌ Error al obtener información básica: {e}")
    
    def analizar_estructura_indices(self):
        """Analiza la estructura detallada de los índices"""
        print("\n" + "=" * 60)
        print("🏗️ ESTRUCTURA DETALLADA DE ÍNDICES")
        print("=" * 60)
        
        try:
            collection = self.chroma_client._collection
            
            # Información del directorio de datos
            persist_dir = Path(self.config["persist_directory"])
            if persist_dir.exists():
                print(f"📁 Archivos en directorio de persistencia:")
                
                # Listar archivos de índices
                index_files = []
                for file_path in persist_dir.rglob("*"):
                    if file_path.is_file():
                        size = file_path.stat().st_size
                        index_files.append((file_path.name, size))
                
                for filename, size in sorted(index_files):
                    size_mb = size / (1024 * 1024)
                    print(f"   - {filename}: {size_mb:.2f} MB")
                
                # Análisis de archivos específicos
                print(f"\n🔍 Análisis de archivos de índices:")
                
                # Buscar archivos específicos de Chroma
                chroma_files = {
                    "parquet": list(persist_dir.glob("*.parquet")),
                    "sqlite": list(persist_dir.glob("*.sqlite*")),
                    "json": list(persist_dir.glob("*.json")),
                    "index": list(persist_dir.glob("*index*"))
                }
                
                for file_type, files in chroma_files.items():
                    if files:
                        print(f"   📄 Archivos {file_type}: {len(files)}")
                        for file in files:
                            size = file.stat().st_size
                            size_mb = size / (1024 * 1024)
                            print(f"      - {file.name}: {size_mb:.2f} MB")
            else:
                print(f"⚠️  El directorio {persist_dir} no existe")
                
        except Exception as e:
            print(f"❌ Error al analizar estructura: {e}")
    
    def analizar_rendimiento_indices(self):
        """Analiza el rendimiento de los índices"""
        print("\n" + "=" * 60)
        print("⚡ ANÁLISIS DE RENDIMIENTO DE ÍNDICES")
        print("=" * 60)
        
        try:
            collection = self.chroma_client._collection
            count = collection.count()
            
            if count == 0:
                print("⚠️  No hay documentos para analizar rendimiento")
                return
            
            print(f"📊 Métricas de rendimiento:")
            print(f"   - Total de documentos indexados: {count}")
            
            # Probar diferentes tipos de consultas
            test_queries = [
                "YOLO",
                "detection", 
                "model",
                "architecture"
            ]
            
            print(f"\n🔍 Pruebas de rendimiento de consultas:")
            
            for query in test_queries:
                import time
                start_time = time.time()
                
                # Realizar consulta
                results = self.chroma_client.similarity_search(query, k=5)
                
                end_time = time.time()
                query_time = (end_time - start_time) * 1000  # en milisegundos
                
                print(f"   - '{query}': {len(results)} resultados en {query_time:.2f}ms")
            
            # Análisis de distribución de documentos
            print(f"\n📈 Análisis de distribución:")
            
            results = collection.get()
            if results and results['metadatas']:
                # Analizar distribución por fuente
                source_distribution = {}
                for metadata in results['metadatas']:
                    if metadata and 'source' in metadata:
                        source = os.path.basename(metadata['source'])
                        source_distribution[source] = source_distribution.get(source, 0) + 1
                
                print(f"   - Distribución por documento:")
                for source, count in sorted(source_distribution.items()):
                    percentage = (count / len(results['metadatas'])) * 100
                    print(f"      - {source}: {count} chunks ({percentage:.1f}%)")
                
                # Analizar distribución por página
                page_distribution = {}
                for metadata in results['metadatas']:
                    if metadata and 'page' in metadata:
                        page = metadata['page']
                        page_distribution[page] = page_distribution.get(page, 0) + 1
                
                if page_distribution:
                    print(f"   - Distribución por página:")
                    for page in sorted(page_distribution.keys()):
                        count = page_distribution[page]
                        percentage = (count / len(results['metadatas'])) * 100
                        print(f"      - Página {page}: {count} chunks ({percentage:.1f}%)")
            
        except Exception as e:
            print(f"❌ Error al analizar rendimiento: {e}")
    
    def mostrar_configuracion_indices(self):
        """Muestra la configuración de índices"""
        print("\n" + "=" * 60)
        print("⚙️ CONFIGURACIÓN DE ÍNDICES")
        print("=" * 60)
        
        try:
            collection = self.chroma_client._collection
            
            print(f"🔧 Configuración actual:")
            print(f"   - Nombre de colección: {collection.name}")
            print(f"   - Modelo de embeddings: {self.models_config['embedding_model']}")
            print(f"   - Dimensión de embeddings: 768 (nomic-embed-text)")
            print(f"   - Tamaño de chunks: {self.config.get('chunk_size', 'N/A')}")
            print(f"   - Solapamiento: {self.config.get('chunk_overlap', 'N/A')}")
            
            # Información sobre el tipo de índice
            print(f"\n🏗️ Tipo de índice:")
            print(f"   - Chroma usa HNSW (Hierarchical Navigable Small World) por defecto")
            print(f"   - Optimizado para búsquedas de similitud de vectores")
            print(f"   - Índice en memoria para consultas rápidas")
            
            # Información sobre persistencia
            print(f"\n💾 Persistencia:")
            print(f"   - Directorio: {self.config['persist_directory']}")
            print(f"   - Formato: Parquet para datos, SQLite para metadatos")
            print(f"   - Índices se reconstruyen automáticamente al cargar")
            
        except Exception as e:
            print(f"❌ Error al mostrar configuración: {e}")
    
    def exportar_informacion_indices(self, filename=None):
        """Exporta información detallada de índices a JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"indices_report_{timestamp}.json"
        
        print(f"\n📤 Exportando información de índices a {filename}...")
        
        try:
            collection = self.chroma_client._collection
            count = collection.count()
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "collection_info": {
                    "name": collection.name,
                    "total_documents": count,
                    "persist_directory": self.config["persist_directory"]
                },
                "embedding_config": {
                    "model": self.models_config["embedding_model"],
                    "dimension": 768,
                    "chunk_size": self.config["chunk_size"],
                    "chunk_overlap": self.config["chunk_overlap"]
                },
                "index_structure": {},
                "performance_metrics": {}
            }
            
            # Información de estructura de índices
            persist_dir = Path(self.config["persist_directory"])
            if persist_dir.exists():
                index_files = []
                for file_path in persist_dir.rglob("*"):
                    if file_path.is_file():
                        size = file_path.stat().st_size
                        index_files.append({
                            "filename": file_path.name,
                            "size_bytes": size,
                            "size_mb": size / (1024 * 1024),
                            "relative_path": str(file_path.relative_to(persist_dir))
                        })
                
                report["index_structure"]["files"] = index_files
                report["index_structure"]["total_files"] = len(index_files)
                report["index_structure"]["total_size_mb"] = sum(f["size_mb"] for f in index_files)
            
            # Métricas de rendimiento
            if count > 0:
                import time
                performance_tests = {}
                
                test_queries = ["YOLO", "detection", "model"]
                for query in test_queries:
                    start_time = time.time()
                    results = self.chroma_client.similarity_search(query, k=5)
                    end_time = time.time()
                    
                    performance_tests[query] = {
                        "query_time_ms": (end_time - start_time) * 1000,
                        "results_count": len(results)
                    }
                
                report["performance_metrics"] = performance_tests
            
            # Guardar reporte
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Información de índices exportada a {filename}")
            
        except Exception as e:
            print(f"❌ Error al exportar información: {e}")
    
    def modo_interactivo(self):
        """Modo interactivo para explorar índices"""
        print("\n" + "=" * 60)
        print("🎮 MODO INTERACTIVO - ANÁLISIS DE ÍNDICES")
        print("=" * 60)
        print("Comandos disponibles:")
        print("  basic - Información básica de índices")
        print("  structure - Estructura detallada de índices")
        print("  performance - Análisis de rendimiento")
        print("  config - Configuración de índices")
        print("  export - Exportar información")
        print("  quit - Salir")
        print("=" * 60)
        
        while True:
            try:
                command = input("\n🔍 Comando: ").strip().lower()
                
                if command == "quit" or command == "exit":
                    print("👋 ¡Hasta luego!")
                    break
                elif command == "basic":
                    self.mostrar_informacion_basica_indices()
                elif command == "structure":
                    self.analizar_estructura_indices()
                elif command == "performance":
                    self.analizar_rendimiento_indices()
                elif command == "config":
                    self.mostrar_configuracion_indices()
                elif command == "export":
                    self.exportar_informacion_indices()
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
    print("🔍 ANALIZADOR DE ÍNDICES DE CHROMA DB")
    print("=" * 60)
    
    try:
        analyzer = IndexAnalyzer()
        
        # Ejecutar análisis automáticos
        analyzer.mostrar_informacion_basica_indices()
        analyzer.analizar_estructura_indices()
        analyzer.analizar_rendimiento_indices()
        analyzer.mostrar_configuracion_indices()
        
        # Preguntar si quiere modo interactivo
        print("\n" + "=" * 60)
        response = input("¿Quieres entrar al modo interactivo? (y/n): ").strip().lower()
        
        if response in ['y', 'yes', 'sí', 'si']:
            analyzer.modo_interactivo()
        else:
            print("✅ Análisis completado")
            
    except Exception as e:
        print(f"❌ Error al inicializar el analizador: {e}")
        print("Verifica que:")
        print("  - Chroma esté ejecutándose en localhost:8000")
        print("  - Ollama esté disponible en 172.16.1.37:11434")
        print("  - Los modelos nomic-embed-text y gpt-oss:20b estén instalados")

if __name__ == "__main__":
    main()
