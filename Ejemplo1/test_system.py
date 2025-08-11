"""
Script de prueba para verificar que todo el sistema funciona correctamente
"""

import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import print_config, get_ollama_config, get_chroma_config, get_models_config
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
import requests

def test_ollama_connection():
    """Prueba la conexión con el servidor Ollama"""
    print("🔍 Probando conexión con Ollama...")
    
    config = get_ollama_config()
    try:
        response = requests.get(f"{config['base_url']}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json()["models"]
            print(f"✅ Conexión exitosa a {config['base_url']}")
            print(f"📦 Modelos disponibles: {len(models)}")
            for model in models:
                print(f"   - {model['name']}")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_embeddings():
    """Prueba el modelo de embeddings"""
    print("\n🔍 Probando modelo de embeddings...")
    
    config = get_models_config()
    try:
        embeddings = OllamaEmbeddings(
            model=config["embedding_model"],
            base_url=get_ollama_config()["base_url"]
        )
        
        # Probar con un texto simple
        test_text = "Este es un texto de prueba para embeddings"
        vectors = embeddings.embed_query(test_text)
        
        print(f"✅ Embeddings funcionando correctamente")
        print(f"📊 Dimensiones del vector: {len(vectors)}")
        return True
    except Exception as e:
        print(f"❌ Error en embeddings: {e}")
        return False

def test_chroma_connection():
    """Prueba la conexión con Chroma"""
    print("\n🔍 Probando conexión con Chroma...")
    
    config = get_chroma_config()
    try:
        # Intentar conectar a Chroma
        embeddings = OllamaEmbeddings(
            model=get_models_config()["embedding_model"],
            base_url=get_ollama_config()["base_url"]
        )
        
        chroma_client = Chroma(
            collection_name=config["collection_name"],
            embedding_function=embeddings,
            persist_directory=config["persist_directory"]
        )
        
        # Verificar que la colección existe
        count = chroma_client._collection.count()
        print(f"✅ Conexión exitosa a Chroma")
        print(f"📊 Documentos en BD: {count}")
        return True
    except Exception as e:
        print(f"❌ Error en Chroma: {e}")
        return False

def test_llm():
    """Prueba el modelo LLM"""
    print("\n🔍 Probando modelo LLM...")
    
    config = get_models_config()
    try:
        llm = Ollama(
            model=config["llm_model"],
            base_url=get_ollama_config()["base_url"]
        )
        
        # Probar con una pregunta simple
        test_prompt = "Responde con 'OK' si puedes leer este mensaje."
        response = llm.invoke(test_prompt)
        
        print(f"✅ LLM funcionando correctamente")
        print(f"🤖 Respuesta: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Error en LLM: {e}")
        return False

def test_documents_path():
    """Prueba que la ruta de documentos existe"""
    print("\n🔍 Probando ruta de documentos...")
    
    from config import DOCUMENTS_PATH
    path = Path(DOCUMENTS_PATH)
    
    if path.exists():
        pdf_files = list(path.glob("*.pdf"))
        print(f"✅ Ruta de documentos encontrada: {DOCUMENTS_PATH}")
        print(f"📄 Archivos PDF encontrados: {len(pdf_files)}")
        for pdf in pdf_files:
            print(f"   - {pdf.name}")
        return True
    else:
        print(f"❌ Ruta de documentos no encontrada: {DOCUMENTS_PATH}")
        return False

def test_imports():
    """Prueba que todas las librerías se pueden importar"""
    print("🔍 Probando importaciones...")
    
    try:
        import langchain
        import langchain_core
        import langchain_community
        import langchain_chroma
        import langchain_ollama
        import chromadb
        import pypdf
        
        print("✅ Todas las librerías importadas correctamente")
        print(f"📦 LangChain: {langchain.__version__}")
        print(f"📦 LangChain Core: {langchain_core.__version__}")
        print(f"📦 LangChain Community: {langchain_community.__version__}")
        print(f"📦 LangChain Chroma: Instalado")
        print(f"📦 LangChain Ollama: {langchain_ollama.__version__}")
        print(f"📦 ChromaDB: {chromadb.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("🧪 SISTEMA DE PRUEBAS DEL RAG")
    print("=" * 60)
    
    # Mostrar configuración actual
    print_config()
    
    # Ejecutar pruebas
    tests = [
        ("Importaciones", test_imports),
        ("Conexión Ollama", test_ollama_connection),
        ("Modelo Embeddings", test_embeddings),
        ("Conexión Chroma", test_chroma_connection),
        ("Modelo LLM", test_llm),
        ("Ruta Documentos", test_documents_path),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en prueba {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Sistema completamente funcional!")
        print("🚀 Puedes ejecutar:")
        print("   - python ejemplo1.py (vectorizar documentos)")
        print("   - python consultar_documentos.py (consultas simples)")
        print("   - python consultar_con_llm.py (consultas con LLM)")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa la configuración.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
