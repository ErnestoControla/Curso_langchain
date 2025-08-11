"""
Script para consultar documentos usando un LLM para generar respuestas
Combina embeddings para búsqueda + LLM para generación de respuestas
"""

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Configuración de la base de datos Chroma
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = "documentos_pdf"

# Configuración de Ollama
OLLAMA_HOST = "172.16.1.37"
OLLAMA_PORT = 11434
EMBEDDING_MODEL = "nomic-embed-text:latest"  # Para embeddings
LLM_MODEL = "gpt-oss:20b"  # Para generación de respuestas

def inicializar_sistema():
    """
    Inicializa el sistema con embeddings y LLM
    """
    try:
        # 1. Embeddings para búsqueda semántica
        embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
        )
        
        # 2. Base de datos vectorial
        chroma_client = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory="chroma_data"
        )
        
        # 3. LLM para generación de respuestas
        llm = Ollama(
            model=LLM_MODEL,
            base_url=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
        )
        
        # 4. Prompt template para respuestas estructuradas
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            Basándote en el siguiente contexto, responde la pregunta de manera clara y precisa.
            Si la información no está en el contexto, indícalo claramente.
            
            Contexto:
            {context}
            
            Pregunta: {question}
            
            Respuesta:"""
        )
        
        # 5. Chain que combina búsqueda + generación
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=chroma_client.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": prompt_template}
        )
        
        return qa_chain, chroma_client
        
    except Exception as e:
        print(f"Error al inicializar el sistema: {e}")
        return None, None

def consultar_con_llm(qa_chain, query):
    """
    Realiza una consulta usando el LLM para generar respuestas
    """
    try:
        print(f"\n🤖 Generando respuesta para: '{query}'")
        print("=" * 60)
        
        # Obtener respuesta del LLM
        response = qa_chain.invoke({"query": query})
        
        print(f"📝 Respuesta generada:")
        print(response["result"])
        
        return response["result"]
        
    except Exception as e:
        print(f"Error al consultar: {e}")
        return None

def obtener_estadisticas(chroma_client):
    """
    Obtiene estadísticas de la base de datos
    """
    try:
        collection = chroma_client._collection
        count = collection.count()
        
        print(f"\n📊 Estadísticas del sistema:")
        print(f"• Documentos en BD: {count}")
        print(f"• Modelo de embeddings: {EMBEDDING_MODEL}")
        print(f"• Modelo LLM: {LLM_MODEL}")
        print(f"• Servidor: {OLLAMA_HOST}:{OLLAMA_PORT}")
        
        return count
        
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return 0

def main():
    """
    Función principal
    """
    print("=== Sistema de Consulta con LLM ===")
    print("Combina embeddings para búsqueda + LLM para respuestas\n")
    
    # Inicializar sistema
    qa_chain, chroma_client = inicializar_sistema()
    
    if not qa_chain:
        print("❌ Error al inicializar el sistema")
        return
    
    print("✅ Sistema inicializado correctamente")
    
    # Obtener estadísticas
    obtener_estadisticas(chroma_client)
    
    # Ejemplos de consultas
    consultas_ejemplo = [
        "¿Qué es YOLOv11 y cuáles son sus características principales?",
        "¿Cuáles son las mejoras de YOLOv11 sobre versiones anteriores?",
        "¿Qué tareas de visión por computadora soporta YOLOv11?",
        "¿Cuál es la diferencia entre YOLOv10 y YOLOv11?"
    ]
    
    print(f"\n💡 Consultas de ejemplo:")
    for i, query in enumerate(consultas_ejemplo, 1):
        print(f"{i}. {query}")
    
    # Realizar consultas
    while True:
        print(f"\n" + "="*60)
        query = input("🤔 Ingresa tu consulta (o 'salir' para terminar): ").strip()
        
        if query.lower() in ['salir', 'exit', 'quit']:
            break
        
        if query:
            consultar_con_llm(qa_chain, query)
        else:
            print("Por favor ingresa una consulta válida")

if __name__ == "__main__":
    main()
