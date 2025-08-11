# Sistema de Vectorización de Documentos PDF con LangChain y Chroma

Este proyecto permite cargar documentos PDF, dividirlos en chunks y vectorizarlos en una base de datos Chroma local para búsquedas semánticas.

## Versiones Instaladas

- **LangChain**: 0.3.27
- **LangChain Core**: 0.3.74
- **ChromaDB**: 1.0.16
- **PyPDF**: 5.9.0

## Configuración del Sistema

### Configuraciones Importantes:

1. **Tamaño de Chunks (CHUNK_SIZE)**: 1000 caracteres
   - Recomendado para documentos técnicos/científicos
   - Puedes ajustar según el tipo de contenido

2. **Solapamiento de Chunks (CHUNK_OVERLAP)**: 200 caracteres
   - Mantiene contexto entre chunks adyacentes
   - Evita cortar frases importantes

3. **Puerto de Chroma**: 8000
   - Asegúrate de que Chroma esté ejecutándose en este puerto

4. **Modelo de Embeddings**: gpt-oss:20b (Ollama)
   - Modelo avanzado para embeddings de alta calidad
   - Requiere Ollama instalado con el modelo gpt-oss:20b

5. **Configuración de Ollama**:
   - Host: localhost
   - Puerto: 11434
   - Modelo: gpt-oss:20b

## Instalación y Configuración

### 1. Verificar que Chroma esté ejecutándose:
```bash
# Si usas Docker Compose
docker-compose up -d

# O iniciar Chroma manualmente en puerto 8000
```

### 2. Verificar que Ollama esté disponible:
```bash
# Verificar que Ollama esté instalado
ollama --version

# Verificar modelos disponibles
ollama list

# Si no tienes gpt-oss:20b, instalarlo
ollama pull gpt-oss:20b
```

## Uso del Sistema

### 1. Vectorizar Documentos PDF:
```bash
python ejemplo1.py
```

Este script:
- Carga todos los PDF de la carpeta `Documentos/`
- Los divide en chunks de 1000 caracteres
- Los vectoriza en la base de datos Chroma
- Usa embeddings con el modelo gpt-oss:120b

### 2. Consultar Documentos Vectorizados:
```bash
python consultar_documentos.py
```

Este script permite:
- Realizar búsquedas semánticas
- Ver estadísticas de la base de datos
- Explorar contenido vectorizado

## Configuraciones Recomendadas

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

**Embeddings con gpt-oss:120b:**
```python
embeddings = OllamaEmbeddings(
    model="gpt-oss:20b",
    base_url="http://localhost:11434"
)
```

## Estructura del Proyecto

```
Ejemplo1/
├── ejemplo1.py              # Script principal de vectorización
├── consultar_documentos.py  # Script de consultas
├── requirements_ultra_minimal.txt  # Dependencias
├── docker-compose.yml      # Configuración de Chroma
├── Documentos/             # Carpeta con PDFs
│   ├── 2502.12524v1.pdf
│   └── 2410.17725v1.pdf
└── chroma_data/           # Datos persistentes de Chroma
```

## Solución de Problemas

### Error de Conexión con Chroma:
- Verificar que Chroma esté ejecutándose en puerto 8000
- Revisar logs de Docker: `docker-compose logs`

### Error de Embeddings:
- Verificar que Ollama esté instalado
- Descargar modelo: `ollama pull gpt-oss:120b`
- Verificar que el modelo esté disponible: `ollama list`

### Error al Cargar PDFs:
- Verificar que los archivos PDF no estén corruptos
- Asegurar permisos de lectura en la carpeta Documentos

## Monitoreo y Mantenimiento

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

## Rendimiento y Optimización

### Para Grandes Volúmenes:
- Aumentar CHUNK_SIZE para reducir número de chunks
- Usar procesamiento por lotes
- Considerar múltiples colecciones por tipo de documento

### Para Consultas Rápidas:
- Indexar metadatos importantes
- Usar filtros en las consultas
- Optimizar queries con parámetros específicos

## Verificación de la Instalación

```bash
# Verificar que todas las librerías estén instaladas correctamente
python -c "
import langchain
import langchain_core
import chromadb
import pypdf
print('✓ Todas las librerías instaladas correctamente')
print(f'LangChain: {langchain.__version__}')
print(f'LangChain Core: {langchain_core.__version__}')
print(f'ChromaDB: {chromadb.__version__}')
"

# Verificar que el modelo gpt-oss:20b esté disponible
ollama list | grep gpt-oss
```
