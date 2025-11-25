
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

# # === 4️⃣ BANCO DE INFORMAÇÕES COMPLETO DO JOVEM PROGRAMADOR ===
# INFORMACOES_JOVEM_PROGRAMADOR = """
# INFORMAÇÕES OFICIAIS DO JOVEM PROGRAMADOR 2026:

# 🏢 SOBRE O PROGRAMA:
# - Programa de capacitação tecnológica para formação de PROGRAMADORES
# - Idade mínima: 16 anos
# - Escolaridade: Ensino Médio cursando ou completo
# - Residência: Cidades beneficiadas ou vizinhas
# - Iniciativa: SEPROSC (Sindicato das Empresas de TI de SC)
# - Realização: SENAC Santa Catarina

# 🎯 OBJETIVO:
# Formar jovens para atuar em empresas de TI de Santa Catarina, independente da localização.

# 🏙️ CIDADES ATENDIDAS 2026:
# Araranguá, Blumenau, Biguaçu, Brusque, Caçador, Canoinhas, Chapecó, Concórdia, 
# Criciúma, Curitibanos, Florianópolis, Fraiburgo, Jaraguá do Sul, Joaçaba, 
# Joinville, Lages, Palhoça, Porto União, Rio do Sul, São Miguel do Oeste, 
# Tubarão, Videira e Xanxerê.

# 📚 ESTRUTURA DO CURSO:
# Módulo I - 04 horas: Conceitos e Lógica
# Módulo II - 200 horas: Programador de Sistemas  
# Módulo III - 240 horas: Desenvolvimento Web com IA
# TOTAL: 444 horas

# 🎓 MODALIDADE:
# - Aulas HÍBRIDAS (presenciais e virtuais)
# - Presencial: Unidades do SENAC nas 23 cidades
# - Virtual: Plataforma online

# 💰 INVESTIMENTO:
# - GRATUITO para renda familiar per capita ≤ 2 salários mínimos (PSG)
# - Mensalidade acessível para demais casos
# - Programa Senac de Gratuidade (PSG)

# 👥 VAGAS INCLUSIVAS:
# - 6% das vagas reservadas para Pessoas com Deficiência (PcD)
# - Documentação: Laudo médico com CID
# - Acessibilidade garantida
# - Turma exclusiva para mulheres na Faculdade Senac Palhoça

# 📅 CALENDÁRIO 2026:
# - Inscrições: Abertas
# - Workshop inicial: Fevereiro 2026
# - Aulas: Segunda quinzena de Fevereiro 2026
# - Processo seletivo: Workshop com atividade avaliativa

# 🔗 PROCESSO SELETIVO:
# 1. Inscrição online no site
# 2. Participação no workshop
# 3. Atividade avaliativa no workshop
# 4. Divulgação do resultado
# 5. Matrícula dos aprovados

# 📞 CONTATOS:
# - WhatsApp: (49) 98858-3009
# - Email: contato@jovemprogramador.com.br
# - Site: https://www.jovemprogramador.com.br
# - SEPROSC: seprosc@seprosc.com.br

# 🏢 ENDEREÇO SEPROSC:
# Rua Antônio Treis, 607, Vorstadt, Blumenau/SC - CEP 89015-400

# 🤝 PARCEIROS:
# ORGANIZADOR: SEPROSC
# ENSINO: SENAC

# 🎯 PATROCINADORES:
# Softplan, Hartsystem, Cloudpark, CB Sistemas, Senior, Grupo BST, Mobuss, Clube Associados

# 📢 APOIADORES:
# Collabtech, Novale Hub, Gene, NSC TV, Sigma Park, Citeb, Inovale, Somar, Acate, 
# Communitech, SESC, CIB, Orion, Amureltec

# 💼 EMPREGABILIDADE:
# - Alta taxa de empregabilidade em TI
# - Parcerias com empresas do setor
# - Preparação para mercado de trabalho
# - Oportunidades em todo Santa Catarina

