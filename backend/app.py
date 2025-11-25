
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

# === 4️⃣ BANCO DE INFORMAÇÕES COMPLETO DO JOVEM PROGRAMADOR ===
INFORMACOES_JOVEM_PROGRAMADOR = """
INFORMAÇÕES OFICIAIS DO JOVEM PROGRAMADOR 2026:

🏢 SOBRE O PROGRAMA:
- Programa de capacitação tecnológica para formação de PROGRAMADORES
- Idade mínima: 16 anos
- Escolaridade: Ensino Médio cursando ou completo
- Residência: Cidades beneficiadas ou vizinhas
- Iniciativa: SEPROSC (Sindicato das Empresas de TI de SC)
- Realização: SENAC Santa Catarina

🎯 OBJETIVO:
Formar jovens para atuar em empresas de TI de Santa Catarina, independente da localização.

🏙️ CIDADES ATENDIDAS 2026:
Araranguá, Blumenau, Biguaçu, Brusque, Caçador, Canoinhas, Chapecó, Concórdia, 
Criciúma, Curitibanos, Florianópolis, Fraiburgo, Jaraguá do Sul, Joaçaba, 
Joinville, Lages, Palhoça, Porto União, Rio do Sul, São Miguel do Oeste, 
Tubarão, Videira e Xanxerê.

📚 ESTRUTURA DO CURSO:
Módulo I - 04 horas: Conceitos e Lógica
Módulo II - 200 horas: Programador de Sistemas  
Módulo III - 240 horas: Desenvolvimento Web com IA
TOTAL: 444 horas

🎓 MODALIDADE:
- Aulas HÍBRIDAS (presenciais e virtuais)
- Presencial: Unidades do SENAC nas 23 cidades
- Virtual: Plataforma online

💰 INVESTIMENTO:
- GRATUITO para renda familiar per capita ≤ 2 salários mínimos (PSG)
- Mensalidade acessível para demais casos
- Programa Senac de Gratuidade (PSG)

👥 VAGAS INCLUSIVAS:
- 6% das vagas reservadas para Pessoas com Deficiência (PcD)
- Documentação: Laudo médico com CID
- Acessibilidade garantida
- Turma exclusiva para mulheres na Faculdade Senac Palhoça

📅 CALENDÁRIO 2026:
- Inscrições: Abertas
- Workshop inicial: Fevereiro 2026
- Aulas: Segunda quinzena de Fevereiro 2026
- Processo seletivo: Workshop com atividade avaliativa

🔗 PROCESSO SELETIVO:
1. Inscrição online no site
2. Participação no workshop
3. Atividade avaliativa no workshop
4. Divulgação do resultado
5. Matrícula dos aprovados

📞 CONTATOS:
- WhatsApp: (49) 98858-3009
- Email: contato@jovemprogramador.com.br
- Site: https://www.jovemprogramador.com.br
- SEPROSC: seprosc@seprosc.com.br

🏢 ENDEREÇO SEPROSC:
Rua Antônio Treis, 607, Vorstadt, Blumenau/SC - CEP 89015-400

🤝 PARCEIROS:
ORGANIZADOR: SEPROSC
ENSINO: SENAC

🎯 PATROCINADORES:
Softplan, Hartsystem, Cloudpark, CB Sistemas, Senior, Grupo BST, Mobuss, Clube Associados

📢 APOIADORES:
Collabtech, Novale Hub, Gene, NSC TV, Sigma Park, Citeb, Inovale, Somar, Acate, 
Communitech, SESC, CIB, Orion, Amureltec

💼 EMPREGABILIDADE:
- Alta taxa de empregabilidade em TI
- Parcerias com empresas do setor
- Preparação para mercado de trabalho
- Oportunidades em todo Santa Catarina

🎮 HACKATHON 2025:
- Evento extracurricular online
- Desenvolvimento de soluções tecnológicas
- Premiação para melhores projetos
- Desafios reais do mercado

❓ PERGUNTAS FREQUENTES:

PERGUNTA: Tenho 15 anos, posso me inscrever?
RESPOSTA: Sim, se completar 16 anos até 20/02/2026.

PERGUNTA: Preciso ter experiência em programação?
RESPOSTA: Não, o programa é para iniciantes.

PERGUNTA: Quantas vagas são oferecidas?
RESPOSTA: Mais de 1.264 vagas em 2026.

PERGUNTA: O curso é totalmente online?
RESPOSTA: Não, é HÍBRIDO (presencial e virtual).

PERGUNTA: Como comprovar renda para gratuidade?
RESPOSTA: Somar renda familiar e dividir por membros da família.

PERGUNTA: Há vagas para pessoas de outras cidades?
RESPOSTA: Sim, desde que sejam cidades vizinhas às atendidas.

📋 DOCUMENTAÇÃO NECESSÁRIA:
- Documento de identidade
- Comprovante de residência
- Comprovante de escolaridade
- Para PcD: Laudo médico atualizado
- Para gratuidade: Comprovantes de renda familiar

🎓 CERTIFICAÇÃO:
- Certificado por módulo concluído
- Reconhecimento pelo mercado
- Requisitos: Frequência e aproveitamento
"""

