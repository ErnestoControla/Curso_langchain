# Sistema de Vectorización y Consulta de Documentos PDF con LangChain y Chroma

Este proyecto implementa un sistema completo de **RAG (Retrieval-Augmented Generation)** que permite cargar documentos PDF, vectorizarlos y realizar consultas inteligentes usando LLMs.

## 🏗️ Arquitectura del Sistema

```
📄 Documentos PDF → 🔍 nomic-embed-text → 🗄️ Chroma DB → 🤖 gpt-oss:20b → 📝 Respuesta
```

### Componentes:
- **Embeddings**: `nomic-embed-text:latest` (vectorización)
- **Base de datos**: Chroma en `localhost:8000` (almacenamiento)
- **LLM**: `gpt-oss:20b` (generación de respuestas)
- **Servidor**: Ollama en `172.16.1.37:11434`

## 📦 Versiones Instaladas

- **LangChain**: 0.3.27
- **LangChain Core**: 0.3.74
- **LangChain Community**: 0.0.38
- **LangChain Chroma**: 0.2.5
- **LangChain Ollama**: 0.1.0
- **ChromaDB**: 1.0.16
- **PyPDF**: 5.9.0

## ⚙️ Configuración del Sistema

### Configuraciones Importantes:

1. **Tamaño de Chunks (CHUNK_SIZE)**: 1000 caracteres
   - Recomendado para documentos técnicos/científicos
   - Puedes ajustar según el tipo de contenido

2. **Solapamiento de Chunks (CHUNK_OVERLAP)**: 200 caracteres
   - Mantiene contexto entre chunks adyacentes
   - Evita cortar frases importantes

3. **Puerto de Chroma**: 8000
   - Asegúrate de que Chroma esté ejecutándose en este puerto

4. **Modelo de Embeddings**: nomic-embed-text:latest (Ollama)
   - Modelo especializado para embeddings
   - Requiere Ollama instalado con el modelo nomic-embed-text

5. **Modelo LLM**: gpt-oss:20b (Ollama)
   - Modelo para generación de respuestas
   - Optimizado para velocidad y calidad

6. **Configuración de Ollama**:
   - Host: 172.16.1.37
   - Puerto: 11434
   - Modelos: nomic-embed-text:latest, gpt-oss:20b

## 🚀 Instalación y Configuración

### 1. Crear ambiente conda:
```bash
conda create -n langchain_clean python=3.9
conda activate langchain_clean
```

### 2. Instalar dependencias:
```bash
pip install -r requirements_ultra_minimal.txt
```

### 3. Verificar que Chroma esté ejecutándose:
```bash
# Si usas Docker Compose
docker-compose up -d

# O iniciar Chroma manualmente en puerto 8000
```

### 4. Verificar que Ollama esté disponible:
```bash
# Verificar que Ollama esté instalado
ollama --version

# Verificar modelos disponibles
curl -s http://172.16.1.37:11434/api/tags | python -c "import sys, json; data=json.load(sys.stdin); print('Modelos disponibles:'); [print(f'- {model[\"name\"]}') for model in data['models']]"

# Si no tienes nomic-embed-text, instalarlo
curl -X POST http://172.16.1.37:11434/api/pull -d '{"name": "nomic-embed-text"}'
```

## 📋 Uso del Sistema

### 1. Vectorizar Documentos PDF:
```bash
python ejemplo1.py
```

Este script:
- Carga todos los PDF de la carpeta `Documentos/`
- Los divide en chunks de 1000 caracteres
- Los vectoriza usando nomic-embed-text
- Los almacena en la base de datos Chroma

### 2. Consultar Documentos (Búsqueda Simple):
```bash
python consultar_documentos.py
```

Este script permite:
- Realizar búsquedas semánticas
- Ver estadísticas de la base de datos
- Explorar contenido vectorizado

### 3. Consultar con LLM (Respuestas Inteligentes):
```bash
python consultar_con_llm.py
```

Este script combina:
- Búsqueda semántica con embeddings
- Generación de respuestas con LLM
- Respuestas contextualizadas y estructuradas

### 4. Monitorear Base de Datos:
```bash
python database_monitor.py
```

Este script permite:
- Verificar el estado de la base de datos
- Obtener estadísticas detalladas
- Realizar consultas de diagnóstico
- Exportar reportes en JSON
- Modo interactivo para exploración

## 🔧 Configuraciones Recomendadas

### Para Diferentes Tipos de Contenido:

**Documentos Técnicos/Científicos:**
- CHUNK_SIZE: 1000-1500 caracteres
- CHUNK_OVERLAP: 200-300 caracteres

**Documentos Narrativos:**
- CHUNK_SIZE: 800-1200 caracteres
- CHUNK_OVERLAP: 150-250 caracteres

**Documentos Legales/Contractuales:**
- CHUNK_SIZE: 1200-2000 caracteres
- CHUNK_OVERLAP: 300-500 caracteres

### Configuración de la Base de Datos:

**Chroma Settings:**
```python
chroma_client = Chroma(
    collection_name="documentos_pdf",
    embedding_function=embeddings,
    persist_directory="chroma_data"
)
```

**Embeddings con nomic-embed-text:**
```python
embeddings = OllamaEmbeddings(
    model="nomic-embed-text:latest",
    base_url="http://172.16.1.37:11434"
)
```

**LLM con gpt-oss:20b:**
```python
llm = Ollama(
    model="gpt-oss:20b",
    base_url="http://172.16.1.37:11434"
)
```

## 📁 Estructura del Proyecto

