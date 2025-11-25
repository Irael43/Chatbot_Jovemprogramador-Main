# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# import requests
# from bs4 import BeautifulSoup

# # === 1️⃣ CONFIGURAÇÃO E INICIALIZAÇÃO ===
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

# genai.configure(api_key=api_key)

# app = Flask(__name__)
# CORS(app)
# model = genai.GenerativeModel("gemini-2.0-flash")

# # === 2️⃣ CONSTANTES E CONFIGURAÇÕES ===
# CUMPRIMENTOS = {
#     "oi": "Olá! Como posso ajudar você hoje?",
#     "olá": "Olá! Tudo bem? Estou aqui para ajudar.",
#     "bom dia": "Bom dia! Como posso ajudar você?",
#     "boa tarde": "Boa tarde! Precisa de alguma informação?",
#     "boa noite": "Boa noite! Como posso ajudar?",
#     "e aí": "E aí! Tudo certo? Como posso ajudar?"
# }

# DESPEDIDAS = {
#     "tchau": "Até mais! Se precisar, estou aqui.",
#     "até logo": "Até logo! Volte sempre 😊",
#     "até mais": "Até mais! Foi um prazer ajudar.",
#     "falou": "Falou! Qualquer coisa, me chame!",
#     "obrigado": "Disponha! Sempre que precisar, estou por aqui.",
#     "valeu": "Valeu! Conte comigo sempre!"
# }

# TERMOS_PERMITIDOS = [
#     "jovem programador", "curso", "inscrição", "site",
#     "senac", "sesi", "empregabilidade", "ensino", "formação", "aprendizagem"
# ]

# # === 3️⃣ FUNÇÕES AUXILIARES ===
# def extrair_conteudo_site(url: str) -> str:
#     """Extrai texto do site Jovem Programador."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")
#         return soup.get_text(separator="\n", strip=True)
#     except Exception:
#         return "Erro ao acessar o site Jovem Programador."

# def extrair_dados_imagens(url: str):
#     """Extrai informações das imagens do site com atributos de acessibilidade."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")

#         imagens = []
        
#         # Processa imagens dentro de figures
#         for figura in soup.find_all("figure"):
#             img = figura.find("img")
#             legenda = figura.find("figcaption")
#             if img:
#                 imagens.append({
#                     "src": img.get("src"),
#                     "alt": img.get("alt"),
#                     "title": img.get("title"),
#                     "legenda": legenda.get_text(strip=True) if legenda else None
#                 })

#         # Processa outras imagens
#         for img in soup.find_all("img"):
#             if not any(img.get("src") == i["src"] for i in imagens):
#                 imagens.append({
#                     "src": img.get("src"),
#                     "alt": img.get("alt"),
#                     "title": img.get("title"),
#                     "legenda": None
#                 })
#         return imagens
#     except Exception:
#         return []

# def verificar_resposta_automatica(pergunta: str) -> str:
#     """Verifica se a pergunta tem resposta automática."""
#     pergunta_lower = pergunta.lower()
    
#     # Verifica cumprimentos
#     for termo in CUMPRIMENTOS:
#         if termo in pergunta_lower:
#             return CUMPRIMENTOS[termo]

#     # Verifica despedidas
#     for termo in DESPEDIDAS:
#         if termo in pergunta_lower:
#             return DESPEDIDAS[termo]
    
#     return None

# def validar_tema_pergunta(pergunta: str) -> bool:
#     """Valida se a pergunta está dentro dos temas permitidos."""
#     pergunta_lower = pergunta.lower()
#     return any(palavra in pergunta_lower for palavra in TERMOS_PERMITIDOS)

# def gerar_resposta_gemini(pergunta: str) -> str:
#     """Gera resposta usando Gemini AI."""
#     conteudo_site = extrair_conteudo_site("https://www.jovemprogramador.com.br")
#     imagens_info = extrair_dados_imagens("https://www.jovemprogramador.com.br")

#     # Formata informações das imagens
#     imagens_texto = "\n".join([
#         f"- Imagem: {img.get('alt', 'Sem descrição disponível')}. "
#         f"Título: {img.get('title', 'sem título')}. "
#         f"Legenda: {img.get('legenda', 'sem legenda')}."
#         for img in imagens_info
#     ])

#     # Constrói o prompt
#     prompt = f"""
#     Você é um assistente especializado no site Jovem Programador (https://www.jovemprogramador.com.br).
#     Responda APENAS com base nas informações desse site.
#     Caso a pergunta não esteja relacionada, informe que só pode responder sobre o site Jovem Programador.

