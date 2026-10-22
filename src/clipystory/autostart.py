import os
import sys
from pathlib import Path

_config = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
DESTINO: Path = _config / "autostart" / "clipystory.desktop"


def install() -> None:
    """cria o .desktop de autostart apontando pro comando que está rodando agora"""
    exe = Path(sys.argv[0]).absolute()

    if ".venv" in exe.parts:
        raise RuntimeError(
            "rode o --install pelo comando instalado (uv tool install), não pelo uv run"
        )

    conteudo = f"""[Desktop Entry]
Type=Application
Name=Clipystory
Comment=Histórico de clipboard
Exec="{exe}" --daemon
Terminal=false
X-GNOME-Autostart-enabled=true
"""
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(conteudo, encoding="utf-8")
    print(f"instalado em {DESTINO}")


def uninstall() -> None:
    DESTINO.unlink(missing_ok=True)
    print("autostart removido")
