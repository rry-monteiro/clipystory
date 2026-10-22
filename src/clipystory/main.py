import argparse as arg

from . import clipboard, daemon


def main():
    parser = arg.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--daemon", action="store_true", help="vigia o clipboard")
    grupo.add_argument("--show", action="store_true", help="abre a janela do histórico")
    args = parser.parse_args()

    if args.daemon:
        print("vigiando clipboard...")
        clipboard.verify()  # verificação do tool
        daemon.run() # começa a rodar o histórico

    elif args.show:
        print("pedindo pro daemon abrir a janela...")



if __name__ == "__main__":
    main()
