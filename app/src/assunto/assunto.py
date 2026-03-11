from typing import Generic, TypeVar, List

from app.src.observador.observador import Observador

T = TypeVar('T')


class Assunto(Generic[T]):

    def __init__(self):
        self.observador: List[Observador[T]] = []

    def anexar_observador(self, observador: Observador[T]):
        self.observador.append(observador)

    def notificar_observador(self, dados: T) -> None:
        for obs in self.observador:
            obs.atualizar_registro(dados)
