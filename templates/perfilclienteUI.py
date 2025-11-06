import streamlit as st
from views import View
import time

class PerfilClienteUI:

    def main():
        st.header("Meus Dados")

        op = View.cliente_listar_id(st.session_state["usuario_id"])

        nome = st.text_input("Novo nome", op.get_nome())
        email = st.text_input("Novo e-mail", op.get_email())
        fone = st.text_input("Novo fone", op.get_fone())
        senha = st.text_input("Nova senha", op.get_senha(), type="password")

        if st.button("Atualizar"):
            id = op.get_id()
            View.cliente_atualizar(id, nome, email, fone, senha)
            st.success("Dados atualizados com sucesso")
            time.sleep(2)
            st.rerun()
