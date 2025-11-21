# import streamlit as st
# import streamlit.components.v1 as components
# import requests
# from pathlib import Path
# import os

# # === Configuração da página ===
# st.set_page_config(
#     page_title="Chatbot Jovem Programador",
#     page_icon="💬",
#     layout="wide"
# )

# # === Caminho para os arquivos locais ===
# assets_path = Path(__file__).parent / "assets"

# # === Aplicar CSS com tolerância a erros de leitura ===
# try:
#     with open(assets_path / "style.css", "r", encoding="utf-8", errors="ignore") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# except Exception as e:
#     st.warning(f"Erro ao carregar o CSS: {e}")

# # === Cabeçalho acessível ===
# st.markdown("""
#     <h1 id="titulo" style="text-align:center; color:#C7A4FF;">
#         <span aria-hidden="true">🤖</span> Chatbot Jovem Programador
#     </h1>
#     <p style="text-align:center;">
#         Converse sobre o site Jovem Programador e receba respostas acessíveis em Libras.
#     </p>
# """, unsafe_allow_html=True)

# # === Exibir logo se existir ===
# logo_path = assets_path / "logo.png"
# if os.path.exists(logo_path):
#     st.image(str(logo_path), width=120, caption="Logo do projeto Jovem Programador")

# # === Histórico do chat ===
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # === Exibir mensagens anteriores com rótulos de acessibilidade ===
# for msg in st.session_state.messages:
#     avatar_file = "avatar-user.png" if msg["role"] == "user" else "avatar-original.png"
#     avatar_path = assets_path / avatar_file
#     role_label = "Você disse:" if msg["role"] == "user" else "Chatbot respondeu:"
#     with st.chat_message(msg["role"], avatar=str(avatar_path)):
#         st.markdown(f"<p aria-label='{role_label}'>{msg['content']}</p>", unsafe_allow_html=True)

# # === Entrada do usuário ===
# user_input = st.chat_input(
#     "Digite sua pergunta sobre o site Jovem Programador...",
#     key="input_usuario"
# )

# # === Quando o usuário envia mensagem ===
# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user", avatar=str(assets_path / "avatar-user.png")):
#         st.markdown(f"<p aria-label='Você disse'>{user_input}</p>", unsafe_allow_html=True)

#     # === Comunicação com backend ===
#     try:
#         response = requests.post(
#             "http://127.0.0.1:5000/perguntar",
#             json={"pergunta": user_input},
#             timeout=20
#         )

#         if response.status_code == 200 and "resposta" in response.json():
#             bot_reply = response.json()["resposta"]
#         else:
#             bot_reply = "Ocorreu um problema ao processar sua pergunta. Tente novamente."
#     except requests.exceptions.RequestException:
#         bot_reply = "Não foi possível conectar ao servidor no momento. Verifique se ele está em execução."

#     # === Exibir resposta do chatbot ===
#     st.session_state.messages.append({"role": "assistant", "content": bot_reply})
#     with st.chat_message("assistant", avatar=str(assets_path / "avatar-original.png")):
#         st.markdown(f"<p aria-label='Chatbot respondeu'>{bot_reply}</p>", unsafe_allow_html=True)

# # === Rodapé acessível ===
# st.markdown("""
#     <footer style="text-align:center; margin-top:2rem; font-size:0.9em; color:#888;">
#         <p>Chatbot desenvolvido para o projeto Jovem Programador | Acessível conforme WCAG 2.1</p>
#     </footer>
# """, unsafe_allow_html=True)

# # === VLibras (correto e funcional no Streamlit) ===
# components.html(
#     """
#     <div vw class="enabled">
#         <div vw-access-button class="active"></div>
#         <div vw-plugin-wrapper>
#             <div class="vw-plugin-top-wrapper"></div>
#         </div>
#     </div>

#     <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
#     <script>
#         new window.VLibras.Widget('https://vlibras.gov.br/app');
#     </script>
#     """,
#     height=300,
# )
