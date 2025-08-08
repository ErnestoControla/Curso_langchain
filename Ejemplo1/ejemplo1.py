""" 
Script para cargar documentos PDF y vectorizarlos en Chroma
Versión compatible con LangChain 0.3.27
"""

import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

# Configuración de la base de datos Chroma
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = "documentos_pdf"

# Configuración para el procesamiento de documentos
CHUNK_SIZE = 1000  # Tamaño de cada chunk en caracteres
CHUNK_OVERLAP = 200  # Solapamiento entre chunks para mantener contexto
DOCUMENTS_PATH = "/home/ernesto/Proyectos_local/Curso_langchain/Ejemplo1/Documentos/"

def cargar_documentos_pdf(ruta_documentos):
    """
    Carga todos los documentos PDF de la ruta especificada
    """
    documentos = []
    ruta = Path(ruta_documentos)
    
    # Buscar todos los archivos PDF
    archivos_pdf = list(ruta.glob("*.pdf"))
    
    print(f"Encontrados {len(archivos_pdf)} archivos PDF:")
    
    for archivo in archivos_pdf:
        try:
            print(f"Procesando: {archivo.name}")
            loader = PyPDFLoader(str(archivo))
            documentos.extend(loader.load())
            print(f"✓ {archivo.name} cargado exitosamente")
        except Exception as e:
            print(f"✗ Error al cargar {archivo.name}: {e}")
    
    return documentos

def dividir_documentos(documentos, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """
    Divide los documentos en chunks más pequeños para mejor procesamiento
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documentos)
    print(f"Documentos divididos en {len(chunks)} chunks")
    return chunks

def inicializar_chroma():
    """
    Inicializa la conexión con Chroma
    """
    try:
        # Usar OllamaEmbeddings para embeddings locales
        embeddings = OllamaEmbeddings(model="llama2")
        
        # Inicializar Chroma con configuración simplificada
        chroma_client = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory="chroma_data"
        )
        
        return chroma_client
    except Exception as e:
        print(f"Error al inicializar Chroma: {e}")
        print("Intentando con configuración alternativa...")
        
        # Configuración alternativa sin persist_directory
        embeddings = OllamaEmbeddings(model="llama2")
        chroma_client = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings
        )
        
        return chroma_client

def vectorizar_documentos(chroma_client, chunks):
    """
    Vectoriza los chunks de documentos en la base de datos
    """
    try:
        # Agregar documentos a la base de datos
        chroma_client.add_documents(chunks)
        print(f"✓ {len(chunks)} chunks vectorizados exitosamente")
        
        # Intentar persistir los cambios (puede no estar disponible en todas las versiones)
        try:
            chroma_client.persist()
            print("✓ Cambios persistidos en la base de datos")
        except:
            print("ℹ Persistencia no disponible en esta versión")
        
    except Exception as e:
        print(f"✗ Error al vectorizar documentos: {e}")

def main():
    """
    Función principal que ejecuta todo el proceso
    """
    print("=== Iniciando proceso de vectorización de documentos PDF ===\n")
    
    # 1. Cargar documentos PDF
    print("1. Cargando documentos PDF...")
    documentos = cargar_documentos_pdf(DOCUMENTS_PATH)
    
    if not documentos:
        print("No se encontraron documentos para procesar")
        return
    
    print(f"✓ {len(documentos)} documentos cargados\n")
    
    # 2. Dividir documentos en chunks
    print("2. Dividiendo documentos en chunks...")
    chunks = dividir_documentos(documentos)
    print(f"✓ {len(chunks)} chunks creados\n")
    
    # 3. Inicializar Chroma
    print("3. Inicializando conexión con Chroma...")
    try:
        chroma_client = inicializar_chroma()
        print("✓ Conexión con Chroma establecida\n")
    except Exception as e:
        print(f"✗ Error al conectar con Chroma: {e}")
        print("Asegúrate de que Chroma esté ejecutándose en el puerto 8000")
        return
    
    # 4. Vectorizar documentos
    print("4. Vectorizando documentos...")
    vectorizar_documentos(chroma_client, chunks)
    
    print("\n=== Proceso completado ===")
    print(f"Documentos vectorizados en la colección: {COLLECTION_NAME}")
    print(f"Base de datos: {CHROMA_HOST}:{CHROMA_PORT}")

if __name__ == "__main__":
    main()