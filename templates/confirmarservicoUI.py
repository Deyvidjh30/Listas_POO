
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

        pendentes = [
            h for h in horarios
            if h.get_id_profissional() == profissional.get_id()
            and h.get_id_cliente() not in [0, None]
            and not h.get_confirmado()
        ]
        if len(pendentes) == 0:
            st.info("Nenhum serviço pendente de confirmação.")
            return

        op = st.selectbox(
            "Selecione o horário",
            pendentes,
            format_func=lambda h: f"{h.get_data().strftime('%d/%m/%Y %H:%M')} - Cliente: {View.cliente_listar_id(h.get_id_cliente()).get_nome()}"
        )

        cliente = View.cliente_listar_id(op.get_id_cliente())
        servico = View.servico_listar_id(op.get_id_servico())
        duracao = op.get_duracao_horas()

        st.subheader("🧾 Detalhes do Agendamento")
        st.write(f"**Cliente:** {cliente.get_nome()} ({cliente.get_email()} - {cliente.get_fone()})")
        st.write(f"**Serviço:** {servico.get_descricao()}")
        st.write(f"**Data:** {op.get_data().strftime('%d/%m/%Y %H:%M')}")
        st.write(f"**Duração:** {duracao} hora(s)")

        tipo = servico.to_json().get("tipo", "fixo")
        valor_total = servico.calcular_preco(duracao)
        st.write(f"**Valor Total:** R$ {valor_total:.2f}")

        if st.button("Confirmar Serviço"):
            View.horario_atualizar(
                op.get_id(),
                op.get_data(),
                True,
                op.get_id_cliente(),
                op.get_id_servico(),
                op.get_id_profissional(),
                duracao_horas=op.get_duracao_horas()
            )
            st.success("Serviço confirmado com sucesso!")
            time.sleep(2)
            st.rerun()