#     Conteúdo do site:
#     {conteudo_site}

#     Informações sobre imagens:
#     {imagens_texto}

#     Pergunta do usuário:
#     {pergunta}
#     """

#     try:
#         resposta = model.generate_content(prompt)
#         texto_resposta = resposta.text.strip()
#     except Exception as e:
#         texto_resposta = f"Ocorreu um erro ao gerar a resposta: {e}"

#     # Resposta de fallback
#     if not texto_resposta or len(texto_resposta) < 20:
#         texto_resposta = (
#             "Não encontrei informações suficientes no site Jovem Programador "
#             "para responder a essa pergunta."
#         )

#     return texto_resposta

# # === 4️⃣ ROTAS ===
# @app.route('/')
# def index():
#     """Rota raiz simples"""
#     return jsonify({
#         "message": "🤖 API do Chatbot Jovem Programador está funcionando!",
#         "status": "online",
#         "endpoints": {
#             "health_check": "/health",
#             "chatbot": "/perguntar (POST)"
#         }
#     })

# @app.route("/perguntar", methods=["POST"])
# def perguntar():
#     """Rota principal do chatbot"""
#     dados = request.json
#     pergunta = dados.get("pergunta", "").strip()

#     # Validação de pergunta vazia
#     if not pergunta:
#         return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

#     # Verifica respostas automáticas
#     resposta_automatica = verificar_resposta_automatica(pergunta)
#     if resposta_automatica:
#         return jsonify({"resposta": resposta_automatica})

#     # Valida tema da pergunta
#     if not validar_tema_pergunta(pergunta):
#         return jsonify({
#             "resposta": (
#                 "Posso responder apenas sobre o site Jovem Programador. "
#                 "Por favor, envie uma pergunta relacionada a ele."
#             )
#         })

#     # Gera resposta usando AI
#     resposta = gerar_resposta_gemini(pergunta)
#     return jsonify({"resposta": resposta})

# @app.route('/health')
# def health():
#     """Health check para o Render"""
#     return jsonify({"status": "healthy"}), 200

# # === 5️⃣ EXECUÇÃO ===
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))
#     app.run(debug=False, host="0.0.0.0", port=port)



# +++++++++++++++++++++++++++++++++++++++++++++++++++

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# import requests
# from bs4 import BeautifulSoup

# # === 1️⃣ CONFIGURAÇÃO E INICIALIZAÇÃO ===
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

# genai.configure(api_key=api_key)

# app = Flask(__name__, static_folder='static', static_url_path='')
# CORS(app)
# model = genai.GenerativeModel("gemini-2.0-flash")

# # === 2️⃣ CONSTANTES E CONFIGURAÇÕES ===
# CUMPRIMENTOS = {
#     "oi": "Olá! Como posso ajudar você hoje?",
#     "olá": "Olá! Tudo bem? Estou aqui para ajudar.",
#     "bom dia": "Bom dia! Como posso ajudar você?",
#     "boa tarde": "Boa tarde! Precisa de alguma informação?",
#     "boa noite": "Boa noite! Como posso ajudar?",
#     "e aí": "E aí! Tudo certo? Como posso ajudar?"
# }

# DESPEDIDAS = {
#     "tchau": "Até mais! Se precisar, estou aqui.",
#     "até logo": "Até logo! Volte sempre 😊",
#     "até mais": "Até mais! Foi um prazer ajudar.",
#     "falou": "Falou! Qualquer coisa, me chame!",
#     "obrigado": "Disponha! Sempre que precisar, estou por aqui.",
#     "valeu": "Valeu! Conte comigo sempre!"
# }

# TERMOS_PERMITIDOS = [
#     "jovem programador", "curso", "inscrição", "site",
#     "senac", "sesi", "empregabilidade", "ensino", "formação", "aprendizagem"
# ]

# # === 3️⃣ FUNÇÕES AUXILIARES ===
# def extrair_conteudo_site(url: str) -> str:
#     """Extrai texto do site Jovem Programador."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")
#         return soup.get_text(separator="\n", strip=True)
#     except Exception:
#         return "Erro ao acessar o site Jovem Programador."

# def extrair_dados_imagens(url: str):
#     """Extrai informações das imagens do site com atributos de acessibilidade."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")

#         imagens = []
        
