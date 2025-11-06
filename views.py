# views.py
from models.servico import Servico, ServicoDAO, ServicoPorHora
from models.cliente import Cliente, ClienteDAO
from models.horarios import Horario, HorarioDAO
from models.profissional import Profissional, ProfissionalDAO
from datetime import datetime, timedelta

class View:

    # CLIENTE
    def cliente_inserir(nome, email, fone, senha):
        cliente = Cliente(0, nome, email, fone, senha)
        ClienteDAO.inserir(cliente)

    def cliente_listar():
        return ClienteDAO.listar()

    def cliente_listar_id(id):
        return ClienteDAO.listar_id(id)

    def cliente_atualizar(id, nome, email, fone, senha):
        cliente = Cliente(id, nome, email, fone, senha)
        ClienteDAO.atualizar(cliente)

    def cliente_excluir(id):
        cliente = Cliente(id, "", "", "", "")
        ClienteDAO.excluir(cliente)

    def cliente_criar_admin():
        for c in View.cliente_listar():
            if c.get_email() == "admin":
                return
        View.cliente_inserir("admin", "admin", "fone", "1234")

    def cliente_autenticar(email, senha):
        for c in View.cliente_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id": c.get_id(), "nome": c.get_nome()}
        return None

    # PROFISSIONAL
    def profissional_inserir(nome, especialidade, conselho, email, senha):
        prof = Profissional(0, nome, especialidade, conselho, email, senha)
        ProfissionalDAO.inserir(prof)

    def profissional_listar():
        return ProfissionalDAO.listar()

    def profissional_listar_id(id):
        return ProfissionalDAO.listar_id(id)

    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        prof = Profissional(id, nome, especialidade, conselho, email, senha)
        ProfissionalDAO.atualizar(prof)

    def profissional_excluir(id):
        prof = Profissional(id, "", "", "", "", "")
        ProfissionalDAO.excluir(prof)

    def profissional_autenticar(email, senha):
        for p in View.profissional_listar():
            if p.get_email() == email and p.get_senha() == senha:
                return {"id": p.get_id(), "nome": p.get_nome()}
        return None

    # SERVIÇO
    def servico_inserir(descricao, valor):
        serv = Servico(0, descricao, valor)
        ServicoDAO.inserir(serv)

    def servico_inserir_por_hora(descricao, valor_hora):
        serv = ServicoPorHora(0, descricao, valor_hora)
        ServicoDAO.inserir(serv)

    def servico_listar():
        return ServicoDAO.listar()

    def servico_listar_id(id):
        return ServicoDAO.listar_id(id)

    def servico_atualizar(id, descricao, valor):
        # Detecta tipo atual para manter ou converter
        atual = View.servico_listar_id(id)
        if atual and isinstance(atual, ServicoPorHora):
            serv = ServicoPorHora(id, descricao, valor)
        else:
            serv = Servico(id, descricao, valor)
        ServicoDAO.atualizar(serv)

    def servico_excluir(id):
        serv = Servico(id, "", 0.0)
        ServicoDAO.excluir(serv)

    # HORÁRIO
    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional, duracao_horas=1):
        c = Horario(0, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente if id_cliente is not None else 0)
        c.set_id_servico(id_servico if id_servico is not None else 0)
        c.set_id_profissional(id_profissional if id_profissional is not None else 0)
        c.set_duracao_horas(duracao_horas)
        HorarioDAO.inserir(c)

    def horario_listar():
        return HorarioDAO.listar()

    def horario_listar_id(id):
        return HorarioDAO.listar_id(id)

    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional, duracao_horas=1):
        c = Horario(id, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente if id_cliente is not None else 0)
        c.set_id_servico(id_servico if id_servico is not None else 0)
        c.set_id_profissional(id_profissional if id_profissional is not None else 0)
        c.set_duracao_horas(duracao_horas)
        HorarioDAO.atualizar(c)

    def horario_excluir(id):
        c = Horario(id, None)
        HorarioDAO.excluir(c)

    # Retorna horários disponíveis para agendar de um profissional (>= agora, sem confirmar e sem cliente)
    def horario_agendar_horario(id_profissional):
        r = []
        agora = datetime.now()
        for h in View.horario_listar():
            if h.get_data() is None:
                continue
            if h.get_data() >= agora and not h.get_confirmado() and h.get_id_cliente() in [0, None] and h.get_id_profissional() == id_profissional:
                r.append(h)
        r.sort(key=lambda h: h.get_data())
        return r

    # Helper: verifica se existe sequência de horários livres (hora cheia) a partir de start, para duracao horas
    def verificar_blocos_consecutivos(profissional_id, start_dt, duracao_horas):
        # procura blocos com mesma data/hora e id_profissional e sem cliente
        encontrados = []
        all_h = View.horario_listar()
        for i in range(duracao_horas):
            target = start_dt + timedelta(hours=i)
            achado = None
            for h in all_h:
                if h.get_data() == target and h.get_id_profissional() == profissional_id and (h.get_id_cliente() in [0, None]) and (not h.get_confirmado()):
                    achado = h
                    break
            if achado is None:
                return None
            encontrados.append(achado)
        return encontrados
