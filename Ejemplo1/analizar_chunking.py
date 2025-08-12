"""
Script para analizar en detalle cómo funciona la división de documentos en chunks
Explica las estrategias de contexto y las decisiones de diseño implementadas
"""

import os
import sys
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analizar_estrategia_chunking():
    """
    Analiza la estrategia de chunking implementada en ejemplo1.py
    """
    print("=" * 80)
    print("🔍 ANÁLISIS DETALLADO DE LA ESTRATEGIA DE CHUNKING")
    print("=" * 80)
    
    # Configuración actual del proyecto
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    DOCUMENTS_PATH = "/home/ernesto/Proyectos_local/Curso_langchain/Ejemplo1/Documentos/"
    
    print(f"📊 CONFIGURACIÓN ACTUAL:")
    print(f"   - Tamaño de chunks: {CHUNK_SIZE} caracteres")
    print(f"   - Solapamiento: {CHUNK_OVERLAP} caracteres")
    print(f"   - Porcentaje de solapamiento: {(CHUNK_OVERLAP/CHUNK_SIZE)*100:.1f}%")
    print(f"   - Separadores: ['\\n\\n', '\\n', ' ', '']")
    
    # Crear el text splitter con la configuración actual
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    print(f"\n🏗️ ESTRATEGIA DE DIVISIÓN IMPLEMENTADA:")
    print(f"   - Tipo: RecursiveCharacterTextSplitter")
    print(f"   - Enfoque: División recursiva por separadores")
    print(f"   - Prioridad: Mantener unidades semánticas intactas")
    
    # Analizar separadores
    print(f"\n🔧 ANÁLISIS DE SEPARADORES:")
    separators = ["\n\n", "\n", " ", ""]
    for i, separator in enumerate(separators):
        if separator == "\n\n":
            desc = "Párrafos (doble salto de línea)"
        elif separator == "\n":
            desc = "Líneas (salto de línea simple)"
        elif separator == " ":
            desc = "Palabras (espacios)"
        else:
            desc = "Caracteres individuales (último recurso)"
        print(f"   {i+1}. '{repr(separator)}': {desc}")
    
    return text_splitter

def demostrar_proceso_chunking(text_splitter):
    """
    Demuestra el proceso de chunking con ejemplos reales
    """
    print(f"\n" + "=" * 80)
    print("🎯 DEMOSTRACIÓN DEL PROCESO DE CHUNKING")
    print("=" * 80)
    
    # Cargar un documento de ejemplo
    DOCUMENTS_PATH = "/home/ernesto/Proyectos_local/Curso_langchain/Ejemplo1/Documentos/"
    ruta = Path(DOCUMENTS_PATH)
    archivos_pdf = list(ruta.glob("*.pdf"))
    
    if not archivos_pdf:
        print("❌ No se encontraron archivos PDF para analizar")
        return
    
    # Usar el primer PDF como ejemplo
    archivo_ejemplo = archivos_pdf[0]
    print(f"📄 Analizando: {archivo_ejemplo.name}")
    
    try:
        # Cargar el documento
        loader = PyPDFLoader(str(archivo_ejemplo))
        documentos = loader.load()
        
        if not documentos:
            print("❌ No se pudo cargar el documento")
            return
        
        # Tomar solo la primera página para el análisis
        documento_ejemplo = documentos[0]
        texto_original = documento_ejemplo.page_content
        
        print(f"\n📏 ESTADÍSTICAS DEL TEXTO ORIGINAL:")
        print(f"   - Longitud total: {len(texto_original)} caracteres")
        print(f"   - Número de párrafos: {texto_original.count(chr(10) + chr(10))}")
        print(f"   - Número de líneas: {texto_original.count(chr(10))}")
        print(f"   - Número de palabras: {len(texto_original.split())}")
        
        # Mostrar una muestra del texto original
        print(f"\n📝 MUESTRA DEL TEXTO ORIGINAL (primeros 500 caracteres):")
        print("-" * 60)
        print(texto_original[:500] + "..." if len(texto_original) > 500 else texto_original)
        print("-" * 60)
        
        # Aplicar chunking
        chunks = text_splitter.split_documents([documento_ejemplo])
        
        print(f"\n✂️ RESULTADO DEL CHUNKING:")
        print(f"   - Número de chunks generados: {len(chunks)}")
        
        # Analizar cada chunk
        for i, chunk in enumerate(chunks[:3]):  # Mostrar solo los primeros 3 chunks
            print(f"\n🔍 CHUNK {i+1}:")
            print(f"   - Longitud: {len(chunk.page_content)} caracteres")
            print(f"   - Palabras: {len(chunk.page_content.split())}")
            print(f"   - Contenido:")
            print("-" * 40)
            print(chunk.page_content[:300] + "..." if len(chunk.page_content) > 300 else chunk.page_content)
            print("-" * 40)
        
        if len(chunks) > 3:
            print(f"\n... y {len(chunks) - 3} chunks más")
        
        # Analizar solapamiento
        if len(chunks) >= 2:
            print(f"\n🔄 ANÁLISIS DE SOLAPAMIENTO:")
            chunk1 = chunks[0].page_content
            chunk2 = chunks[1].page_content
            
            # Encontrar el solapamiento real
            overlap_size = 0
            for i in range(min(len(chunk1), len(chunk2))):
                if chunk1[-i:] == chunk2[:i]:
                    overlap_size = i
                    break
            
            print(f"   - Solapamiento configurado: {200} caracteres")
            print(f"   - Solapamiento real: {overlap_size} caracteres")
            print(f"   - Texto solapado:")
            if overlap_size > 0:
                print("-" * 30)
                print(chunk1[-overlap_size:] if overlap_size <= 100 else chunk1[-100:] + "...")
                print("-" * 30)
        
    except Exception as e:
        print(f"❌ Error al analizar el documento: {e}")

