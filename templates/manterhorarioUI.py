# templates/manterhorarioUI.py
import streamlit as st
import pandas as pd
from views import View
import time
from datetime import datetime

class ManterHorarioUI:

    def main():
        st.header("Cadastro de Horários")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterHorarioUI.listar()
        with tab2: ManterHorarioUI.inserir()
        with tab3: ManterHorarioUI.atualizar()
        with tab4: ManterHorarioUI.excluir()

    def listar():
        horarios = View.horario_listar()
        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
            return

        dic = []
        for obj in horarios:
            cliente = View.cliente_listar_id(obj.get_id_cliente())
            servico = View.servico_listar_id(obj.get_id_servico())
            profissional = View.profissional_listar_id(obj.get_id_profissional())
            tipo = servico.to_json().get("tipo") if servico else "fixo"

            linha = {
                "id": obj.get_id(),
                "data": obj.get_data(),
                "confirmado": obj.get_confirmado(),
                "cliente": cliente.get_nome() if cliente else None,
                "serviço": servico.get_descricao() if servico else None,
                "profissional": profissional.get_nome() if profissional else None,
            }

            if tipo == "hora":
                linha["duração (h)"] = obj.get_duracao_horas()

            dic.append(linha)

        df = pd.DataFrame(dic)
        st.dataframe(df, hide_index=True)

    def inserir():
        clientes = View.cliente_listar()
        servicos = View.servico_listar()
        profissionais = View.profissional_listar()

        data = st.text_input("Informe a data e horário do serviço", datetime.now().strftime("%d/%m/%Y %H:%M"))
        confirmado = st.checkbox("Confirmado")

        cliente = st.selectbox("Informe o cliente", clientes, index=None)
        profissional = st.selectbox("Informe o profissional", profissionais, index=None)
        servico = st.selectbox("Informe o serviço", servicos, index=None)

        duracao = 1  # valor padrão

        # Só mostra o campo de duração se o serviço selecionado for "por hora"
        if servico is not None and servico.to_json().get("tipo") == "hora":
            duracao = st.number_input("Duração em horas", min_value=1, value=1, step=1)

        if st.button("Inserir"):
            id_cliente = cliente.get_id() if cliente else None
            id_profissional = profissional.get_id() if profissional else None
            id_servico = servico.get_id() if servico else None

            View.horario_inserir(
                datetime.strptime(data, "%d/%m/%Y %H:%M"),
                confirmado,
                id_cliente,
                id_servico,
                id_profissional,
                duracao_horas=duracao
            )
            st.success("Horário inserido com sucesso")
            time.sleep(1)
            st.rerun()

    def atualizar():
        horarios = View.horario_listar()
        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
            return

        op = st.selectbox("Selecione o horário para atualizar", horarios)
        data = st.text_input("Informe a nova data e horário", op.get_data().strftime("%d/%m/%Y %H:%M"))
        confirmado = st.checkbox("Confirmado", value=op.get_confirmado())

        clientes = View.cliente_listar()
        profissionais = View.profissional_listar()
        servicos = View.servico_listar()

        cliente = st.selectbox(
            "Informe o novo cliente", clientes,
            index=next((i for i, c in enumerate(clientes) if c.get_id() == op.get_id_cliente()), 0)
        )
        profissional = st.selectbox(
            "Informe o novo profissional", profissionais,
            index=next((i for i, p in enumerate(profissionais) if p.get_id() == op.get_id_profissional()), 0)
        )
        servico = st.selectbox(
            "Informe o novo serviço", servicos,
            index=next((i for i, s in enumerate(servicos) if s.get_id() == op.get_id_servico()), 0)
        )

        duracao = op.get_duracao_horas()

        # Só exibe o campo se o serviço for por hora
        if servico is not None and servico.to_json().get("tipo") == "hora":
            duracao = st.number_input("Duração em horas", min_value=1, value=duracao, step=1)

        if st.button("Atualizar"):
            id_cliente = cliente.get_id() if cliente else None
            id_profissional = profissional.get_id() if profissional else None
            id_servico = servico.get_id() if servico else None

            View.horario_atualizar(
                op.get_id(),
                datetime.strptime(data, "%d/%m/%Y %H:%M"),
                confirmado,
                id_cliente,
                id_servico,
                id_profissional,
                duracao_horas=duracao
            )
            st.success("Horário atualizado com sucesso")
            time.sleep(1)
            st.rerun()

    def excluir():
        horarios = View.horario_listar()
        if len(horarios) == 0:
            st.write("Nenhum horário cadastrado")
            return

        op = st.selectbox("Selecione o horário para excluir", horarios)
        if st.button("Excluir"):
            View.horario_excluir(op.get_id())
            st.success("Horário excluído com sucesso")
            time.sleep(1)
            st.rerun()
