import argparse as arg
import sys

from . import autostart, clipboard, daemon


def main():
    parser = arg.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--daemon", action="store_true", help="vigia o clipboard")
    grupo.add_argument("--show", action="store_true", help="abre a janela do histórico")
    grupo.add_argument("--install", action="store_true", help="liga o autostart no login")
    grupo.add_argument("--uninstall", action="store_true", help="remove o autostart")
    args = parser.parse_args()

    try:
        if args.daemon:
            clipboard.verify()
            daemon.run()
        elif args.show:
            """ from . import window """

            _itens = clipboard.get_list()
            """ window.open(itens) """
        elif args.install:
            autostart.install()
        elif args.uninstall:
            autostart.uninstall()
    except RuntimeError as e:
        print(f"erro: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