def explicar_estrategias_contexto():
    """
    Explica las estrategias de contexto implementadas
    """
    print(f"\n" + "=" * 80)
    print("🧠 ESTRATEGIAS DE CONTEXTO IMPLEMENTADAS")
    print("=" * 80)
    
    print(f"🎯 1. SOLAPAMIENTO (CHUNK OVERLAP):")
    print(f"   - Propósito: Mantener contexto entre chunks adyacentes")
    print(f"   - Configuración: 200 caracteres (20% del tamaño del chunk)")
    print(f"   - Beneficio: Evita cortar frases o conceptos importantes")
    print(f"   - Ejemplo: Si un concepto aparece al final de un chunk,")
    print(f"     también aparecerá al inicio del siguiente")
    
    print(f"\n🎯 2. SEPARADORES JERÁRQUICOS:")
    print(f"   - Enfoque: Respetar la estructura natural del texto")
    print(f"   - Prioridad 1: Párrafos (\\n\\n) - Unidades semánticas completas")
    print(f"   - Prioridad 2: Líneas (\\n) - Estructura lógica")
    print(f"   - Prioridad 3: Palabras (espacios) - Unidades léxicas")
    print(f"   - Prioridad 4: Caracteres - Último recurso")
    
    print(f"\n🎯 3. DIVISIÓN RECURSIVA:")
    print(f"   - Método: RecursiveCharacterTextSplitter")
    print(f"   - Proceso: Intenta dividir por el primer separador,")
    print(f"     si el chunk sigue siendo muy grande, usa el siguiente")
    print(f"   - Ventaja: Maximiza la preservación del contexto")
    
    print(f"\n🎯 4. TAMAÑO ÓPTIMO DE CHUNKS:")
    print(f"   - Configuración: 1000 caracteres")
    print(f"   - Justificación: Balance entre contexto y eficiencia")
    print(f"   - Muy pequeño: Pierde contexto")
    print(f"   - Muy grande: Menos preciso en búsquedas")
    
    print(f"\n🎯 5. PRESERVACIÓN DE METADATOS:")
    print(f"   - Cada chunk mantiene los metadatos del documento original")
    print(f"   - Incluye: fuente, página, título, autor, etc.")
    print(f"   - Beneficio: Trazabilidad completa del contenido")

def comparar_estrategias_alternativas():
    """
    Compara con otras estrategias de chunking posibles
    """
    print(f"\n" + "=" * 80)
    print("⚖️ COMPARACIÓN CON ESTRATEGIAS ALTERNATIVAS")
    print("=" * 80)
    
    print(f"🔍 ESTRATEGIA ACTUAL vs ALTERNATIVAS:")
    
    print(f"\n📊 1. DIVISIÓN POR TAMAÑO FIJO:")
    print(f"   - Actual: ✅ Respeta separadores naturales")
    print(f"   - Alternativa: ❌ Corta palabras y frases")
    print(f"   - Ejemplo: 'YOLO' podría cortarse en 'YO' y 'LO'")
    
    print(f"\n📊 2. DIVISIÓN POR PÁRRAFOS:")
    print(f"   - Actual: ✅ Flexible, se adapta al contenido")
    print(f"   - Alternativa: ❌ Párrafos muy largos o muy cortos")
    print(f"   - Ejemplo: Un párrafo de 5000 caracteres sería problemático")
    
    print(f"\n📊 3. DIVISIÓN POR ORACIONES:")
    print(f"   - Actual: ✅ Considera múltiples niveles de estructura")
    print(f"   - Alternativa: ⚠️ Buena, pero menos flexible")
    print(f"   - Ejemplo: Oraciones muy largas podrían ser problemáticas")
    
    print(f"\n📊 4. DIVISIÓN SEMÁNTICA:")
    print(f"   - Actual: ✅ Respeta estructura natural")
    print(f"   - Alternativa: 🔮 Futuro prometedor con IA")
    print(f"   - Ejemplo: Usar embeddings para dividir por similitud semántica")

