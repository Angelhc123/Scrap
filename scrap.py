import requests 
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Configuración
ORG_NAME = "NOMBRE DE LA ORGANIZACION"
GITHUB_TOKEN = "TOKEN DE GITHUB"  # Necesitas generar uno en GitHub
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_all_repos(org_name):
    """Obtener todos los repositorios de una organización"""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{org_name}/repos?page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error al obtener repositorios: {response.status_code}")
            break
        
        data = response.json()
        if not data:
            break
            
        repos.extend(data)
        page += 1
        time.sleep(1)  # Para evitar rate limiting
        
    return repos

def analyze_repo_languages(repo):
    """Analizar los lenguajes de un repositorio"""
    url = repo['languages_url']
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {}

def get_repo_readme(repo):
    """Obtener el contenido del README de un repositorio"""
    url = f"https://api.github.com/repos/{repo['full_name']}/readme"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        readme_data = response.json()
        readme_content = requests.get(readme_data['download_url']).text
        return readme_content.lower()  # Convertir a minúsculas para búsqueda insensible
    return ""

def detect_tech_in_readme(readme_content, tech_list):
    """Detectar tecnologías mencionadas en el README"""
    detected = []
    for tech in tech_list:
        if tech.lower() in readme_content:
            detected.append(tech)
    return detected

# (El código anterior permanece igual hasta la función analyze_repositories)

