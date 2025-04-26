# Web Scraping de Stack Tecnológico en GitHub

## Objetivo
Extraer y analizar el stack tecnológico utilizado por organizaciones en GitHub mediante scraping de sus repositorios públicos.

## Tecnologías detectadas

### Categorías principales:
1. **Lenguajes de programación**  
   (Ej: Python, JavaScript, Java, Go)
2. **Frameworks**  
   (Ej: React, Django, Spring, .NET)
3. **Librerías**  
   (Ej: Pandas, Lodash, jQuery)
4. **Bases de datos**  
   (Ej: PostgreSQL, MongoDB, Redis)
5. **Herramientas CI/CD**  
   (Ej: GitHub Actions, Jenkins, CircleCI)

## Metodología
El proceso de scraping analiza:
- Archivos de configuración (package.json, requirements.txt, etc.)
- Workflows de GitHub Actions
- Dependencias declaradas
- Estructura de directorios
- Lenguajes detectados por GitHub

## Instalacion
Antes de Correr el codigo cambiar estas lineas
```bash
# Configuración
ORG_NAME = "NOMBRE DE LA ORGANIZACION"
GITHUB_TOKEN = "TOKEN DE GITHUB"  # Necesitas generar uno en GitHub
```

Comandos para correr el codigo

```bash
.\.venv\Scripts\activate
```
```bash
pip install requests pandas matplotlib beautifulsoup4 openpyxl
```
```bash
python scrap.py
```