```
Ejemplo1/
├── ejemplo1.py                    # Script principal de vectorización
├── consultar_documentos.py        # Script de consultas simples
├── consultar_con_llm.py          # Script de consultas con LLM
├── database_monitor.py           # Monitor de base de datos
├── test_system.py                # Script de pruebas del sistema
├── config.py                     # Configuración centralizada
├── requirements_ultra_minimal.txt # Dependencias exactas
├── docker-compose.yml            # Configuración de Chroma
├── README.md                     # Documentación
├── .gitignore                    # Archivos a ignorar
├── Documentos/                   # Carpeta con PDFs
│   ├── 2502.12524v1.pdf
│   └── 2410.17725v1.pdf
└── chroma_data/                  # Datos persistentes de Chroma
```

## 🔍 Solución de Problemas

### Error de Conexión con Chroma:
- Verificar que Chroma esté ejecutándose en puerto 8000
- Revisar logs de Docker: `docker-compose logs`

### Error de Embeddings:
- Verificar que Ollama esté instalado
- Descargar modelo: `curl -X POST http://172.16.1.37:11434/api/pull -d '{"name": "nomic-embed-text"}'`
- Verificar que el modelo esté disponible

### Error al Cargar PDFs:
- Verificar que los archivos PDF no estén corruptos
- Asegurar permisos de lectura en la carpeta Documentos

### Error de LLM:
- Verificar que gpt-oss:20b esté disponible en el servidor
- Comprobar conectividad con 172.16.1.37:11434

## 📊 Monitoreo y Mantenimiento

### Monitor de Base de Datos:
```bash
# Verificación completa automática
python database_monitor.py

# Modo interactivo para exploración
python database_monitor.py
# Luego usar comandos: stats, detailed, search, health, export, quit
```

### Funcionalidades del Monitor:
- **Estadísticas básicas**: Conteo de documentos, metadatos
- **Estadísticas detalladas**: Análisis de longitud, fuentes, páginas
- **Pruebas de búsqueda**: Verificación de consultas semánticas
- **Verificación de salud**: Estado general de la base de datos
- **Exportación**: Reportes en formato JSON
- **Modo interactivo**: Exploración interactiva de la BD

### Verificar Estado de la Base de Datos:
```python
# En consultar_documentos.py
obtener_estadisticas(chroma_client)
```

### Limpiar Base de Datos:
```python
# Eliminar colección si es necesario
chroma_client.delete_collection()
```

### Backup de Datos:
- Los datos se guardan en `chroma_data/`
- Hacer backup regular de esta carpeta

## ⚡ Rendimiento y Optimización

### Para Grandes Volúmenes:
- Aumentar CHUNK_SIZE para reducir número de chunks
- Usar procesamiento por lotes
- Considerar múltiples colecciones por tipo de documento

### Para Consultas Rápidas:
- Indexar metadatos importantes
- Usar filtros en las consultas
- Optimizar queries con parámetros específicos

### Cambio de Modelos:
Para cambiar el LLM, modifica esta línea en `consultar_con_llm.py`:
```python
LLM_MODEL = "gpt-oss:120b"  # Cambia por el modelo deseado
```

Modelos disponibles en el servidor:
- gpt-oss:20b (recomendado - velocidad/calidad)
- gpt-oss:120b (más potente - más lento)
- gemma3:12b
- deepseek-r1:latest
- llama3.1:8b

## ✅ Verificación de la Instalación

### Verificación Completa del Sistema:
```bash
# Ejecutar todas las pruebas automáticamente
python test_system.py
```

### Verificación de la Base de Datos:
```bash
# Verificar estado y contenido de la base de datos
python database_monitor.py
```

### Verificación Manual de Librerías:
```bash
# Verificar que todas las librerías estén instaladas correctamente
python -c "
import langchain
import langchain_core
import langchain_community
import langchain_chroma
import langchain_ollama
import chromadb
import pypdf
print('✓ Todas las librerías instaladas correctamente')
print(f'LangChain: {langchain.__version__}')
print(f'LangChain Core: {langchain_core.__version__}')
print(f'LangChain Community: {langchain_community.__version__}')
print(f'LangChain Chroma: Instalado')
print(f'LangChain Ollama: {langchain_ollama.__version__}')
print(f'ChromaDB: {chromadb.__version__}')
"

# Verificar que los modelos estén disponibles
curl -s http://172.16.1.37:11434/api/tags | python -c "import sys, json; data=json.load(sys.stdin); print('Modelos disponibles:'); [print(f'- {model[\"name\"]}') for model in data['models']]"
```

## 🎯 Casos de Uso

### 1. Investigación Académica:
- Cargar papers científicos
- Hacer consultas específicas sobre metodologías
- Obtener respuestas contextualizadas

### 2. Documentación Técnica:
- Indexar manuales técnicos
- Buscar soluciones específicas
- Generar resúmenes automáticos

### 3. Análisis de Documentos:
- Procesar reportes empresariales
- Extraer información clave
- Generar insights automáticos

## 🔄 Flujo de Trabajo Típico

1. **Preparación**: Colocar PDFs en carpeta `Documentos/`
2. **Vectorización**: Ejecutar `python ejemplo1.py`
3. **Verificación del Sistema**: Ejecutar `python test_system.py`
4. **Verificación de la BD**: Ejecutar `python database_monitor.py`
5. **Consulta**: Ejecutar `python consultar_con_llm.py`
6. **Mantenimiento**: Backup regular de `chroma_data/`

## 📈 Métricas del Sistema

- **Documentos procesados**: 2 PDFs
- **Chunks generados**: 114
- **Tiempo de vectorización**: ~30 segundos
- **Tiempo de consulta**: ~2-5 segundos
- **Precisión de búsqueda**: Alta (embeddings semánticos)
- **Calidad de respuestas**: Excelente (LLM contextual)
