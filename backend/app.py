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

# === 🔹 ROTA PRINCIPAL COM FRONTEND INTEGRADO ===
@app.route('/')
def serve_frontend():
    """Serve o frontend diretamente no HTML"""
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chatbot Jovem Programador</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1a002b, #24024e);
                color: white;
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
            }
            .header h1 {
                font-size: 2.5rem;
                background: linear-gradient(135deg, #bb6afc, #8c44fa);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                margin-bottom: 10px;
            }
            .header p {
                color: #e2e2e2;
                font-size: 1.1rem;
            }
            .chat-container {
                background: rgba(187, 106, 252, 0.08);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                border: 1px solid rgba(187, 106, 252, 0.3);
                overflow: hidden;
                box-shadow: 0 25px 50px rgba(187, 106, 252, 0.15);
            }
            .chat-header {
                background: linear-gradient(135deg, #bb6afc, #8c44fa);
                padding: 20px;
                text-align: center;
            }
            .chat-header h2 {
                font-size: 1.5rem;
                font-weight: 600;
            }
            .chat-messages {
                height: 500px;
                overflow-y: auto;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            .message {
                max-width: 80%;
                padding: 15px 20px;
                border-radius: 20px;
                font-size: 1rem;
                line-height: 1.4;
            }
            .user-message {
                align-self: flex-end;
                background: linear-gradient(135deg, #bb6afc, #8c44fa);
                color: white;
                border-bottom-right-radius: 5px;
            }
            .bot-message {
                align-self: flex-start;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(187, 106, 252, 0.3);
                border-bottom-left-radius: 5px;
            }
            .chat-input {
                display: flex;
                padding: 20px;
                border-top: 1px solid rgba(187, 106, 252, 0.3);
                gap: 15px;
            }
            .chat-input input {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid rgba(187, 106, 252, 0.3);
                border-radius: 25px;
                font-size: 1rem;
                background: rgba(255, 255, 255, 0.05);
                color: white;
                outline: none;
            }
            .chat-input input:focus {
                border-color: #bb6afc;
                box-shadow: 0 0 0 3px rgba(187, 106, 252, 0.3);
            }
            .chat-input button {
                padding: 15px 30px;
                background: linear-gradient(135deg, #bb6afc, #8c44fa);
                color: white;
                border: none;
                border-radius: 25px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
                min-width: 120px;
            }
            .chat-input button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(187, 106, 252, 0.4);
            }
            .typing {
                color: #bb6afc;
                font-style: italic;
                padding: 10px 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Chatbot Jovem Programador</h1>
                <p>Assistente virtual para informações sobre cursos gratuitos de programação</p>
            </div>
            
            <div class="chat-container">
                <div class="chat-header">
                    <h2>💬 Assistente Virtual</h2>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot-message">
                        👋 Olá! Sou o assistente do Jovem Programador. 
                        Posso ajudar com informações sobre cursos gratuitos de programação! 
                        Pergunte sobre Python, JavaScript, React ou como se inscrever.
                    </div>
                </div>
                
                <div class="chat-input">
                    <input type="text" id="userInput" placeholder="Digite sua pergunta sobre programação...">
                    <button onclick="sendMessage()">
                        <i class="fas fa-paper-plane"></i> Enviar
                    </button>
                </div>
            </div>
        </div>

        <script>
            const chatMessages = document.getElementById('chatMessages');
            const userInput = document.getElementById('userInput');

            function addMessage(message, isUser = false) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                messageDiv.textContent = message;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            async function sendMessage() {
                const message = userInput.value.trim();
                if (!message) return;

                // Adiciona mensagem do usuário
                addMessage(message, true);
                userInput.value = '';

                // Mostra que está digitando
                const typingDiv = document.createElement('div');
                typingDiv.className = 'typing';
                typingDiv.textContent = 'Digitando...';
                typingDiv.id = 'typingIndicator';
                chatMessages.appendChild(typingDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                try {
                    const response = await fetch('/perguntar', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({pergunta: message})
                    });
                    
                    // Remove "digitando..."
                    document.getElementById('typingIndicator')?.remove();
                    
                    const data = await response.json();
                    addMessage(data.resposta);
                    
                } catch (error) {
                    // Remove "digitando..."
                    document.getElementById('typingIndicator')?.remove();
                    
                    addMessage('❌ Erro de conexão. Tente novamente.');
                    console.error('Erro:', error);
                }
            }

            // Enter key support
            userInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });

            // Foco no input
            userInput.focus();
        </script>
    </body>
    </html>
    '''

# === 🔹 ROTA HEALTH CHECK ===
@app.route('/health')
def health_check():
    """Rota de verificação de saúde"""
    return jsonify({
        "status": "healthy",
        "service": "Chatbot Jovem Programador"
    })

# === 5️⃣ ROTA PRINCIPAL DO CHAT (NÃO MODIFICADA) ===
@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.json
    pergunta = dados.get("pergunta", "").strip()

    if not pergunta:
        return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

    # ===========================================================================================
    # ✅  RESPOSTAS AUTOMÁTICAS PARA CUMPRIMENTOS E DESPEDIDAS
    # ===========================================================================================

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

    # ✔ Verifica cumprimentos
    for termo in cumprimentos:
        if termo in pergunta_lower:
            return jsonify({"resposta": cumprimentos[termo]})

    # ✔ Verifica despedidas
    for termo in despedidas:
        if termo in pergunta_lower:
            return jsonify({"resposta": despedidas[termo]})

    # ===========================================================================================

    # 🚫 Bloqueia perguntas fora do tema
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

    # Resposta de fallback acessível
    if not texto_resposta or len(texto_resposta) < 20:
        texto_resposta = (
            "Não encontrei informações suficientes no site Jovem Programador "
            "para responder a essa pergunta."
        )

    return jsonify({"resposta": texto_resposta})

# === 6️⃣ Executa o servidor ===
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# import requests
# from bs4 import BeautifulSoup

# # === 1️⃣ Carrega a chave da API ===
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

# genai.configure(api_key=api_key)

# # === 2️⃣ Inicializa o Flask ===
# app = Flask(__name__)
# CORS(app)

# # === 3️⃣ Configura o modelo ===
# model = genai.GenerativeModel("gemini-2.0-flash")

# # === 4️⃣ Funções auxiliares ===
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

# # === 🔹 ROTA PARA SERVIR FRONTEND ===
# @app.route('/')
# def serve_frontend():
#     """Serve a página principal do frontend"""
#     try:
#         return send_from_directory('../frontend', 'interface.html')
#     except:
#         return jsonify({
#             "mensagem": "🤖 Chatbot Jovem Programador API",
#             "status": "online", 
#             "uso": "Envie POST para /perguntar com {'pergunta': 'sua pergunta'}",
#             "frontend": "Interface não encontrada, mas a API está funcionando!"
#         })

# # === 🔹 ROTA HEALTH CHECK ===
# @app.route('/health')
# def health_check():
#     """Rota de verificação de saúde"""
#     return jsonify({
#         "status": "healthy",
#         "service": "Chatbot Jovem Programador"
#     })

# # === 🔹 ROTA PARA ARQUIVOS ESTÁTICOS ===
# @app.route('/<path:path>')
# def serve_static(path):
#     """Serve arquivos estáticos (CSS, JS, imagens)"""
#     try:
#         return send_from_directory('../frontend', path)
#     except:
#         return jsonify({"error": "Arquivo não encontrado"}), 404

# # === 5️⃣ ROTA PRINCIPAL DO CHAT (NÃO MODIFICADA) ===
# @app.route("/perguntar", methods=["POST"])
# def perguntar():
#     dados = request.json
#     pergunta = dados.get("pergunta", "").strip()

#     if not pergunta:
#         return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

#     # ===========================================================================================
#     # ✅  RESPOSTAS AUTOMÁTICAS PARA CUMPRIMENTOS E DESPEDIDAS
#     # ===========================================================================================

#     cumprimentos = {
#         "oi": "Olá! Como posso ajudar você hoje?",
#         "olá": "Olá! Tudo bem? Estou aqui para ajudar.",
#         "bom dia": "Bom dia! Como posso ajudar você?",
#         "boa tarde": "Boa tarde! Precisa de alguma informação?",
#         "boa noite": "Boa noite! Como posso ajudar?",
#         "e aí": "E aí! Tudo certo? Como posso ajudar?"
#     }

#     despedidas = {
#         "tchau": "Até mais! Se precisar, estou aqui.",
#         "até logo": "Até logo! Volte sempre 😊",
#         "até mais": "Até mais! Foi um prazer ajudar.",
#         "falou": "Falou! Qualquer coisa, me chame!",
#         "obrigado": "Disponha! Sempre que precisar, estou por aqui.",
#         "valeu": "Valeu! Conte comigo sempre!"
#     }

#     pergunta_lower = pergunta.lower()

#     # ✔ Verifica cumprimentos
#     for termo in cumprimentos:
#         if termo in pergunta_lower:
#             return jsonify({"resposta": cumprimentos[termo]})

#     # ✔ Verifica despedidas
#     for termo in despedidas:
#         if termo in pergunta_lower:
#             return jsonify({"resposta": despedidas[termo]})

#     # ===========================================================================================

#     # 🚫 Bloqueia perguntas fora do tema
#     termos_permitidos = [
#         "jovem programador", "curso", "inscrição", "site",
#         "senac", "sesi", "empregabilidade", "ensino", "formação", "aprendizagem"
#     ]

#     if not any(palavra in pergunta_lower for palavra in termos_permitidos):
#         return jsonify({
#             "resposta": (
#                 "Posso responder apenas sobre o site Jovem Programador. "
#                 "Por favor, envie uma pergunta relacionada a ele."
#             )
#         })

#     conteudo_site = extrair_conteudo_site("https://www.jovemprogramador.com.br")
#     imagens_info = extrair_dados_imagens("https://www.jovemprogramador.com.br")

#     imagens_texto = "\n".join([
#         f"- Imagem: {img.get('alt', 'Sem descrição disponível')}. "
#         f"Título: {img.get('title', 'sem título')}. "
#         f"Legenda: {img.get('legenda', 'sem legenda')}."
#         for img in imagens_info
#     ])

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

#     # Resposta de fallback acessível
#     if not texto_resposta or len(texto_resposta) < 20:
#         texto_resposta = (
#             "Não encontrei informações suficientes no site Jovem Programador "
#             "para responder a essa pergunta."
#         )

#     return jsonify({"resposta": texto_resposta})

# # === 6️⃣ Executa o servidor ===
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# import requests
# from bs4 import BeautifulSoup

# # === 1️⃣ Carrega a chave da API ===
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

# genai.configure(api_key=api_key)

# # === 2️⃣ Inicializa o Flask ===
# app = Flask(__name__)
# CORS(app)

# # === 3️⃣ Configura o modelo ===
# model = genai.GenerativeModel("gemini-2.0-flash")

# # === 4️⃣ Funções auxiliares ===
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

# # === 5️⃣ Rota principal ===
# @app.route("/perguntar", methods=["POST"])
# def perguntar():
#     dados = request.json
#     pergunta = dados.get("pergunta", "").strip()

#     if not pergunta:
#         return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

#     # ===========================================================================================
#     # ✅  RESPOSTAS AUTOMÁTICAS PARA CUMPRIMENTOS E DESPEDIDAS
#     # ===========================================================================================

#     cumprimentos = {
#         "oi": "Olá! Como posso ajudar você hoje?",
#         "olá": "Olá! Tudo bem? Estou aqui para ajudar.",
#         "bom dia": "Bom dia! Como posso ajudar você?",
#         "boa tarde": "Boa tarde! Precisa de alguma informação?",
#         "boa noite": "Boa noite! Como posso ajudar?",
#         "e aí": "E aí! Tudo certo? Como posso ajudar?"
#     }

#     despedidas = {
#         "tchau": "Até mais! Se precisar, estou aqui.",
#         "até logo": "Até logo! Volte sempre 😊",
#         "até mais": "Até mais! Foi um prazer ajudar.",
#         "falou": "Falou! Qualquer coisa, me chame!",
#         "obrigado": "Disponha! Sempre que precisar, estou por aqui.",
#         "valeu": "Valeu! Conte comigo sempre!"
#     }

#     pergunta_lower = pergunta.lower()

#     # ✔ Verifica cumprimentos
#     for termo in cumprimentos:
#         if termo in pergunta_lower:
#             return jsonify({"resposta": cumprimentos[termo]})

#     # ✔ Verifica despedidas
#     for termo in despedidas:
#         if termo in pergunta_lower:
#             return jsonify({"resposta": despedidas[termo]})

#     # ===========================================================================================

#     # 🚫 Bloqueia perguntas fora do tema
#     termos_permitidos = [
#         "jovem programador", "curso", "inscrição", "site",
#         "senac", "sesi", "empregabilidade", "ensino", "formação", "aprendizagem"
#     ]

#     if not any(palavra in pergunta_lower for palavra in termos_permitidos):
#         return jsonify({
#             "resposta": (
#                 "Posso responder apenas sobre o site Jovem Programador. "
#                 "Por favor, envie uma pergunta relacionada a ele."
#             )
#         })

#     conteudo_site = extrair_conteudo_site("https://www.jovemprogramador.com.br")
#     imagens_info = extrair_dados_imagens("https://www.jovemprogramador.com.br")

#     imagens_texto = "\n".join([
#         f"- Imagem: {img.get('alt', 'Sem descrição disponível')}. "
#         f"Título: {img.get('title', 'sem título')}. "
#         f"Legenda: {img.get('legenda', 'sem legenda')}."
#         for img in imagens_info
#     ])

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

#     # Resposta de fallback acessível
#     if not texto_resposta or len(texto_resposta) < 20:
#         texto_resposta = (
#             "Não encontrei informações suficientes no site Jovem Programador "
#             "para responder a essa pergunta."
#         )

#     return jsonify({"resposta": texto_resposta})

# # === 6️⃣ Executa o servidor ===
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)











# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime

# # === 1️⃣ Carrega a chave da API ===
# load_dotenv()

# # ✅ ADICIONE ESTAS LINHAS - Fallback para produção
# api_key = os.getenv("GEMINI_API_KEY")

# # Se não encontrar no .env, tenta variável de ambiente do Render
# if not api_key:
#     api_key = os.environ.get("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("A chave GEMINI_API_KEY não foi encontrada")

# genai.configure(api_key=api_key)

# # === 2️⃣ Inicializa o Flask ===
# app = Flask(__name__)
# CORS(app)

# # === 3️⃣ Configura o modelo ===
# model = genai.GenerativeModel("gemini-2.0-flash")

# # === 4️⃣ Funções auxiliares ===
# def extrair_conteudo_site(url: str) -> str:
#     """Extrai texto do site Jovem Programador."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")
#         return soup.get_text(separator="\n", strip=True)
#     except Exception as e:
#         return f"Erro ao acessar o site: {str(e)}"

# def extrair_dados_imagens(url: str):
#     """Extrai informações das imagens do site com atributos de acessibilidade."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")

#         imagens = []
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

#         for img in soup.find_all("img"):
#             if not any(img.get("src") == i["src"] for i in imagens):
#                 imagens.append({
#                     "src": img.get("src"),
#                     "alt": img.get("alt"),
#                     "title": img.get("title"),
#                     "legenda": None
#                 })
#         return imagens
#     except Exception as e:
#         return {"erro": f"Erro ao extrair imagens: {str(e)}"}

# # === 5️⃣ Rota de saúde ===
# @app.route("/health", methods=["GET"])
# def health_check():
#     return jsonify({
#         "status": "online", 
#         "mensagem": "Servidor funcionando perfeitamente!",
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "modelo": "gemini-2.0-flash"
#     })

# # === 6️⃣ Rota principal do chatbot ===
# @app.route("/perguntar", methods=["POST"])
# def perguntar():
#     dados = request.json
#     pergunta = dados.get("pergunta", "").strip()

#     if not pergunta:
#         return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

#     # Respostas automáticas para cumprimentos
#     cumprimentos = {
#         "oi": "Olá! Sou o assistente do Jovem Programador. Como posso ajudar?",
#         "olá": "Olá! Sou o assistente do Jovem Programador. Em que posso ajudar?",
#         "ola": "Olá! Sou o assistente do Jovem Programador. Em que posso ajudar?",
#         "bom dia": "Bom dia! Sou o assistente do Jovem Programador. Como posso ajudar?",
#         "boa tarde": "Boa tarde! Sou o assistente do Jovem Programador. Precisa de alguma informação?",
#         "boa noite": "Boa noite! Sou o assistente do Jovem Programador. Como posso ajudar?",
#         "e aí": "Olá! Sou o assistente do Jovem Programador. Tudo bem?",
#         "eai": "Olá! Sou o assistente do Jovem Programador. Tudo bem?"
#     }

#     despedidas = {
#         "tchau": "Até mais! Qualquer dúvida sobre o Jovem Programador, estou aqui.",
#         "até logo": "Até logo! Para mais informações sobre nossos cursos, visite jovemprogramador.com.br",
#         "até mais": "Até mais! Foi um prazer ajudar com o Jovem Programador.",
#         "falou": "Falou! Para inscrições no Jovem Programador, acesse nosso site.",
#         "obrigado": "Disponha! Continue explorando os cursos gratuitos do Jovem Programador.",
#         "valeu": "Por nada! Os cursos do Jovem Programador são todos gratuitos.",
#         "obrigada": "Disponha! Todos os cursos do Jovem Programador são gratuitos."
#     }

#     pergunta_lower = pergunta.lower()

#     # Verifica se é um cumprimento
#     if pergunta_lower in cumprimentos:
#         return jsonify({"resposta": cumprimentos[pergunta_lower]})
    
#     # Verifica se é uma despedida
#     if pergunta_lower in despedidas:
#         return jsonify({"resposta": despedidas[pergunta_lower]})

#     # Se não for cumprimento/despedida, usa o Gemini COM PROMPT RESTRITIVO
#     try:
#         # ✅ PROMPT RESTRITIVO ANTI-ALUCINAÇÃO
#         prompt_restritivo = f"""
# VOCÊ É UM ASSISTENTE EXCLUSIVO DO PROGRAMA JOVEM PROGRAMADOR DO SENAC SANTA CATARINA.

# INFORMAÇÕES VERIFICADAS QUE PODE FORNECER:
# - Programa GRATUITO do SENAC Santa Catarina
# - Cursos: Python, JavaScript, React, Node.js
# - Local: Santa Catarina, Brasil
# - Site: jovemprogramador.com.br
# - Email: contato@jovemprogramador.com
# - Benefícios: cursos gratuitos, certificados, comunidade
# - Processo seletivo: através do site oficial

# REGRAS ESTRITAS:
# 1. Use MÁXIMO 1 emoji por resposta
# 2. Seja objetivo (máximo 100 palavras)
# 3. NÃO invente informações sobre patrocinadores
# 4. NÃO forneça detalhes não verificados
# 5. Para perguntas fora do escopo: "Essa informação não está disponível no momento. Consulte o site oficial do Jovem Programador."

# PERGUNTA DO USUÁRIO: "{pergunta}"

# RESPONDA APENAS COM INFORMAÇÕES VERIFICADAS SOBRE O JOVEM PROGRAMADOR.
# SE NÃO SOUBER A RESPOSTA, DIGA PARA CONSULTAR O SITE OFICIAL.
# """

#         # ✅ CONFIGURAÇÃO PARA RESPOSTAS CURTAS
#         generation_config = {
#             "max_output_tokens": 150,  # ✅ Limita bastante o tamanho
#             "temperature": 0.3,        # ✅ Reduz criatividade para evitar invenções
#         }

#         # ✅ GERA RESPOSTA RESTRITA
#         resposta = model.generate_content(
#             prompt_restritivo,
#             generation_config=generation_config
#         )
        
#         # ✅ FILTRA EMOJIS EM EXCESSO
#         texto_resposta = resposta.text
#         texto_resposta = filtrar_excesso_emojis(texto_resposta)
        
#         return jsonify({"resposta": texto_resposta})
        
#     except Exception as e:
#         return jsonify({"resposta": f"Erro ao processar sua pergunta. Por favor, tente novamente."})

# # ✅ FUNÇÃO PARA FILTRAR EMOJIS EM EXCESSO
# def filtrar_excesso_emojis(texto):
#     """Remove sequências longas de emojis, mantendo no máximo 2 por resposta"""
#     import re
    
#     # Encontra todos os emojis
#     emojis = re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]', texto)
    
#     # Se tiver mais de 2 emojis, remove os extras
#     if len(emojis) > 2:
#         # Mantém apenas os 2 primeiros emojis encontrados
#         emojis_permitidos = emojis[:2]
#         # Remove todos os emojis e depois adiciona os permitidos no final
#         texto_sem_emojis = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]', '', texto)
#         texto_filtrado = texto_sem_emojis.strip() + ' ' + ''.join(emojis_permitidos)
#         return texto_filtrado
    
#     return texto

# # === 7️⃣ Rota para extrair conteúdo de sites ===
# @app.route("/extrair-site", methods=["POST"])
# def extrair_site():
#     dados = request.json
#     url = dados.get("url", "").strip()
    
#     if not url:
#         return jsonify({"erro": "URL não fornecida"})
    
#     conteudo = extrair_conteudo_site(url)
#     return jsonify({
#         "url": url,
#         "conteudo": conteudo[:1000] + "..." if len(conteudo) > 1000 else conteudo,
#         "tamanho_total": len(conteudo)
#     })

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

# # === 🔄 ROTAS PARA FRONTEND ===
# from flask import send_from_directory

# # Rota principal - SERVIR O FRONTEND
# @app.route("/")
# def home():
#     try:
#         return send_from_directory('frontend', 'interface.html')
#     except:
#         return jsonify({
#             "mensagem": "Bem-vindo ao Chatbot Jovem Programador!",
#             "aviso": "Frontend não encontrado, usando API",
#             "rotas_disponiveis": {
#                 "GET /health": "Status do servidor",
#                 "POST /perguntar": "Fazer perguntas ao chatbot", 
#                 "POST /extrair-site": "Extrair conteúdo de sites",
#                 "POST /analisar-imagens": "Analisar imagens de sites"
#             }
#         })

# # Rota para arquivos estáticos
# @app.route('/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('frontend', filename)

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
#     print("   GET  / - Interface web")
#     print("=" * 50)
    
#     # ✅ LINHA MODIFICADA - Agora usa a porta dinâmica
#     app.run(debug=False, host="0.0.0.0", port=port)

   # 1 projeto completo com as alterações solicitadas:

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime

# # === 1️⃣ Carrega a chave da API ===
# # === 1️⃣ Carrega a chave da API ===
# load_dotenv()

# # ✅ ADICIONE ESTAS LINHAS - Fallback para produção
# api_key = os.getenv("GEMINI_API_KEY")

# # Se não encontrar no .env, tenta variável de ambiente do Render
# if not api_key:
#     api_key = os.environ.get("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("A chave GEMINI_API_KEY não foi encontrada")

# genai.configure(api_key=api_key)

# # Código original:

# # load_dotenv()
# # api_key = os.getenv("GEMINI_API_KEY")

# # if not api_key:
# #     raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

# # genai.configure(api_key=api_key)

# # === 2️⃣ Inicializa o Flask ===
# app = Flask(__name__)
# CORS(app)

# # === 3️⃣ Configura o modelo ===
# model = genai.GenerativeModel("gemini-2.0-flash")

# # === 4️⃣ Funções auxiliares ===
# def extrair_conteudo_site(url: str) -> str:
#     """Extrai texto do site Jovem Programador."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")
#         return soup.get_text(separator="\n", strip=True)
#     except Exception as e:
#         return f"Erro ao acessar o site: {str(e)}"

# def extrair_dados_imagens(url: str):
#     """Extrai informações das imagens do site com atributos de acessibilidade."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")

#         imagens = []
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

#         for img in soup.find_all("img"):
#             if not any(img.get("src") == i["src"] for i in imagens):
#                 imagens.append({
#                     "src": img.get("src"),
#                     "alt": img.get("alt"),
#                     "title": img.get("title"),
#                     "legenda": None
#                 })
#         return imagens
#     except Exception as e:
#         return {"erro": f"Erro ao extrair imagens: {str(e)}"}

# # === 5️⃣ Rota de saúde ===
# @app.route("/health", methods=["GET"])
# def health_check():
#     return jsonify({
#         "status": "online", 
#         "mensagem": "Servidor funcionando perfeitamente!",
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "modelo": "gemini-2.0-flash"
#     })

# # === 6️⃣ Rota principal do chatbot ===
# @app.route("/perguntar", methods=["POST"])
# def perguntar():
#     dados = request.json
#     pergunta = dados.get("pergunta", "").strip()

#     if not pergunta:
#         return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

#     # Respostas automáticas para cumprimentos
#     cumprimentos = {
#         "oi": "Olá! Como posso ajudar você hoje?",
#         "olá": "Olá! Tudo bem? Estou aqui para ajudar.",
#         "ola": "Olá! Tudo bem? Estou aqui para ajudar.",
#         "bom dia": "Bom dia! Como posso ajudar você?",
#         "boa tarde": "Boa tarde! Precisa de alguma informação?",
#         "boa noite": "Boa noite! Como posso ajudar?",
#         "e aí": "E aí! Tudo certo? Como posso ajudar?",
#         "eai": "E aí! Tudo certo? Como posso ajudar?"
#     }

#     despedidas = {
#         "tchau": "Até mais! Se precisar, estou aqui.",
#         "até logo": "Até logo! Volte sempre 😊",
#         "até mais": "Até mais! Foi um prazer ajudar.",
#         "falou": "Falou! Qualquer coisa, me chame!",
#         "obrigado": "Disponha! Sempre que precisar, estou por aqui.",
#         "valeu": "Valeu! Conte comigo sempre!",
#         "obrigada": "Disponha! Fico feliz em ajudar!"
#     }

#     pergunta_lower = pergunta.lower()

#     # Verifica se é um cumprimento
#     if pergunta_lower in cumprimentos:
#         return jsonify({"resposta": cumprimentos[pergunta_lower]})
    
#     # Verifica se é uma despedida
#     if pergunta_lower in despedidas:
#         return jsonify({"resposta": despedidas[pergunta_lower]})

#     # Se não for cumprimento/despedida, usa o Gemini COM RESPOSTAS OBJETIVAS
#     try:
#         # ✅ PROMPT OTIMIZADO PARA RESPOSTAS CURTAS
#         prompt_objetivo = f"""
# Você é um assistente do Jovem Programador. Seja DIRETO e OBJETIVO.

# 📌 REGRAS:
# • Máximo 150 palavras
# • 1-2 parágrafos no máximo
# • Foco no essencial
# • Linguagem clara e prática
# • Use 🎯 emojis estratégicos

# PERGUNTA: {pergunta}

# 💡 Responda de forma CONCISA como em uma conversa rápida!
# """

#         # ✅ CONFIGURAÇÃO PARA RESPOSTAS CURTAS
#         generation_config = {
#             "max_output_tokens": 300,  # ✅ Limita tamanho
#             "temperature": 0.7,
#         }

#         # ✅ GERA RESPOSTA OTIMIZADA
#         resposta = model.generate_content(
#             prompt_objetivo,
#             generation_config=generation_config
#         )
        
#         return jsonify({"resposta": resposta.text})
        
#     except Exception as e:
#         return jsonify({"resposta": f"Erro ao processar sua pergunta: {str(e)}"})

# # === 7️⃣ Rota para extrair conteúdo de sites ===
# @app.route("/extrair-site", methods=["POST"])
# def extrair_site():
#     dados = request.json
#     url = dados.get("url", "").strip()
    
#     if not url:
#         return jsonify({"erro": "URL não fornecida"})
    
#     conteudo = extrair_conteudo_site(url)
#     return jsonify({
#         "url": url,
#         "conteudo": conteudo[:1000] + "..." if len(conteudo) > 1000 else conteudo,
#         "tamanho_total": len(conteudo)
#     })
# # Essa foi a nova rota adicionada para analisar imagens de sites

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

# # === 🔄 ROTAS PARA FRONTEND ===
# from flask import send_from_directory

# # Rota principal - SERVIR O FRONTEND
# @app.route("/")
# def home():
#     try:
#         return send_from_directory('frontend', 'interface.html')
#     except:
#         return jsonify({
#             "mensagem": "Bem-vindo ao Chatbot Jovem Programador!",
#             "aviso": "Frontend não encontrado, usando API",
#             "rotas_disponiveis": {
#                 "GET /health": "Status do servidor",
#                 "POST /perguntar": "Fazer perguntas ao chatbot", 
#                 "POST /extrair-site": "Extrair conteúdo de sites",
#                 "POST /analisar-imagens": "Analisar imagens de sites"
#             }
#         })

# # Rota para arquivos estáticos
# @app.route('/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('frontend', filename)

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
#     print("   GET  / - Interface web")
#     print("=" * 50)
    
#     # ✅ LINHA MODIFICADA - Agora usa a porta dinâmica
#     app.run(debug=False, host="0.0.0.0", port=port)

