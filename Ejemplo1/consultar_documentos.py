"""
Script para consultar documentos vectorizados en Chroma
Versión compatible con LangChain 0.3.27
"""

from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Configuración de la base de datos Chroma
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = "documentos_pdf"

def inicializar_chroma():
    """
    Inicializa la conexión con Chroma
    """
    try:
        embeddings = OllamaEmbeddings(model="llama2")
        
        chroma_client = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory="chroma_data"
        )
        
        return chroma_client
    except Exception as e:
        print(f"Error al inicializar Chroma: {e}")
        # Configuración alternativa
        embeddings = OllamaEmbeddings(model="llama2")
        chroma_client = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings
        )
        
        return chroma_client

def consultar_documentos(chroma_client, query, n_results=5):
    """
    Realiza una consulta semántica en la base de datos
    """
    try:
        results = chroma_client.similarity_search(query, k=n_results)
        
        print(f"\nResultados para la consulta: '{query}'")
        print("=" * 50)
        
        for i, doc in enumerate(results, 1):
            print(f"\n--- Documento {i} ---")
            print(f"Contenido: {doc.page_content[:200]}...")
            if hasattr(doc, 'metadata'):
                print(f"Metadatos: {doc.metadata}")
        
        return results
        
    except Exception as e:
        print(f"Error al consultar: {e}")
        return []

def obtener_estadisticas(chroma_client):
    """
    Obtiene estadísticas de la base de datos
    """
    try:
        # Obtener información de la colección
        collection = chroma_client._collection
        count = collection.count()
        
        print(f"\nEstadísticas de la base de datos:")
        print(f"Total de documentos: {count}")
        print(f"Colección: {COLLECTION_NAME}")
        print(f"Host: {CHROMA_HOST}:{CHROMA_PORT}")
        
        return count
        
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return 0

def main():
    """
    Función principal para consultar documentos
    """
    print("=== Consulta de Documentos Vectorizados ===\n")
    
    # Inicializar Chroma
    try:
        chroma_client = inicializar_chroma()
        print("✓ Conexión con Chroma establecida")
    except Exception as e:
        print(f"✗ Error al conectar con Chroma: {e}")
        return
    
    # Obtener estadísticas
    obtener_estadisticas(chroma_client)
    
    # Ejemplos de consultas
    consultas_ejemplo = [
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "neural networks"
    ]
    
    print(f"\nConsultas de ejemplo disponibles:")
    for i, query in enumerate(consultas_ejemplo, 1):
        print(f"{i}. {query}")
    
    # Realizar consultas
    while True:
        print(f"\n" + "="*50)
        query = input("Ingresa tu consulta (o 'salir' para terminar): ").strip()
        
        if query.lower() in ['salir', 'exit', 'quit']:
            break
        
        if query:
            consultar_documentos(chroma_client, query)
        else:
            print("Por favor ingresa una consulta válida")

if __name__ == "__main__":
    main()
