from pathlib import Path

import dearpygui.dearpygui as dpg

SIZE_FONT = 15
FONT = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"


def cut_text(texto: str, limite: int = 50) -> str:
    linha = " ".join(texto.split())  # junta quebras de linha e espaços em um só
    return linha[:limite] + "..." if len(linha) > limite else linha


def show(get_list, write):

    def ao_clicar(_sender, _app_data, texto):
        write(texto)
        dpg.stop_dearpygui()

    historico = get_list()

    dpg.create_context()  # liga o pygui
    dpg.create_viewport(title="Histórico", width=400, height=300)  # cria a janela

    if FONT.exists():
        with dpg.font_registry():
            fonte = dpg.add_font(str(FONT), SIZE_FONT)
        dpg.bind_font(fonte)

    # cria painel dentro do viewport
    with dpg.window(label="janela", tag="histwin"):
        for texto in historico:
            dpg.add_selectable(
                label=cut_text(texto), callback=ao_clicar, user_data=texto
            )
            dpg.add_separator()

    # esc = fecha o app
    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_Escape, callback=dpg.stop_dearpygui)

    dpg.setup_dearpygui()  # prepara o renderizador
    dpg.show_viewport()  # mostra a janela
    dpg.set_primary_window("histwin", True)  # transforma em janela principal

    dpg.start_dearpygui()  # roda loop
    dpg.destroy_context()  # desativa