#         # Processa imagens dentro de figures
#         for figura in soup.find_all("figure"):
#             img = figura.find("img")
#             legenda = figura.find("figcaption")
#             if img:
#                 imagens.append({
#                     "src": img.get("src"),
#                     "alt": img.get("alt"),
#                     "title": img.get("title"),
#                     "legenda": legenda.get_text(strip=True) if legenda else None
#                 })

#         # Processa outras imagens
#         for img in soup.find_all("img"):
#             if not any(img.get("src") == i["src"] for i in imagens):
#                 imagens.append({
#                     "src": img.get("src"),
#                     "alt": img.get("alt"),
#                     "title": img.get("title"),
#                     "legenda": None
#                 })
#         return imagens
#     except Exception:
#         return []

# def verificar_resposta_automatica(pergunta: str) -> str:
#     """Verifica se a pergunta tem resposta automática."""
#     pergunta_lower = pergunta.lower()
    
#     # Verifica cumprimentos
#     for termo in CUMPRIMENTOS:
#         if termo in pergunta_lower:
#             return CUMPRIMENTOS[termo]

#     # Verifica despedidas
#     for termo in DESPEDIDAS:
#         if termo in pergunta_lower:
#             return DESPEDIDAS[termo]
    
#     return None

# def validar_tema_pergunta(pergunta: str) -> bool:
#     """Valida se a pergunta está dentro dos temas permitidos."""
#     pergunta_lower = pergunta.lower()
#     return any(palavra in pergunta_lower for palavra in TERMOS_PERMITIDOS)

# def gerar_resposta_gemini(pergunta: str) -> str:
#     """Gera resposta usando Gemini AI."""
#     conteudo_site = extrair_conteudo_site("https://www.jovemprogramador.com.br")
#     imagens_info = extrair_dados_imagens("https://www.jovemprogramador.com.br")

#     # Formata informações das imagens
#     imagens_texto = "\n".join([
#         f"- Imagem: {img.get('alt', 'Sem descrição disponível')}. "
#         f"Título: {img.get('title', 'sem título')}. "
#         f"Legenda: {img.get('legenda', 'sem legenda')}."
#         for img in imagens_info
#     ])

#     # Constrói o prompt
#     prompt = f"""
#     Você é um assistente especializado no site Jovem Programador (https://www.jovemprogramador.com.br).
#     Responda APENAS com base nas informações desse site.
#     Caso a pergunta não esteja relacionada, informe que só pode responder sobre o site Jovem Programador.

#     Conteúdo do site:
#     {conteudo_site}

#     Informações sobre imagens:
#     {imagens_texto}

#     Pergunta do usuário:
#     {pergunta}
#     """

#     try:
#         resposta = model.generate_content(prompt)
#         texto_resposta = resposta.text.strip()
#     except Exception as e:
#         texto_resposta = f"Ocorreu um erro ao gerar a resposta: {e}"

#     # Resposta de fallback
#     if not texto_resposta or len(texto_resposta) < 20:
#         texto_resposta = (
#             "Não encontrei informações suficientes no site Jovem Programador "
#             "para responder a essa pergunta."
#         )

#     return texto_resposta

# # === 4️⃣ ROTAS ===
# @app.route('/')
# def index():
#     """Serve o arquivo HTML principal"""
#     return send_from_directory('static', 'index.html')

# @app.route("/perguntar", methods=["POST"])
# def perguntar():
#     """Rota principal do chatbot"""
#     dados = request.json
#     pergunta = dados.get("pergunta", "").strip()

#     # Validação de pergunta vazia
#     if not pergunta:
#         return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

#     # Verifica respostas automáticas
#     resposta_automatica = verificar_resposta_automatica(pergunta)
#     if resposta_automatica:
#         return jsonify({"resposta": resposta_automatica})

#     # Valida tema da pergunta
#     if not validar_tema_pergunta(pergunta):
#         return jsonify({
#             "resposta": (
#                 "Posso responder apenas sobre o site Jovem Programador. "
#                 "Por favor, envie uma pergunta relacionada a ele."
#             )
#         })

#     # Gera resposta usando AI
#     resposta = gerar_resposta_gemini(pergunta)
#     return jsonify({"resposta": resposta})

# @app.route('/health')
# def health():
#     """Health check para o Render"""
#     return jsonify({"status": "healthy"}), 200

# # === 5️⃣ EXECUÇÃO ===
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(debug=False, host="0.0.0.0", port=port)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++






 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

# 

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# === 1️⃣ Carrega a chave da API ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

genai.configure(api_key=api_key)

# === 2️⃣ Inicializa o Flask ===
app = Flask(__name__)
CORS(app)

