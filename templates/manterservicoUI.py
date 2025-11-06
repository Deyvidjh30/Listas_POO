# templates/manterservicoUI.py
import streamlit as st
import pandas as pd
import time
from views import View

class ManterServicoUI:

    def main():
        st.header("Cadastro de Serviços")

        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterServicoUI.listar()
        with tab2: ManterServicoUI.inserir()
        with tab3: ManterServicoUI.atualizar()
        with tab4: ManterServicoUI.excluir()

    def listar():
        servicos = View.servico_listar()
        if len(servicos) == 0:
            st.write("Nenhum serviço cadastrado")
        else:
            dic = []
            for s in servicos:
                j = s.to_json()
                tipo = j.get("tipo", "fixo")
                if tipo == "hora":
                    valor = j.get("valor_hora", s.get_valor())
                    tipo_label = "Por Hora"
                else:
                    valor = j.get("valor", s.get_valor())
                    tipo_label = "Fixo"
                dic.append({
                    "id": s.get_id(),
                    "descricao": s.get_descricao(),
                    "valor": valor,
                    "tipo": tipo_label
                })
            df = pd.DataFrame(dic)
            st.dataframe(df, hide_index=True)

    def inserir():
        tipo = st.radio("Tipo de Serviço", ["Fixo", "Por Hora"])
        descricao = st.text_input("Descrição do serviço")
        if tipo == "Fixo":
            valor = st.number_input("Valor do serviço (R$)", min_value=0.0, step=0.1)
        else:
            valor = st.number_input("Valor por hora (R$)", min_value=0.0, step=0.1)

        if st.button("Inserir"):
            if tipo == "Fixo":
                View.servico_inserir(descricao, valor)
            else:
                View.servico_inserir_por_hora(descricao, valor)
            st.success("Serviço inserido com sucesso")
            time.sleep(1)
            st.rerun()

    def atualizar():
        servicos = View.servico_listar()
        if len(servicos) == 0:
            st.write("Nenhum serviço cadastrado")
            return
        op = st.selectbox("Selecione o serviço para atualizar", servicos)
        j = op.to_json()
        tipo = j.get("tipo", "fixo")
        descricao = st.text_input("Nova descrição", op.get_descricao())
        if tipo == "hora":
            valor = st.number_input("Novo valor por hora (R$)", value=op.get_valor())
        else:
            valor = st.number_input("Novo valor (R$)", value=op.get_valor())
        if st.button("Atualizar"):
            View.servico_atualizar(op.get_id(), descricao, valor)
            st.success("Serviço atualizado com sucesso")
            time.sleep(1)
            st.rerun()

    def excluir():
        servicos = View.servico_listar()
        if len(servicos) == 0:
            st.write("Nenhum serviço cadastrado")
            return
        op = st.selectbox("Selecione o serviço para excluir", servicos)
        if st.button("Excluir"):
            View.servico_excluir(op.get_id())
            st.success("Serviço excluído com sucesso")
            time.sleep(1)
            st.rerun()
