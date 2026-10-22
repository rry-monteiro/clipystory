import shutil
import subprocess

_comandos: dict = {}  # dicionario de comandos | depende do tool que o usuário usa


def verify() -> None:
    """garante que exista uma ferramenta de copia e cola, devolvendo raise RuntimeError caso não exista"""
    global _comandos

    """
    aqui o pontyo de vista é do  TOOL, não nosso, logo:
        escrever -> escrever no sistema
        ler -> colar no sistema
    """

    if shutil.which("wl-paste"):
        _comandos = {
            "ler": ["wl-paste", "--no-newline"],
            "escrever": ["wl-copy"],
        }
    elif shutil.which("xclip"):
        _comandos = {
            "ler": ["xclip", "-selection", "clipboard", "-o"],
            "escrever": ["xclip", "-selection", "clipboard"],
        }
    else:
        raise RuntimeError("instale wl-clipboard ou xclip")

    print(_comandos)


def write(text: str):
    """
    copia o conteúdo pro histórico: window.py vai chamar essa função sempre que o usuário escrolher
    o texto do histórico, assim, o texto escolhido pelo vai pro clipboar do usuário
    """
    subprocess.run(_comandos["escrever"], input=text, text=True, timeout=2, check=False)
