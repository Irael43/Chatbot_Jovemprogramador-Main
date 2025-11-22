from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# === 1️⃣ Carrega a chave da API ===
# === 1️⃣ Carrega a chave da API ===
load_dotenv()

# ✅ ADICIONE ESTAS LINHAS - Fallback para produção
api_key = os.getenv("GEMINI_API_KEY")

# Se não encontrar no .env, tenta variável de ambiente do Render
if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada")

genai.configure(api_key=api_key)

# Código original:

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

# genai.configure(api_key=api_key)

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
    except Exception as e:
        return f"Erro ao acessar o site: {str(e)}"

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
    except Exception as e:
        return {"erro": f"Erro ao extrair imagens: {str(e)}"}

# === 5️⃣ Rota de saúde ===
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online", 
        "mensagem": "Servidor funcionando perfeitamente!",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modelo": "gemini-2.0-flash"
    })

# === 6️⃣ Rota principal do chatbot ===
@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.json
    pergunta = dados.get("pergunta", "").strip()

    if not pergunta:
        return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

    # Respostas automáticas para cumprimentos
    cumprimentos = {
        "oi": "Olá! Como posso ajudar você hoje?",
        "olá": "Olá! Tudo bem? Estou aqui para ajudar.",
        "ola": "Olá! Tudo bem? Estou aqui para ajudar.",
        "bom dia": "Bom dia! Como posso ajudar você?",
        "boa tarde": "Boa tarde! Precisa de alguma informação?",
        "boa noite": "Boa noite! Como posso ajudar?",
        "e aí": "E aí! Tudo certo? Como posso ajudar?",
        "eai": "E aí! Tudo certo? Como posso ajudar?"
    }

    despedidas = {
        "tchau": "Até mais! Se precisar, estou aqui.",
        "até logo": "Até logo! Volte sempre 😊",
        "até mais": "Até mais! Foi um prazer ajudar.",
        "falou": "Falou! Qualquer coisa, me chame!",
        "obrigado": "Disponha! Sempre que precisar, estou por aqui.",
        "valeu": "Valeu! Conte comigo sempre!",
        "obrigada": "Disponha! Fico feliz em ajudar!"
    }

    pergunta_lower = pergunta.lower()

    # Verifica se é um cumprimento
    if pergunta_lower in cumprimentos:
        return jsonify({"resposta": cumprimentos[pergunta_lower]})
    
    # Verifica se é uma despedida
    if pergunta_lower in despedidas:
        return jsonify({"resposta": despedidas[pergunta_lower]})

    # Se não for cumprimento/despedida, usa o Gemini COM RESPOSTAS OBJETIVAS
    try:
        # ✅ PROMPT OTIMIZADO PARA RESPOSTAS CURTAS
        prompt_objetivo = f"""
Você é um assistente do Jovem Programador. Seja DIRETO e OBJETIVO.

📌 REGRAS:
• Máximo 150 palavras
• 1-2 parágrafos no máximo
• Foco no essencial
• Linguagem clara e prática
• Use 🎯 emojis estratégicos

PERGUNTA: {pergunta}

💡 Responda de forma CONCISA como em uma conversa rápida!
"""

        # ✅ CONFIGURAÇÃO PARA RESPOSTAS CURTAS
        generation_config = {
            "max_output_tokens": 300,  # ✅ Limita tamanho
            "temperature": 0.7,
        }

        # ✅ GERA RESPOSTA OTIMIZADA
        resposta = model.generate_content(
            prompt_objetivo,
            generation_config=generation_config
        )
        
        return jsonify({"resposta": resposta.text})
        
    except Exception as e:
        return jsonify({"resposta": f"Erro ao processar sua pergunta: {str(e)}"})

# === 7️⃣ Rota para extrair conteúdo de sites ===
@app.route("/extrair-site", methods=["POST"])
def extrair_site():
    dados = request.json
    url = dados.get("url", "").strip()
    
    if not url:
        return jsonify({"erro": "URL não fornecida"})
    
    conteudo = extrair_conteudo_site(url)
    return jsonify({
        "url": url,
        "conteudo": conteudo[:1000] + "..." if len(conteudo) > 1000 else conteudo,
        "tamanho_total": len(conteudo)
    })
