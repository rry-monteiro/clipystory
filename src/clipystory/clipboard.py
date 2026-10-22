import shutil

_comandos: dict = {} #dicionario de comandos | depende do tool que o usuário usa


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