# 🎮 HACKATHON 2025:
# - Evento extracurricular online
# - Desenvolvimento de soluções tecnológicas
# - Premiação para melhores projetos
# - Desafios reais do mercado

# ❓ PERGUNTAS FREQUENTES:

# PERGUNTA: Tenho 15 anos, posso me inscrever?
# RESPOSTA: Sim, se completar 16 anos até 20/02/2026.

# PERGUNTA: Preciso ter experiência em programação?
# RESPOSTA: Não, o programa é para iniciantes.

# PERGUNTA: Quantas vagas são oferecidas?
# RESPOSTA: Mais de 1.264 vagas em 2026.

# PERGUNTA: O curso é totalmente online?
# RESPOSTA: Não, é HÍBRIDO (presencial e virtual).

# PERGUNTA: Como comprovar renda para gratuidade?
# RESPOSTA: Somar renda familiar e dividir por membros da família.

# PERGUNTA: Há vagas para pessoas de outras cidades?
# RESPOSTA: Sim, desde que sejam cidades vizinhas às atendidas.

# 📋 DOCUMENTAÇÃO NECESSÁRIA:
# - Documento de identidade
# - Comprovante de residência
# - Comprovante de escolaridade
# - Para PcD: Laudo médico atualizado
# - Para gratuidade: Comprovantes de renda familiar

# 🎓 CERTIFICAÇÃO:
# - Certificado por módulo concluído
# - Reconhecimento pelo mercado
# - Requisitos: Frequência e aproveitamento
# """

# # === 5️⃣ Funções auxiliares ===
# def extrair_conteudo_site(url: str) -> str:
#     """Extrai texto do site Jovem Programador."""
#     try:
#         resposta = requests.get(url, timeout=10)
#         resposta.raise_for_status()
#         soup = BeautifulSoup(resposta.text, "html.parser")
        
#         for script in soup(["script", "style"]):
#             script.decompose()
            
#         texto = soup.get_text(separator="\n", strip=True)
#         return texto[:4000] if len(texto) > 4000 else texto
#     except Exception as e:
#         print(f"Erro ao acessar site: {e}")
#         return ""

# def obter_informacoes_completas():
#     """Obtém informações do site + banco interno"""
#     conteudo_site = extrair_conteudo_site("https://www.jovemprogramador.com.br")
    
#     # Prioriza informações internas (mais organizadas)
#     if not conteudo_site:
#         return INFORMACOES_JOVEM_PROGRAMADOR
#     else:
#         return f"""
#         INFORMAÇÕES ATUALIZADAS DO SITE:
#         {conteudo_site[:2000]}
        
#         BANCO DE INFORMAÇÕES OFICIAIS:
#         {INFORMACOES_JOVEM_PROGRAMADOR}
#         """

# # === 6️⃣ Rotas ===
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
#         "oi": "Olá! Sou o assistente do Jovem Programador 2026. Como posso ajudar? 😊",
#         "olá": "Olá! Tudo bem? Estou aqui para tirar suas dúvidas sobre o programa Jovem Programador!",
#         "bom dia": "Bom dia! Em que posso ajudar você sobre o Jovem Programador 2026?",
#         "boa tarde": "Boa tarde! Precisa de informações sobre as inscrições 2026?",
#         "boa noite": "Boa noite! Estou aqui para ajudar com suas dúvidas sobre o Jovem Programador.",
#         "e aí": "E aí! Tudo certo? Como posso ajudar com o Jovem Programador 2026?"
#     }

#     despedidas = {
#         "tchau": "Até mais! Lembre-se: inscrições abertas para 2026! WhatsApp (49) 98858-3009",
#         "até logo": "Até logo! Espero ter ajudado. Inscrições: www.jovemprogramador.com.br 😊",
#         "até mais": "Até mais! Foi um prazer ajudar. Dúvidas? WhatsApp (49) 98858-3009",
#         "falou": "Falou! Qualquer dúvida sobre o Jovem Programador, me chame!",
#         "obrigado": "Disponha! Para mais informações: WhatsApp (49) 98858-3009",
#         "valeu": "Valeu! Inscrições 2026 abertas: www.jovemprogramador.com.br"
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

