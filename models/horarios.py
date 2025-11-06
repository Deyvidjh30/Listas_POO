# models/horarios.py
from datetime import datetime
import json

class Horario:
    def __init__(self, id, data):
        self.set_id(id)
        self.set_data(data)
        self.set_confirmado(False)
        self.set_id_cliente(0)
        self.set_id_servico(0)
        self.set_id_profissional(0)
        self.set_duracao_horas(1)  # novo campo: duração em horas (inteiro >=1)

    # Representação
    def __str__(self):
        data_str = self.data.strftime("%d/%m/%Y %H:%M") if self.data else "N/A"
        return f"{self.id} - {data_str} - {self.confirmado} - {self.duracao_horas}h"

    # gets
    def get_id(self): return self.id
    def get_data(self): return self.data
    def get_confirmado(self): return self.confirmado
    def get_id_cliente(self): return self.id_cliente
    def get_id_servico(self): return self.id_servico
    def get_id_profissional(self): return self.id_profissional
    def get_duracao_horas(self): return self.duracao_horas

    # sets
    def set_id(self, id): self.id = id
    def set_data(self, data): self.data = data
    def set_confirmado(self, confirmado): self.confirmado = confirmado
    def set_id_cliente(self, id_cliente): self.id_cliente = id_cliente
    def set_id_servico(self, id_servico): self.id_servico = id_servico
    def set_id_profissional(self, id_profissional): self.id_profissional = id_profissional
    def set_duracao_horas(self, dur): self.duracao_horas = max(1, int(dur))

    # JSON
    def to_json(self):
        return {
            "id": self.id,
            "data": self.data.strftime("%d/%m/%Y %H:%M") if self.data else None,
            "confirmado": self.confirmado,
            "id_cliente": self.id_cliente,
            "id_servico": self.id_servico,
            "id_profissional": self.id_profissional,
            "duracao_horas": self.duracao_horas
        }

    @staticmethod
    def from_json(dic):
        data = None
        if dic.get("data"):
            data = datetime.strptime(dic["data"], "%d/%m/%Y %H:%M")
        h = Horario(dic["id"], data)
        h.set_confirmado(dic.get("confirmado", False))
        h.set_id_cliente(dic.get("id_cliente", 0))
        h.set_id_servico(dic.get("id_servico", 0))
        h.set_id_profissional(dic.get("id_profissional", 0))
        h.set_duracao_horas(dic.get("duracao_horas", 1))
        return h


class HorarioDAO:
    objetos = []
    arquivo = "horarios.json"

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        id_max = 0
        for aux in cls.objetos:
            if aux.get_id() > id_max:
                id_max = aux.get_id()
        obj.set_id(id_max + 1)
        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.objetos

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open(cls.arquivo, mode="r", encoding="utf-8") as f:
                list_dic = json.load(f)
                for dic in list_dic:
                    cls.objetos.append(Horario.from_json(dic))
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open(cls.arquivo, mode="w", encoding="utf-8") as f:
            json.dump([o.to_json() for o in cls.objetos], f, ensure_ascii=False, indent=2)
