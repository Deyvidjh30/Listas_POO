import streamlit as st

from templates.manterclienteUI import ManterClienteUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.manterprofissionalUI import ManterProfissionalUI
from templates.alterarsenhaUI import AlterarSenhaUI
from templates.abrircontaUI import AbrirContaUI
from templates.loginUI import LoginUI
from templates.perfilclienteUI import PerfilClienteUI
from templates.perfilprofissionalUI import PerfilProfissionalUI
from templates.agendarservicoUI import AgendarServicoUI
from templates.visualizarAgendaUI import VisualizarAgendaUI
from templates.visualizarservicoUI import VisualizarServicoUI
from templates.confirmarservicoUI import ConfirmarServicoUI
from templates.loginprofissionalUI import LoginProfissionalUI
from templates.abriragendaUI import AbrirAgendaUI

from views import View


class IndexUI:

    def main():
        View.cliente_criar_admin()
        IndexUI.sidebar()

    # -------------------- MENUS --------------------
    def menu_visitante():
        op = st.sidebar.selectbox(
            "Menu",
            ["Entrar no Sistema", "Entrar no Sistema de Profissionais", "Abrir Conta"]
        )
        if op == "Entrar no Sistema": LoginUI.main()
        if op == "Entrar no Sistema de Profissionais": LoginProfissionalUI.main()
        if op == "Abrir Conta": AbrirContaUI.main()

    def menu_cliente():
        op = st.sidebar.selectbox("Menu", ["Meus Dados", "Agendar Serviço", "Meus Serviços"])
        if op == "Meus Dados": PerfilClienteUI.main()
        if op == "Agendar Serviço": AgendarServicoUI.main()
        if op == "Meus Serviços": VisualizarServicoUI.main()

    def menu_profissional():
        op = st.sidebar.selectbox("Menu", ["Meus Dados", "Gerenciar Agenda", "Confirmar Serviço"])
        if op == "Meus Dados": PerfilProfissionalUI.main()
        if op == "Gerenciar Agenda": VisualizarAgendaUI.main()
        if op == "Confirmar Serviço": ConfirmarServicoUI.main()

    def menu_admin():
        op = st.sidebar.selectbox(
            "Menu",
            ["Cadastro de Clientes", "Cadastro de Serviços",
             "Cadastro de Horários", "Cadastro de Profissionais", "Alterar Senha"]
        )
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Serviços": ManterServicoUI.main()
        if op == "Cadastro de Horários": ManterHorarioUI.main()
        if op == "Cadastro de Profissionais": ManterProfissionalUI.main()
        if op == "Alterar Senha": AlterarSenhaUI.main()

    def sair_do_sistema():
        if st.sidebar.button("Sair"):
            del st.session_state["usuario_id"]
            del st.session_state["usuario_nome"]
            st.rerun()

    # -------------------- SIDEBAR --------------------
    def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            admin = st.session_state["usuario_nome"] == "admin"
            profissional = (
                not admin and View.profissional_listar_id(st.session_state["usuario_id"]) is not None
            )

            st.sidebar.write(f"👋 Bem-vindo(a), {st.session_state['usuario_nome']}")

            if admin:
                IndexUI.menu_admin()
            elif profissional:
                IndexUI.menu_profissional()
            else:
                IndexUI.menu_cliente()

            IndexUI.sair_do_sistema()


if __name__ == "__main__":
    IndexUI.main()