def analyze_repositories(repos):
    """Analizar todos los repositorios"""
    # Inicializar estructuras de datos
    language_stats = defaultdict(int)
    framework_stats = defaultdict(int)
    library_stats = defaultdict(int)
    db_stats = defaultdict(int)
    ci_cd_stats = defaultdict(int)
    last_updated = []
    
    # Listas ampliadas de tecnologías
    frameworks = ["react", "angular", "vue", "django", "flask", "spring", "laravel", 
                 "express", "rails", ".net", "flutter", "xamarin", "asp.net", "ktor"]
    
    # Librerías específicas por lenguaje (ampliadas significativamente)
    libraries = {
        'python': ["pandas", "numpy", "tensorflow", "pytorch", "scikit-learn", "matplotlib", 
                  "seaborn", "requests", "beautifulsoup", "scrapy", "opencv", "pillow",
                  "django", "flask", "fastapi", "sqlalchemy", "pytest", "pygame", "nltk",
                  "spacy", "transformers", "keras", "plotly", "bokeh", "dash", "celery"],
        
        'javascript': ["axios", "lodash", "moment", "react", "vue", "angular", "jquery",
                      "express", "redux", "jest", "mocha", "chai", "webpack", "babel",
                      "three.js", "d3.js", "socket.io", "mongoose", "sequelize"],
        
        'java': ["junit", "mockito", "lombok", "log4j", "slf4j", "gson", "jackson",
                "hibernate", "spring-boot", "spring-mvc", "spring-security", "jpa",
                "jdbc", "apache-commons", "guava", "assertj", "jersey", "vert.x"],
        
        'c#': ["entityframework", "dapper", "newtonsoft.json", "nunit", "xunit",
              "moq", "serilog", "automapper", "mediatr", "polly", "hangfire",
              "signalr", "aspnetcore", "efcore", "identityserver", "fluentvalidation"],
        
        'php': ["laravel", "symfony", "codeigniter", "cakephp", "phpunit", "monolog",
               "guzzle", "doctrine", "eloquent", "phpmailer", "twig", "faker"],
        
        'ruby': ["rails", "sinatra", "rspec", "capybara", "devise", "sidekiq",
                "puma", "faraday", "rubocop", "hanami", "grape", "activeadmin"],
        
        'go': ["gin", "echo", "gorm", "testify", "viper", "cobra", "zerolog",
              "uuid", "go-redis", "go-kit", "go-micro", "grpc-go", "mux"]
    }
    
    databases = ["mysql", "postgresql", "mongodb", "sqlite", "mariadb", "redis", 
                "firebase", "oracle", "sqlserver", "cassandra", "dynamodb", "neo4j",
                "elasticsearch", "couchdb", "rethinkdb", "arangodb", "cosmosdb"]
    
    ci_cd_tools = ["github actions", "jenkins", "travis ci", "circleci", "gitlab ci", 
                  "azure pipelines", "teamcity", "bamboo", "bitbucket pipelines",
                  "argo cd", "tekton", "spinnaker", "flux"]
    
    for repo in repos:
        print(f"\nAnalizando repositorio: {repo['name']}")
        
        # Lenguajes de programación
        languages = analyze_repo_languages(repo)
        for lang, bytes in languages.items():
            language_stats[lang] += bytes
        
        # Obtener README y analizar
        readme = get_repo_readme(repo)
        
        # Detectar tecnologías
        for framework in detect_tech_in_readme(readme, frameworks):
            framework_stats[framework] += 1
            
        # Detectar librerías específicas por lenguaje
        for lang in languages:
            lang_lower = lang.lower()
            if lang_lower in libraries:
                for library in detect_tech_in_readme(readme, libraries[lang_lower]):
                    library_stats[f"{lang.lower()}:{library}"] += 1
                    
        for db in detect_tech_in_readme(readme, databases):
            db_stats[db] += 1
            
        for tool in detect_tech_in_readme(readme, ci_cd_tools):
            ci_cd_stats[tool] += 1
            
        # Fecha de última actualización
        last_updated.append(datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ"))
        
        # Esperar para evitar rate limiting
        time.sleep(1)
    
    return {
        "languages": language_stats,
        "frameworks": framework_stats,
        "libraries": library_stats,
        "databases": db_stats,
        "ci_cd_tools": ci_cd_stats,
        "last_updated": last_updated
    }

# (El resto del código permanece igual)

def create_dataframes(stats):
    """Convertir estadísticas en DataFrames de pandas"""
    # Lenguajes
    lang_df = pd.DataFrame.from_dict(stats["languages"], orient='index', columns=['bytes']).reset_index()
    lang_df.columns = ['language', 'bytes']
    lang_df['percentage'] = (lang_df['bytes'] / lang_df['bytes'].sum()) * 100
    lang_df = lang_df.sort_values('bytes', ascending=False)
    
    # Frameworks
    framework_df = pd.DataFrame.from_dict(stats["frameworks"], orient='index', columns=['count']).reset_index()
    framework_df.columns = ['framework', 'count']
    framework_df = framework_df.sort_values('count', ascending=False)
    
    # Librerías
    library_df = pd.DataFrame.from_dict(stats["libraries"], orient='index', columns=['count']).reset_index()
    library_df.columns = ['library', 'count']
    library_df = library_df.sort_values('count', ascending=False)
    
    # Bases de datos
    db_df = pd.DataFrame.from_dict(stats["databases"], orient='index', columns=['count']).reset_index()
    db_df.columns = ['database', 'count']
    db_df = db_df.sort_values('count', ascending=False)
    
    # CI/CD
    ci_cd_df = pd.DataFrame.from_dict(stats["ci_cd_tools"], orient='index', columns=['count']).reset_index()
    ci_cd_df.columns = ['tool', 'count']
    ci_cd_df = ci_cd_df.sort_values('count', ascending=False)
    
    # Fechas de actualización
    dates = pd.Series(stats["last_updated"])
    update_df = pd.DataFrame({
        'year': dates.dt.year,
        'month': dates.dt.month,
        'year_month': dates.dt.to_period('M')
    })
    update_stats = update_df['year_month'].value_counts().sort_index().reset_index()
    update_stats.columns = ['year_month', 'count']
    
    return {
        "languages": lang_df,
        "frameworks": framework_df,
        "libraries": library_df,
        "databases": db_df,
        "ci_cd_tools": ci_cd_df,
        "updates": update_stats
    }

def generate_visualizations(dfs):
    """Generar visualizaciones de los datos"""
    # Lenguajes
    plt.figure(figsize=(12, 6))
    plt.bar(dfs["languages"].head(10)['language'], dfs["languages"].head(10)['percentage'])
    plt.title('Top 10 Lenguajes de Programación (por uso en bytes)')
    plt.ylabel('Porcentaje (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('languages_distribution.png')
    plt.close()
    
    # Frameworks
    plt.figure(figsize=(12, 6))
    plt.bar(dfs["frameworks"]['framework'], dfs["frameworks"]['count'])
    plt.title('Frameworks más populares')
    plt.ylabel('Número de repositorios')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('frameworks_popularity.png')
    plt.close()
    
    # Librerías
    plt.figure(figsize=(12, 6))
    plt.bar(dfs["libraries"].head(10)['library'], dfs["libraries"].head(10)['count'])
    plt.title('Top 10 Librerías más utilizadas')
    plt.ylabel('Número de repositorios')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('libraries_usage.png')
    plt.close()
    
    # Bases de datos
    plt.figure(figsize=(12, 6))
    plt.bar(dfs["databases"]['database'], dfs["databases"]['count'])
    plt.title('Bases de datos más empleadas')
    plt.ylabel('Número de repositorios')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('databases_usage.png')
    plt.close()
    
    # CI/CD
    plt.figure(figsize=(12, 6))
    plt.bar(dfs["ci_cd_tools"]['tool'], dfs["ci_cd_tools"]['count'])
    plt.title('Herramientas CI/CD utilizadas')
    plt.ylabel('Número de repositorios')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('ci_cd_tools.png')
    plt.close()
    
    # Actualizaciones
    plt.figure(figsize=(12, 6))
    plt.plot(dfs["updates"]['year_month'].astype(str), dfs["updates"]['count'])
    plt.title('Actividad de los repositorios por mes')
    plt.ylabel('Número de actualizaciones')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('repo_activity.png')
    plt.close()

def save_to_excel(dfs, filename='github_analysis.xlsx'):
    """Guardar todos los datos en un archivo Excel"""
    with pd.ExcelWriter(filename) as writer:
        dfs["languages"].to_excel(writer, sheet_name='Lenguajes', index=False)
        dfs["frameworks"].to_excel(writer, sheet_name='Frameworks', index=False)
        dfs["libraries"].to_excel(writer, sheet_name='Librerías', index=False)
        dfs["databases"].to_excel(writer, sheet_name='Bases de Datos', index=False)
        dfs["ci_cd_tools"].to_excel(writer, sheet_name='CI_CD', index=False)
        dfs["updates"].to_excel(writer, sheet_name='Actividad', index=False)

def main():
    print(f"Obteniendo repositorios de la organización {ORG_NAME}...")
    repos = get_all_repos(ORG_NAME)
    print(f"Se encontraron {len(repos)} repositorios.")
    
    print("Analizando repositorios...")
    stats = analyze_repositories(repos)
    
    print("Procesando datos...")
    dfs = create_dataframes(stats)
    
    print("Generando visualizaciones...")
    generate_visualizations(dfs)
    
    print("Guardando en Excel...")
    save_to_excel(dfs)
    
    print("Análisis completado!")
    print("\nResumen de hallazgos:")
    print(f"- Lenguajes más usados: {', '.join(dfs['languages'].head(3)['language'].tolist())}")
    print(f"- Frameworks más populares: {', '.join(dfs['frameworks'].head(3)['framework'].tolist())}")
    print(f"- Librerías más utilizadas: {', '.join(dfs['libraries'].head(3)['library'].tolist())}")
    print(f"- Bases de datos más empleadas: {', '.join(dfs['databases'].head(3)['database'].tolist())}")
    print(f"- Herramientas CI/CD encontradas: {', '.join(dfs['ci_cd_tools']['tool'].tolist())}")

if __name__ == "__main__":
    main()