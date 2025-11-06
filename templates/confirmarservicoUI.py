import streamlit as st
import time
from views import View

class ConfirmarServicoUI:

    def main():
        st.header("Confirmar Serviço")

        profissional = View.profissional_listar_id(st.session_state["usuario_id"])
        if profissional is None:
            st.warning("Nenhum profissional logado.")
            return

        horarios = View.horario_listar()
        if len(horarios) == 0:
            st.info("Nenhum horário cadastrado.")
            return

        horarios_profissional = [
            h for h in horarios
            if h.get_id_profissional() == profissional.get_id() and h.get_id_cliente() not in [0, None]
        ]

        if len(horarios_profissional) == 0:
            st.info("Você não possui horários agendados com clientes.")
            return

        op = st.selectbox(
            "Selecione o horário",
            horarios_profissional,
            format_func=lambda h: f"{h.get_id()} - {h.get_data().strftime('%d/%m/%Y %H:%M')} - {h.get_confirmado()}"
        )

        cliente = View.cliente_listar_id(op.get_id_cliente())
        if cliente:
            st.write(f"Cliente: {cliente.get_nome()} ({cliente.get_email()} - {cliente.get_fone()})")

        if st.button("Confirmar"):
            View.horario_atualizar(
                op.get_id(),
                op.get_data(),
                True,
                op.get_id_cliente(),
                op.get_id_servico(),
                op.get_id_profissional()
            )
            st.success("Serviço confirmado com sucesso!")
            time.sleep(2)
            st.rerun()