# === 5️⃣ Funções auxiliares ===
def extrair_conteudo_site(url: str) -> str:
    """Extrai texto do site Jovem Programador."""
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, "html.parser")
        
        for script in soup(["script", "style"]):
            script.decompose()
            
        texto = soup.get_text(separator="\n", strip=True)
        return texto[:4000] if len(texto) > 4000 else texto
    except Exception as e:
        print(f"Erro ao acessar site: {e}")
        return ""

def obter_informacoes_completas():
    """Obtém informações do site + banco interno"""
    conteudo_site = extrair_conteudo_site("https://www.jovemprogramador.com.br")
    
    # Prioriza informações internas (mais organizadas)
    if not conteudo_site:
        return INFORMACOES_JOVEM_PROGRAMADOR
    else:
        return f"""
        INFORMAÇÕES ATUALIZADAS DO SITE:
        {conteudo_site[:2000]}
        
        BANCO DE INFORMAÇÕES OFICIAIS:
        {INFORMACOES_JOVEM_PROGRAMADOR}
        """

# === 6️⃣ Rotas ===
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
        "oi": "Olá! Sou o assistente do Jovem Programador 2026. Como posso ajudar? 😊",
        "olá": "Olá! Tudo bem? Estou aqui para tirar suas dúvidas sobre o programa Jovem Programador!",
        "bom dia": "Bom dia! Em que posso ajudar você sobre o Jovem Programador 2026?",
        "boa tarde": "Boa tarde! Precisa de informações sobre as inscrições 2026?",
        "boa noite": "Boa noite! Estou aqui para ajudar com suas dúvidas sobre o Jovem Programador.",
        "e aí": "E aí! Tudo certo? Como posso ajudar com o Jovem Programador 2026?"
    }

    despedidas = {
        "tchau": "Até mais! Lembre-se: inscrições abertas para 2026! WhatsApp (49) 98858-3009",
        "até logo": "Até logo! Espero ter ajudado. Inscrições: www.jovemprogramador.com.br 😊",
        "até mais": "Até mais! Foi um prazer ajudar. Dúvidas? WhatsApp (49) 98858-3009",
        "falou": "Falou! Qualquer dúvida sobre o Jovem Programador, me chame!",
        "obrigado": "Disponha! Para mais informações: WhatsApp (49) 98858-3009",
        "valeu": "Valeu! Inscrições 2026 abertas: www.jovemprogramador.com.br"
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

    # Obtém informações completas
    informacoes_completas = obter_informacoes_completas()

    prompt = f"""
    VOCÊ É UM ASSISTENTE ESPECIALIZADO NO JOVEM PROGRAMADOR 2026.

    INFORMAÇÕES OFICIAIS ATUALIZADAS:
    {informacoes_completas}

    REGRAS DE RESPOSTA:
    1. Responda APENAS sobre o Jovem Programador 2026
    2. Use as informações acima como fonte ÚNICA
    3. Seja PRECISO, ÚTIL e DIRETO
    4. Para dúvidas específicas, direcione para os contatos oficiais
    5. Mantenha o foco nas informações oficiais do programa

    PERGUNTA DO USUÁRIO: {pergunta}

    RESPOSTA (baseada apenas nas informações oficiais):
    """

    try:
        resposta = model.generate_content(prompt)
        texto_resposta = resposta.text.strip()
        
        # Garante resposta útil
        resposta_lower = texto_resposta.lower()
        if (len(texto_resposta) < 10 or 
            "não sei" in resposta_lower or 
            "não tenho" in resposta_lower):
            
            texto_resposta = "Para informações específicas sobre o Jovem Programador 2026, entre em contato: WhatsApp (49) 98858-3009 ou site www.jovemprogramador.com.br"
            
    except Exception as e:
        texto_resposta = "Para informações sobre o Jovem Programador 2026: WhatsApp (49) 98858-3009 ou www.jovemprogramador.com.br"

    return jsonify({"resposta": texto_resposta})

# === 7️⃣ Executa o servidor ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++






 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

# 

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

# # === 5️⃣ Rotas ===
# @app.route('/')
# def home():
#     """Serve o frontend interface.html"""
#     return send_from_directory('static', 'interface.html')

# @app.route('/health')
# def health():
#     """Health check"""
#     return jsonify({"status": "healthy"})

# @app.route("/perguntar", methods=["POST"])
# def perguntar():
#     dados = request.json
#     pergunta = dados.get("pergunta", "").strip()

#     if not pergunta:
#         return jsonify({"resposta": "Por favor, digite uma pergunta válida."})

#     # Respostas automáticas
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

#     # Verifica cumprimentos
#     for termo in cumprimentos:
#         if termo in pergunta_lower:
#             return jsonify({"resposta": cumprimentos[termo]})

#     # Verifica despedidas
#     for termo in despedidas:
#         if termo in pergunta_lower:
#             return jsonify({"resposta": despedidas[termo]})

#     # Bloqueia perguntas fora do tema
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

#     # Resposta de fallback
#     if not texto_resposta or len(texto_resposta) < 20:
#         texto_resposta = (
#             "Não encontrei informações suficientes no site Jovem Programador "
#             "para responder a essa pergunta."
#         )

#     return jsonify({"resposta": texto_resposta})

# # === 6️⃣ Executa o servidor ===
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))
#     app.run(debug=False, host="0.0.0.0", port=port)