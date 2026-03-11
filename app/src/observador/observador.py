from typing import Protocol, TypeVar

T = TypeVar("T")


class Observador(Protocol[T]):

    def atualizar_registro(self, dados: T) -> None:
        ...