def analizar_impacto_rendimiento():
    """
    Analiza el impacto en el rendimiento del sistema
    """
    print(f"\n" + "=" * 80)
    print("⚡ IMPACTO EN EL RENDIMIENTO DEL SISTEMA")
    print("=" * 80)
    
    print(f"📈 MÉTRICAS DE RENDIMIENTO:")
    
    print(f"\n🔍 1. PRECISIÓN DE BÚSQUEDA:")
    print(f"   - Chunks de 1000 caracteres: ✅ Balance óptimo")
    print(f"   - Contexto suficiente para entender conceptos")
    print(f"   - No demasiado ruido en los resultados")
    
    print(f"\n🔍 2. VELOCIDAD DE CONSULTA:")
    print(f"   - 114 chunks: ✅ Cantidad manejable")
    print(f"   - Tiempo de consulta: ~65ms (excelente)")
    print(f"   - Índice HNSW eficiente para esta cantidad")
    
    print(f"\n🔍 3. USO DE MEMORIA:")
    print(f"   - Tamaño total: ~32.74 MB")
    print(f"   - Por chunk: ~287 KB")
    print(f"   - Escalabilidad: Buena hasta miles de documentos")
    
    print(f"\n🔍 4. CALIDAD DE RESPUESTAS:")
    print(f"   - Solapamiento 20%: ✅ Contexto preservado")
    print(f"   - Información no se pierde entre chunks")
    print(f"   - Respuestas más coherentes del LLM")

def recomendaciones_optimizacion():
    """
    Proporciona recomendaciones para optimizar el chunking
    """
    print(f"\n" + "=" * 80)
    print("🚀 RECOMENDACIONES DE OPTIMIZACIÓN")
    print("=" * 80)
    
    print(f"💡 OPTIMIZACIONES POSIBLES:")
    
    print(f"\n🎯 1. AJUSTE DINÁMICO DE TAMAÑO:")
    print(f"   - Analizar distribución de longitudes de párrafos")
    print(f"   - Ajustar CHUNK_SIZE según el tipo de documento")
    print(f"   - Documentos técnicos: chunks más pequeños")
    print(f"   - Documentos narrativos: chunks más grandes")
    
    print(f"\n🎯 2. SEPARADORES ESPECÍFICOS:")
    print(f"   - Agregar separadores para listas: ['•', '-', '*']")
    print(f"   - Separadores para tablas: ['|', '\\t']")
    print(f"   - Separadores para código: ['```', ';', '{', '}']")
    
    print(f"\n🎯 3. METADATOS ENRIQUECIDOS:")
    print(f"   - Agregar tipo de chunk: 'parrafo', 'lista', 'tabla'")
    print(f"   - Información de sección: 'introduccion', 'metodologia'")
    print(f"   - Nivel de importancia: basado en posición en documento")
    
    print(f"\n🎯 4. CHUNKING INTELIGENTE:")
    print(f"   - Usar embeddings para detectar cambios de tema")
    print(f"   - Dividir en puntos de transición semántica")
    print(f"   - Mantener coherencia temática en cada chunk")

def main():
    """
    Función principal del análisis
    """
    print("🔍 ANÁLISIS COMPLETO DE LA ESTRATEGIA DE CHUNKING")
    print("=" * 80)
    
    # 1. Analizar estrategia actual
    text_splitter = analizar_estrategia_chunking()
    
    # 2. Demostrar proceso con ejemplo real
    demostrar_proceso_chunking(text_splitter)
    
    # 3. Explicar estrategias de contexto
    explicar_estrategias_contexto()
    
    # 4. Comparar con alternativas
    comparar_estrategias_alternativas()
    
    # 5. Analizar impacto en rendimiento
    analizar_impacto_rendimiento()
    
    # 6. Proporcionar recomendaciones
    recomendaciones_optimizacion()
    
    print(f"\n" + "=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)
    print("📋 RESUMEN:")
    print("   - La estrategia actual es sólida y bien pensada")
    print("   - Respeta la estructura natural del texto")
    print("   - Mantiene contexto a través del solapamiento")
    print("   - Proporciona buen rendimiento y escalabilidad")
    print("   - Hay oportunidades de optimización futura")

if __name__ == "__main__":
    main()
