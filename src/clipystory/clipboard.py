import json
import os
import shutil
import socket
import subprocess
from pathlib import Path

SOCKET_PATH: Path = Path(os.environ["XDG_RUNTIME_DIR"]) / "clipystory.sock"

_comandos: dict = {}  # dicionario de comandos | depende do tool que o usuário usa
_modo: str = ""  # "wl-watch" ou "clipnotify"


def get_session() -> str | None:
    """detecta qual sessão o usuário está pra usar x11 ou wayland"""
    tipo = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if tipo in ("wayland", "x11"):
        return tipo
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    if os.environ.get("DISPLAY"):
        return "x11"
    return None


def verify() -> None:
    """garante que exista uma ferramenta de copia e cola, devolvendo raise RuntimeError caso não exista"""
    global _comandos, _modo

    """
    aqui o pontyo de vista é do  TOOL, não nosso, logo:
        escrever -> escrever no sistema
        ler -> colar no sistema
    """

    if get_session() == "wayland" and not is_gnome() and shutil.which("wl-paste"):
        _modo = "wl-watch"
        _comandos = {
            "ler": ["wl-paste", "--no-newline"],
            "escrever": ["wl-copy"],
        }
    elif shutil.which("xclip") and shutil.which("clipnotify"):
        _modo = "clipnotify"
        _comandos = {
            "ler": ["xclip", "-selection", "clipboard", "-o"],
            "escrever": ["xclip", "-selection", "clipboard"],
        }
    else:
        raise RuntimeError(
            "instala wl-clipboard (Sway/KDE/Hyprland) ou xclip + clipnotify (GNOME/X11)"
        )


def is_gnome() -> bool:
    return "GNOME" in os.environ.get("XDG_CURRENT_DESKTOP", "").upper()


def write(text: str) -> None:
    """
    copia o conteúdo pro histórico: window.py vai chamar essa função sempre que o usuário escrolher
    o texto do histórico, assim, o texto escolhido pelo vai pro clipboar do usuário
    """
    subprocess.run(_comandos["escrever"], input=text, text=True, timeout=2, check=False)


def read() -> str:
    """
    lê o que tem dentro do clipboard do usuário e retorna o valor, em caso de imagem ou falha
    do subprocess, retorna ""
    """
    try:
        r = subprocess.run(
            _comandos["ler"], capture_output=True, text=True, timeout=2, check=False
        )
    except subprocess.TimeoutExpired:
        return ""
    if r.returncode != 0:
        return ""
    return r.stdout


def watch():
    if _modo == "wl-watch":
        p = subprocess.Popen(
            ["wl-paste", "--watch", "echo"],
            stdout=subprocess.PIPE,
            text=True,
        )
        for _ in p.stdout:  # uma linha por cópia
            yield
        raise RuntimeError("wl-paste --watch encerrou (compositor sem suporte?)")
    else:
        while True:
            r = subprocess.run(["clipnotify"], check=False)
            if r.returncode != 0:
                raise RuntimeError("clipnotify falhou (sem DISPLAY? XWayland rodando?)")
            yield


def get_list() -> list[str]:
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(2)

    try:
        client.connect(str(SOCKET_PATH))
        client.sendall(b"lista")
        client.shutdown(socket.SHUT_WR)
        partes = []
        while chunk := client.recv(4096):  # lê até o daemon desligar
            partes.append(chunk)
    except (FileNotFoundError, ConnectionRefusedError):
        raise RuntimeError("daemon não está rodando (inicia com: clipystory --daemon)")
    finally:
        client.close()
    return json.loads(b"".join(partes))
