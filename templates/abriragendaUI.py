# templates/abrirAgendaUI.py
import streamlit as st
from views import View
from datetime import datetime, timedelta

class AbrirAgendaUI:

    def main():
        st.header("Abrir Minha Agenda")
        st.write("Preencha os campos para inserir horários de atendimento na sua agenda.")

        data = st.date_input("Dia do atendimento", datetime.now())
        # hora inicial e final em hora cheia por padrão
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        hora_inicial = st.time_input("Hora inicial", value=now.time())
        hora_final = st.time_input("Hora final", value=(now + timedelta(hours=1)).time())
        intervalo = st.number_input("Intervalo entre horários (minutos)", min_value=5, max_value=120, value=30, step=5)

        servicos = View.servico_listar()
        servico = st.selectbox("Serviço oferecido", servicos, format_func=lambda s: s.get_descricao() if s else "")

        tipo = servico.to_json().get("tipo")
        if tipo == "hora":
            intervalo = 60
            st.info("Serviço por hora: intervalo ajustado para 60 minutos e horários serão gerados em horas cheias.")

        if st.button("Inserir horários na agenda"):
            profissional_id = st.session_state.get("usuario_id")
            dt_inicial = datetime.combine(data, hora_inicial)
            dt_final = datetime.combine(data, hora_final)
            horarios_criados = 0

            # Se serviço por hora, ajustar dt_inicial para hora cheia
            if tipo == "hora":
                dt_inicial = dt_inicial.replace(minute=0, second=0, microsecond=0)

            while dt_inicial < dt_final:
                View.horario_inserir(dt_inicial, False, None, servico.get_id(), profissional_id, duracao_horas=1)
                horarios_criados += 1
                dt_inicial += timedelta(minutes=intervalo)

            st.success(f"{horarios_criados} horários inseridos na agenda!")
