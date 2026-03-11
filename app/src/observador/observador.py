from typing import Protocol, TypeVar

T = TypeVar("T", contravariant=True)


class Observador(Protocol[T]):

    def atualizar_registro(self, dados: T, ) -> None:
        ...
