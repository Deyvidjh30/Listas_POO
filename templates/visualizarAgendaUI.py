# templates/visualizarAgendaUI.py
import streamlit as st
from views import View
import pandas as pd

class VisualizarAgendaUI:

    def main():
        st.header("Minha Agenda")

        profissional_id = st.session_state.get("usuario_id")
        horarios = View.horario_listar()

        if len(horarios) == 0:
            st.info("Nenhum horário cadastrado.")
            return

        dic = []
        for h in horarios:
            if h.get_id_profissional() == profissional_id:
                servico = View.servico_listar_id(h.get_id_servico())
                cliente = View.cliente_listar_id(h.get_id_cliente())

                linha = {
                    "Data": h.get_data().strftime("%d/%m/%Y %H:%M"),
                    "Serviço": servico.get_descricao() if servico else "",
                    "Cliente": cliente.get_nome() if cliente else "",
                    "Confirmado": "✅ Sim" if h.get_confirmado() else "❌ Não"
                }

                # Só adiciona duração e preço total se for por hora
                if servico and servico.to_json().get("tipo") == "hora":
                    duracao = h.get_duracao_horas()
                    valor_total = servico.calcular_preco(duracao)
                    linha["Duração (h)"] = duracao
                    linha["Valor Total (R$)"] = f"{valor_total:.2f}"

                dic.append(linha)

        if len(dic) == 0:
            st.warning("Nenhum horário encontrado para este profissional.")
        else:
            df = pd.DataFrame(dic)
            st.dataframe(df, hide_index=True)
