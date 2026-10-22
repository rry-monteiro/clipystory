import argparse as arg
import sys

from . import clipboard, daemon


def main():
    parser = arg.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--daemon", action="store_true", help="vigia o clipboard")
    grupo.add_argument("--show", action="store_true", help="abre a janela do histórico")
    args = parser.parse_args()

    try:
        if args.daemon:
            print("vigiando clipboard...")
            clipboard.verify()
            daemon.run()
        elif args.show:
            from . import window
            print("pedindo pro daemon abrir a janela...")
    except RuntimeError as e:
        print(f"erro: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