#     # Obtém informações completas
#     informacoes_completas = obter_informacoes_completas()

#     prompt = f"""
#     VOCÊ É UM ASSISTENTE ESPECIALIZADO NO JOVEM PROGRAMADOR 2026.

#     INFORMAÇÕES OFICIAIS ATUALIZADAS:
#     {informacoes_completas}

#     REGRAS DE RESPOSTA:
#     1. Responda APENAS sobre o Jovem Programador 2026
#     2. Use as informações acima como fonte ÚNICA
#     3. Seja PRECISO, ÚTIL e DIRETO
#     4. Para dúvidas específicas, direcione para os contatos oficiais
#     5. Mantenha o foco nas informações oficiais do programa

#     PERGUNTA DO USUÁRIO: {pergunta}

#     RESPOSTA (baseada apenas nas informações oficiais):
#     """

#     try:
#         resposta = model.generate_content(prompt)
#         texto_resposta = resposta.text.strip()
        
#         # Garante resposta útil
#         resposta_lower = texto_resposta.lower()
#         if (len(texto_resposta) < 10 or 
#             "não sei" in resposta_lower or 
#             "não tenho" in resposta_lower):
            
#             texto_resposta = "Para informações específicas sobre o Jovem Programador 2026, entre em contato: WhatsApp (49) 98858-3009 ou site www.jovemprogramador.com.br"
            
#     except Exception as e:
#         texto_resposta = "Para informações sobre o Jovem Programador 2026: WhatsApp (49) 98858-3009 ou www.jovemprogramador.com.br"

#     return jsonify({"resposta": texto_resposta})

# # === 7️⃣ Executa o servidor ===
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))
#     app.run(debug=False, host="0.0.0.0", port=port)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++






 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re

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

🎯 OBJETETIVO:
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

# === 5️⃣ SISTEMA DE REFORMULAÇÃO E CONFIRMAÇÃO ===
def analisar_e_reformular_pergunta(pergunta: str) -> dict:
    """Analisa a pergunta e reformula se necessário, retornando contexto"""
    pergunta_lower = pergunta.lower()
    
    # Termos relacionados ao Jovem Programador
    termos_jovem_programador = [
        "jovem programador", "curso", "inscrição", "senac", "seprosc",
        "cidade", "cidades", "município", "idade", "valor", "custo",
        "gratuito", "grátis", "vagas", "vaga", "requisito", "documento",
        "aula", "horas", "dura", "duração", "modalidade", "presencial",
        "online", "híbrido", "workshop", "processo seletivo", "matrícula",
        "certificado", "empregabilidade", "hackathon", "pcD", "deficiência",
        "mulheres", "turma feminina", "acessibilidade", "whatsapp", "contato",
        "site", "email", "blumenau", "florianópolis", "joinville", "chapecó"
    ]
    
    # Verifica se a pergunta está relacionada ao Jovem Programador
    pergunta_relacionada = any(termo in pergunta_lower for termo in termos_jovem_programador)
    
    # Reformulações comuns
    reformulacoes = {
        r"\b(em quecidades|onde tem|quais cidade|em que lugar)\b": "Em que cidades tem o Jovem Programador?",
        r"\b(quero saber|gostaria de|me fala|me diz)\b.*\b(cidade|local)\b": "Quais cidades têm o curso do Jovem Programador?",
        r"\b(precisa de|preciso ter|quais documento|o que precisa)\b": "Quais são os requisitos para participar?",
        r"\b(quanto custa|qual valor|é de graça|é gratuito)\b": "O Jovem Programador é gratuito?",
        r"\b(quantos anos|qual idade|menor de idade|posso com)\b": "Qual a idade mínima para participar?",
        r"\b(como faço|como me inscrevo|quero participar|quero entrar)\b": "Como faço para me inscrever no Jovem Programador?",
        r"\b(quanto tempo|quantas horas|dura quanto|qual carga)\b": "Quantas horas tem o curso completo?",
        r"\b(tem vaga|há vagas|ainda tem|consegue vaga)\b": "Ainda há vagas disponíveis para o Jovem Programador?",
        r"\b(onde fica|local do curso|onde é|endereço)\b": "Em quais cidades o Jovem Programador está disponível?",
        r"\b(o que é|o que faz|sobre o|explica)\b.*\b(jovem programador)\b": "O que é o Jovem Programador e como funciona?"
    }
    
    pergunta_reformulada = None
    for padrao, reformulacao in reformulacoes.items():
        if re.search(padrao, pergunta_lower):
            pergunta_reformulada = reformulacao
            break
    
    return {
        "original": pergunta,
        "reformulada": pergunta_reformulada,
        "relacionada": pergunta_relacionada,
        "precisa_confirmacao": pergunta_reformulada is not None and not pergunta_relacionada
    }