# === 3️⃣ Configura o modelo ===
model = genai.GenerativeModel("gemini-2.0-flash")

# === 4️⃣ Funções auxiliares ===
def extrair_conteudo_site(url: str) -> str:
    """Extrai texto do site Jovem Programador."""
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception:
        return "Erro ao acessar o site Jovem Programador."

def extrair_dados_imagens(url: str):
    """Extrai informações das imagens do site com atributos de acessibilidade."""
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, "html.parser")

        imagens = []
        for figura in soup.find_all("figure"):
            img = figura.find("img")
            legenda = figura.find("figcaption")
            if img:
                imagens.append({
                    "src": img.get("src"),
                    "alt": img.get("alt"),
                    "title": img.get("title"),
                    "legenda": legenda.get_text(strip=True) if legenda else None
                })

        for img in soup.find_all("img"):
            if not any(img.get("src") == i["src"] for i in imagens):
                imagens.append({
                    "src": img.get("src"),
                    "alt": img.get("alt"),
                    "title": img.get("title"),
                    "legenda": None
                })
        return imagens
    except Exception:
        return []

# === 5️⃣ Rotas ===
@app.route('/')
def home():
    """Serve o frontend interface.html"""
    return send_from_directory('static', 'interface.html')

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy"})

@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.json
    pergunta = dados.get("pergunta", "").strip()

    if not pergunta:
        return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

    # Respostas automáticas
    cumprimentos = {
        "oi": "Olá! Como posso ajudar você hoje?",
        "olá": "Olá! Tudo bem? Estou aqui para ajudar.",
        "bom dia": "Bom dia! Como posso ajudar você?",
        "boa tarde": "Boa tarde! Precisa de alguma informação?",
        "boa noite": "Boa noite! Como posso ajudar?",
        "e aí": "E aí! Tudo certo? Como posso ajudar?"
    }

    despedidas = {
        "tchau": "Até mais! Se precisar, estou aqui.",
        "até logo": "Até logo! Volte sempre 😊",
        "até mais": "Até mais! Foi um prazer ajudar.",
        "falou": "Falou! Qualquer coisa, me chame!",
        "obrigado": "Disponha! Sempre que precisar, estou por aqui.",
        "valeu": "Valeu! Conte comigo sempre!"
    }

    pergunta_lower = pergunta.lower()

    # Verifica cumprimentos
    for termo in cumprimentos:
        if termo in pergunta_lower:
            return jsonify({"resposta": cumprimentos[termo]})

    # Verifica despedidas
    for termo in despedidas:
        if termo in pergunta_lower:
            return jsonify({"resposta": despedidas[termo]})

    # Bloqueia perguntas fora do tema
    termos_permitidos = [
        "jovem programador", "curso", "inscrição", "site",
        "senac", "sesi", "empregabilidade", "ensino", "formação", "aprendizagem"
    ]

    if not any(palavra in pergunta_lower for palavra in termos_permitidos):
        return jsonify({
            "resposta": (
                "Posso responder apenas sobre o site Jovem Programador. "
                "Por favor, envie uma pergunta relacionada a ele."
            )
        })

    conteudo_site = extrair_conteudo_site("https://www.jovemprogramador.com.br")
    imagens_info = extrair_dados_imagens("https://www.jovemprogramador.com.br")

    imagens_texto = "\n".join([
        f"- Imagem: {img.get('alt', 'Sem descrição disponível')}. "
        f"Título: {img.get('title', 'sem título')}. "
        f"Legenda: {img.get('legenda', 'sem legenda')}."
        for img in imagens_info
    ])

    prompt = f"""
    Você é um assistente especializado no site Jovem Programador (https://www.jovemprogramador.com.br).
    Responda APENAS com base nas informações desse site.
    Caso a pergunta não esteja relacionada, informe que só pode responder sobre o site Jovem Programador.

    Conteúdo do site:
    {conteudo_site}

    Informações sobre imagens:
    {imagens_texto}

    Pergunta do usuário:
    {pergunta}
    """

    try:
        resposta = model.generate_content(prompt)
        texto_resposta = resposta.text.strip()
    except Exception as e:
        texto_resposta = f"Ocorreu um erro ao gerar a resposta: {e}"

    # Resposta de fallback
    if not texto_resposta or len(texto_resposta) < 20:
        texto_resposta = (
            "Não encontrei informações suficientes no site Jovem Programador "
            "para responder a essa pergunta."
        )

    return jsonify({"resposta": texto_resposta})

# === 6️⃣ Executa o servidor ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)