import os
import socket
import threading
import time
from pathlib import Path

from . import clipboard

SOCKET_PATH: Path = Path(os.environ["XDG_RUNTIME_DIR"]) / "clipystory.sock"
LIMITE: int = 100
INTERVALO: float = 0.5

historico: dict[str, None] = {}


def config_socket() -> socket.socket:
    """cria e configura o socket"""

    SOCKET_PATH.unlink(missing_ok=True)  # remove o socket antigo

    server = socket.socket(
        socket.AF_UNIX, socket.SOCK_STREAM
    )  # AF_UNIX->conversa local | SOCK_STREAM->estilo tcp
    server.bind(str(SOCKET_PATH))  # diz onde o serviço mora
    server.listen(1)  # funcionando e aceitando 1 cliente por vez

    return server


def handle_request(srv: socket.socket) -> None: ...


def add(texto: str) -> None:
    """adiciona o conteúdo do clipboar no histórico, caso o item ja exista, coloca ele por último"""

    historico.pop(texto, None)  # se já existe, tira
    historico[texto] = None  # reinsere no fim

    # verifica se passou do limite
    if len(historico) > LIMITE:
        # next(iter(historico)) captura o primeiro da lista
        del historico[next(iter(historico))]  # descarta o mais antigo


def run() -> None:
    """loop de adição ao historico de clipboard, verifica se o texto copiado é válido e chama add()"""

    server = config_socket()
    threading.Thread(target=handle_request, args=(server,), daemon=True).start()

    ultimo = ""  # erro ou imagem

    while True:
        atual = clipboard.read()
        if atual and atual != ultimo:  # se não é erro, nem imagem
            add(atual)
            ultimo = atual
        time.sleep(INTERVALO)
