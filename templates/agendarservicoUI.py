import streamlit as st
from views import View
import time

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

        horario = st.selectbox("Selecione o horário", horarios)
        servicos = View.servico_listar()
        servico = st.selectbox("Selecione o serviço", servicos)

        if st.button("Agendar"):
            View.horario_atualizar(
                horario.get_id(),
                horario.get_data(),
                False,
                st.session_state["usuario_id"],
                servico.get_id(),
                profissional.get_id()
            )
            st.success("Horário agendado com sucesso!")
            time.sleep(2)
            st.rerun()
