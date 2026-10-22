import argparse as arg


def main():
    parser = arg.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--daemon", action="store_true", help="vigia o clipboard")
    grupo.add_argument("--show", action="store_true", help="abre a janela do histórico")
    args = parser.parse_args()

    if args.daemon:
        print("vigiando clipboard...")
    elif args.show:
        print("pedindo pro daemon abrir a janela...")



if __name__ == "__main__":
    main()
