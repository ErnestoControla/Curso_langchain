"""
Archivo de configuración centralizada para el sistema de RAG
Permite cambiar fácilmente modelos y configuraciones
"""

# ============================================================================
# CONFIGURACIÓN DEL SERVIDOR OLLAMA
# ============================================================================
OLLAMA_HOST = "172.16.1.37"
OLLAMA_PORT = 11434
OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

# ============================================================================
# CONFIGURACIÓN DE MODELOS
# ============================================================================

# Modelo para embeddings (vectorización)
EMBEDDING_MODEL = "nomic-embed-text:latest"

# Modelo LLM para generación de respuestas
# Opciones disponibles en el servidor:
# - "gpt-oss:20b" (recomendado - velocidad/calidad)
# - "gpt-oss:120b" (más potente - más lento)
# - "gemma3:12b"
# - "deepseek-r1:latest"
# - "llama3.1:8b"
LLM_MODEL = "gpt-oss:20b"

# ============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================================
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = "documentos_pdf"
PERSIST_DIRECTORY = "chroma_data"

# ============================================================================
# CONFIGURACIÓN DE PROCESAMIENTO DE DOCUMENTOS
# ============================================================================
DOCUMENTS_PATH = "/home/ernesto/Proyectos_local/Curso_langchain/Ejemplo1/Documentos/"

# Configuración de chunks
CHUNK_SIZE = 1000  # Tamaño de cada chunk en caracteres
CHUNK_OVERLAP = 200  # Solapamiento entre chunks

# Separadores para división de texto
TEXT_SEPARATORS = ["\n\n", "\n", " ", ""]

# ============================================================================
# CONFIGURACIÓN DE BÚSQUEDA
# ============================================================================
SEARCH_K = 5  # Número de documentos a recuperar en búsquedas

# ============================================================================
# CONFIGURACIÓN DE PROMPTS
# ============================================================================
DEFAULT_PROMPT_TEMPLATE = """
Basándote en el siguiente contexto, responde la pregunta de manera clara y precisa.
Si la información no está en el contexto, indícalo claramente.

Contexto:
{context}

Pregunta: {question}

Respuesta:"""

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================
DEBUG_MODE = True
LOG_LEVEL = "INFO"

# ============================================================================
# FUNCIONES DE CONFIGURACIÓN
# ============================================================================

def get_ollama_config():
    """Retorna la configuración de Ollama"""
    return {
        "host": OLLAMA_HOST,
        "port": OLLAMA_PORT,
        "base_url": OLLAMA_BASE_URL
    }

def get_chroma_config():
    """Retorna la configuración de Chroma"""
    return {
        "host": CHROMA_HOST,
        "port": CHROMA_PORT,
        "collection_name": COLLECTION_NAME,
        "persist_directory": PERSIST_DIRECTORY
    }

def get_models_config():
    """Retorna la configuración de modelos"""
    return {
        "embedding_model": EMBEDDING_MODEL,
        "llm_model": LLM_MODEL
    }

def get_processing_config():
    """Retorna la configuración de procesamiento"""
    return {
        "documents_path": DOCUMENTS_PATH,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "text_separators": TEXT_SEPARATORS
    }

def change_llm_model(new_model):
    """Cambia el modelo LLM"""
    global LLM_MODEL
    LLM_MODEL = new_model
    print(f"✅ Modelo LLM cambiado a: {LLM_MODEL}")

def change_embedding_model(new_model):
    """Cambia el modelo de embeddings"""
    global EMBEDDING_MODEL
    EMBEDDING_MODEL = new_model
    print(f"✅ Modelo de embeddings cambiado a: {EMBEDDING_MODEL}")

def print_config():
    """Imprime la configuración actual"""
    print("=" * 50)
    print("CONFIGURACIÓN ACTUAL DEL SISTEMA")
    print("=" * 50)
    print(f"Servidor Ollama: {OLLAMA_BASE_URL}")
    print(f"Modelo Embeddings: {EMBEDDING_MODEL}")
    print(f"Modelo LLM: {LLM_MODEL}")
    print(f"Base de datos: {CHROMA_HOST}:{CHROMA_PORT}")
    print(f"Colección: {COLLECTION_NAME}")
    print(f"Chunk Size: {CHUNK_SIZE}")
    print(f"Chunk Overlap: {CHUNK_OVERLAP}")
    print("=" * 50)

# ============================================================================
# CONFIGURACIONES PREDEFINIDAS
# ============================================================================

# Configuración para documentos técnicos
TECHNICAL_CONFIG = {
    "chunk_size": 1500,
    "chunk_overlap": 300,
    "llm_model": "gpt-oss:20b"
}

# Configuración para documentos narrativos
NARRATIVE_CONFIG = {
    "chunk_size": 800,
    "chunk_overlap": 150,
    "llm_model": "gpt-oss:20b"
}

# Configuración para documentos legales
LEGAL_CONFIG = {
    "chunk_size": 2000,
    "chunk_overlap": 500,
    "llm_model": "gpt-oss:120b"
}

def apply_preset_config(config_name):
    """Aplica una configuración predefinida"""
    global CHUNK_SIZE, CHUNK_OVERLAP, LLM_MODEL
    
    if config_name == "technical":
        config = TECHNICAL_CONFIG
    elif config_name == "narrative":
        config = NARRATIVE_CONFIG
    elif config_name == "legal":
        config = LEGAL_CONFIG
    else:
        print(f"❌ Configuración '{config_name}' no encontrada")
        return
    
    CHUNK_SIZE = config["chunk_size"]
    CHUNK_OVERLAP = config["chunk_overlap"]
    LLM_MODEL = config["llm_model"]
    
    print(f"✅ Configuración '{config_name}' aplicada:")
    print(f"   - Chunk Size: {CHUNK_SIZE}")
    print(f"   - Chunk Overlap: {CHUNK_OVERLAP}")
    print(f"   - LLM Model: {LLM_MODEL}")