# Essa foi a nova rota adicionada para analisar imagens de sites

# === 8️⃣ Rota para analisar imagens de sites ===
@app.route("/analisar-imagens", methods=["POST"])
def analisar_imagens():
    dados = request.json
    url = dados.get("url", "").strip()
    
    if not url:
        return jsonify({"erro": "URL não fornecida"})
    
    imagens = extrair_dados_imagens(url)
    return jsonify({
        "url": url,
        "total_imagens": len(imagens),
        "imagens": imagens
    })

# === 🔄 ROTAS PARA FRONTEND ===
from flask import send_from_directory

# Rota principal - SERVIR O FRONTEND
@app.route("/")
def home():
    try:
        return send_from_directory('frontend', 'interface.html')
    except:
        return jsonify({
            "mensagem": "Bem-vindo ao Chatbot Jovem Programador!",
            "aviso": "Frontend não encontrado, usando API",
            "rotas_disponiveis": {
                "GET /health": "Status do servidor",
                "POST /perguntar": "Fazer perguntas ao chatbot", 
                "POST /extrair-site": "Extrair conteúdo de sites",
                "POST /analisar-imagens": "Analisar imagens de sites"
            }
        })

# Rota para arquivos estáticos
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

# === 🔟 Inicia o servidor ===
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Chatbot Jovem Programador Iniciando...")
    print("=" * 50)
    print("✅ API Key carregada com sucesso")
    
    # ✅ LINHA ADICIONADA - Detecta se é produção ou desenvolvimento
    port = int(os.environ.get("PORT", 5000))
    
    print(f"🚀 Servidor rodando em: http://0.0.0.0:{port}")
    print("📋 Rotas disponíveis:")
    print("   GET  /health")
    print("   POST /perguntar")
    print("   POST /extrair-site") 
    print("   POST /analisar-imagens")
    print("   GET  / - Interface web")
    print("=" * 50)
    
    # ✅ LINHA MODIFICADA - Agora usa a porta dinâmica
    app.run(debug=False, host="0.0.0.0", port=port)

# # === 8️⃣ Rota para analisar imagens de sites ===
# @app.route("/analisar-imagens", methods=["POST"])
# def analisar_imagens():
#     dados = request.json
#     url = dados.get("url", "").strip()
    
#     if not url:
#         return jsonify({"erro": "URL não fornecida"})
    
#     imagens = extrair_dados_imagens(url)
#     return jsonify({
#         "url": url,
#         "total_imagens": len(imagens),
#         "imagens": imagens
#     })

# # === 9️⃣ Rota raiz ===
# @app.route("/")
# def home():
#     return jsonify({
#         "mensagem": "Bem-vindo ao Chatbot Jovem Programador!",
#         "rotas_disponiveis": {
#             "GET /health": "Status do servidor",
#             "POST /perguntar": "Fazer perguntas ao chatbot",
#             "POST /extrair-site": "Extrair conteúdo de sites",
#             "POST /analisar-imagens": "Analisar imagens de sites"
#         }
#     })

# # === 🔟 Inicia o servidor ===
# if __name__ == "__main__":
#     print("=" * 50)
#     print("🤖 Chatbot Jovem Programador Iniciando...")
#     print("=" * 50)
#     print("✅ API Key carregada com sucesso")
    
#     # ✅ LINHA ADICIONADA - Detecta se é produção ou desenvolvimento
#     port = int(os.environ.get("PORT", 5000))
    
#     print(f"🚀 Servidor rodando em: http://0.0.0.0:{port}")
#     print("📋 Rotas disponíveis:")
#     print("   GET  /health")
#     print("   POST /perguntar")
#     print("   POST /extrair-site") 
#     print("   POST /analisar-imagens")
#     print("=" * 50)
    
#     # ✅ LINHA MODIFICADA - Agora usa a porta dinâmica
#     app.run(debug=False, host="0.0.0.0", port=port)


