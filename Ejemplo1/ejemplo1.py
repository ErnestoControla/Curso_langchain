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
from langchain_ollama import OllamaEmbeddings

# Configuración de la base de datos Chroma
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = "documentos_pdf"

# Configuración para el procesamiento de documentos
CHUNK_SIZE = 1000  # Tamaño de cada chunk en caracteres
CHUNK_OVERLAP = 200  # Solapamiento entre chunks para mantener contexto
DOCUMENTS_PATH = "/home/ernesto/Proyectos_local/Curso_langchain/Ejemplo1/Documentos/"

# Configuración de Ollama
OLLAMA_HOST = "172.16.1.37"
OLLAMA_PORT = 11434
OLLAMA_MODEL = "nomic-embed-text:latest"  # Modelo específico para embeddings

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

def analizar_tipo_contenido(texto):
    """
    Analiza el tipo de contenido del documento para optimizar separadores
    """
    texto_lower = texto.lower()
    
    # Detectar tipo de documento
    tipo_documento = "general"
    
    # Detectar papers académicos
    if any(palabra in texto_lower for palabra in ["abstract", "introduction", "methodology", "conclusion", "references"]):
        tipo_documento = "academico"
    
    # Detectar documentos técnicos con código
    if any(palabra in texto_lower for palabra in ["def ", "class ", "import ", "function", "algorithm"]):
        tipo_documento = "tecnico"
    
    # Detectar documentos con tablas
    if "|" in texto or "\t" in texto:
        tipo_documento = "tabular"
    
    # Detectar documentos con listas
    if any(palabra in texto for palabra in ["•", "- ", "* ", "1. ", "2. "]):
        tipo_documento = "lista"
    
    return tipo_documento

def obtener_separadores_optimizados(tipo_documento):
    """
    Retorna separadores optimizados según el tipo de documento
    """
    separadores_base = [
        # Separadores de estructura principal
        "\n\n",      # Párrafos (doble salto de línea)
        "\n",        # Líneas (salto de línea simple)
        " ",         # Espacios entre palabras
        ""           # Caracteres individuales (último recurso)
    ]
    
    separadores_especificos = {
        "academico": [
            "Abstract",
            "Introduction",
            "Methodology",
            "Results",
            "Conclusion",
            "References",
            "## ",
            "### ",
            "#### ",
            "1. ",
            "2. ",
            "3. ",
            "4. ",
            "5. ",
            "6. ",
            "7. ",
            "8. ",
            "9. ",
            "10. ",
            "•",
            "- ",
            "* "
        ],
        "tecnico": [
            "```",
            "```\n",
            "{",
            "}",
            "(",
            ")",
            ";",
            "def ",
            "class ",
            "import ",
            "function",
            "algorithm",
            "1. ",
            "2. ",
            "3. ",
            "4. ",
            "5. ",
            "•",
            "- ",
            "* "
        ],
        "tabular": [
            "|",
            "\t",
            ";",
            ",",
            "1. ",
            "2. ",
            "3. ",
            "4. ",
            "5. ",
            "•",
            "- ",
            "* "
        ],
        "lista": [
            "1. ",
            "2. ",
            "3. ",
            "4. ",
            "5. ",
            "6. ",
            "7. ",
            "8. ",
            "9. ",
            "10. ",
            "•",
            "- ",
            "* "
        ],
        "general": [
            "1. ",
            "2. ",
            "3. ",
            "4. ",
            "5. ",
            "•",
            "- ",
            "* ",
            "## ",
            "### ",
            "#### "
        ]
    }
    
    # Combinar separadores base con específicos
    separadores = separadores_especificos.get(tipo_documento, separadores_especificos["general"]) + separadores_base
    return separadores

def dividir_documentos(documentos, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """
    Divide los documentos en chunks más pequeños para mejor procesamiento
    Utiliza separadores específicos para diferentes tipos de contenido
    """
    chunks_totales = []
    
    for documento in documentos:
        # Analizar tipo de contenido
        tipo_contenido = analizar_tipo_contenido(documento.page_content)
        separadores = obtener_separadores_optimizados(tipo_contenido)
        
        print(f"📄 Tipo de documento detectado: {tipo_contenido}")
        print(f"   - Separadores aplicados: {len(separadores)}")
        
        # Crear text splitter optimizado para este documento
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=separadores
        )
        
        # Dividir este documento específico
        chunks_documento = text_splitter.split_documents([documento])
        chunks_totales.extend(chunks_documento)
        
        print(f"   - Chunks generados: {len(chunks_documento)}")
    
    print(f"\n📊 Total de chunks generados: {len(chunks_totales)}")
    return chunks_totales

def inicializar_chroma():
    """
    Inicializa la conexión con Chroma
    """
    try:
        # Usar OllamaEmbeddings con el modelo nomic-embed-text
        embeddings = OllamaEmbeddings(
            model=OLLAMA_MODEL,
            base_url=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
        )
        
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
        embeddings = OllamaEmbeddings(
            model=OLLAMA_MODEL,
            base_url=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
        )
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
    print(f"Configuración:")
    print(f"- Modelo Ollama: {OLLAMA_MODEL}")
    print(f"- Host Ollama: {OLLAMA_HOST}:{OLLAMA_PORT}")
    print(f"- Base de datos: {CHROMA_HOST}:{CHROMA_PORT}")
    print(f"- Tamaño de chunks: {CHUNK_SIZE}")
    print(f"- Solapamiento: {CHUNK_OVERLAP}\n")
    
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
    print(f"Modelo utilizado: {OLLAMA_MODEL}")

if __name__ == "__main__":
    main()