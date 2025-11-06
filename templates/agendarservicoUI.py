# templates/agendarServicoUI.py
import streamlit as st
from views import View
import time
from datetime import datetime

class AgendarServicoUI:

    def main():
        st.header("Agendar Serviço")

        profs = View.profissional_listar()
        if len(profs) == 0:
            st.write("Nenhum profissional cadastrado")
            return

        profissional = st.selectbox("Selecione o profissional", profs)
        horarios = View.horario_agendar_horario(profissional.get_id())

        if len(horarios) == 0:
            st.write("Nenhum horário disponível")
            return

        servicos = View.servico_listar()
        servico = st.selectbox("Selecione o serviço", servicos)
        tipo_servico = servico.to_json().get("tipo", "fixo")

        # Exibe aviso e campo de horas apenas para serviços por hora
        if tipo_servico == "hora":
            st.info("⏰ Este serviço é cobrado por hora. Só é possível agendar em horários inteiros.")
            qtd_horas = st.number_input("Quantas horas deseja contratar?", min_value=1, max_value=8, step=1)
        else:
            qtd_horas = 1  # padrão para serviços fixos

        # Exibe apenas horários válidos
        if tipo_servico == "hora":
            horarios = [h for h in horarios if h.get_data().minute == 0]
            if len(horarios) == 0:
                st.warning("Nenhum horário em hora cheia disponível para este serviço.")
                return

        horario = st.selectbox("Selecione o horário", horarios)

        if st.button("Agendar"):
            preco_final = servico.calcular_preco(qtd_horas)

            View.horario_atualizar(
                horario.get_id(),
                horario.get_data(),
                False,
                st.session_state["usuario_id"],
                servico.get_id(),
                profissional.get_id(),
                duracao_horas=qtd_horas
            )

            st.success(f"Horário agendado com sucesso! Valor total: R$ {preco_final:.2f}")
            time.sleep(2)
            st.rerun()
