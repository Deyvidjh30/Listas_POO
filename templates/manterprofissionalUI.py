import streamlit as st
import pandas as pd
from views import View
import time

class ManterProfissionalUI:

    def main():
        st.header("Cadastro de Profissionais")

        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterProfissionalUI.listar()
        with tab2: ManterProfissionalUI.inserir()
        with tab3: ManterProfissionalUI.atualizar()
        with tab4: ManterProfissionalUI.excluir()

    def listar():
        profissionais = View.profissional_listar()
        if len(profissionais) == 0:
            st.write("Nenhum profissional cadastrado")
        else:
            list_dic = [obj.to_json() for obj in profissionais]
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index=True)

    def inserir():
        nome = st.text_input("Informe o nome")
        especialidade = st.text_input("Informe a especialidade")
        conselho = st.text_input("Informe o conselho")
        email = st.text_input("Informe o email")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Inserir"):
            View.profissional_inserir(nome, especialidade, conselho, email, senha)
            st.success("Profissional inserido com sucesso")
            time.sleep(2)
            st.rerun()

    def atualizar():
        profissionais = View.profissional_listar()
        if len(profissionais) == 0:
            st.write("Nenhum profissional cadastrado")
        else:
            op = st.selectbox("Atualização de profissionais", profissionais)
            nome = st.text_input("Novo nome", op.get_nome())
            especialidade = st.text_input("Nova especialidade", op.get_especialidade())
            conselho = st.text_input("Novo conselho", op.get_conselho())
            email = st.text_input("Novo email", op.get_email())
            senha = st.text_input("Nova senha", op.get_senha(), type="password")

            if st.button("Atualizar"):
                id = op.get_id()
                View.profissional_atualizar(id, nome, especialidade, conselho, email, senha)
                st.success("Profissional atualizado com sucesso")
                time.sleep(2)
                st.rerun()

    def excluir():
        profissionais = View.profissional_listar()
        if len(profissionais) == 0:
            st.write("Nenhum profissional cadastrado")
        else:
            op = st.selectbox("Exclusão de profissionais", profissionais)
            if st.button("Excluir"):
                id = op.get_id()
                View.profissional_excluir(id)
                st.success("Profissional excluído com sucesso")
                time.sleep(2)
                st.rerun()