def gerar_resposta_com_confirmacao(analise_pergunta: dict, informacoes_completas: str) -> str:
    """Gera resposta com sistema de confirmação quando necessário"""
    
    if analise_pergunta["precisa_confirmacao"]:
        # Resposta pedindo confirmação
        return f"🤔 **Você quis dizer:** \"{analise_pergunta['reformulada']}\"?\n\nSe sim, confirme sua pergunta ou me diga se era outra coisa!"
    
    else:
        # Resposta normal usando Gemini
        prompt = f"""
        VOCÊ É UM ASSISTENTE ESPECIALIZADO NO JOVEM PROGRAMADOR 2026.

        INFORMAÇÕES OFICIAIS ATUALIZADAS:
        {informacoes_completas}

        PERGUNTA DO USUÁRIO: "{analise_pergunta['original']}"
        {"PERGUNTA REFORMULADA: " + analise_pergunta['reformulada'] if analise_pergunta['reformulada'] else ""}

        REGRAS DE RESPOSTA:
        1. Responda APENAS sobre o Jovem Programador 2026
        2. Seja PRECISO, ÚTIL e AMIGÁVEL
        3. Use as informações oficiais como fonte
        4. Se não souber algo específico, direcione para os contatos oficiais

        RESPOSTA (seja natural e direto):
        """

        try:
            resposta = model.generate_content(prompt)
            texto_resposta = resposta.text.strip()
            
            # Fallback para respostas muito genéricas
            if len(texto_resposta) < 15 or "não sei" in texto_resposta.lower():
                texto_resposta = "Para informações específicas sobre o Jovem Programador 2026, entre em contato: WhatsApp (49) 98858-3009 ou site www.jovemprogramador.com.br"
                
            return texto_resposta
            
        except Exception as e:
            return "Para informações sobre o Jovem Programador 2026: WhatsApp (49) 98858-3009 ou www.jovemprogramador.com.br"

# === 6️⃣ Funções auxiliares ===
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
    
    if not conteudo_site:
        return INFORMACOES_JOVEM_PROGRAMADOR
    else:
        return f"""
        INFORMAÇÕES ATUALIZADAS DO SITE:
        {conteudo_site[:2000]}
        
        BANCO DE INFORMAÇÕES OFICIAIS:
        {INFORMACOES_JOVEM_PROGRAMADOR}
        """

# === 7️⃣ Rotas ===
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

    # Analisa e reformula a pergunta
    analise_pergunta = analisar_e_reformular_pergunta(pergunta)
    
    # Obtém informações completas
    informacoes_completas = obter_informacoes_completas()

    # Gera resposta com sistema de confirmação
    resposta = gerar_resposta_com_confirmacao(analise_pergunta, informacoes_completas)

    return jsonify({"resposta": resposta})

# === 8️⃣ Executa o servidor ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)