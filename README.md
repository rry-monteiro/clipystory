# CliPYstory - histórico de área de transferência minimalista para Linux

Histórico da área de transferência para Linux, no estilo do `Win+V` do Windows.

Um daemon guarda tudo que você copia. Quando você aperta um atalho (por padrão `Super+V`), uma janela mostra a lista. Clique num item (ou use as setas e `Enter`) e o texto volta para a área de transferência, pronto para colar com `Ctrl+V`.

## Como funciona

São dois comandos que conversam por um socket unix:

|clipystory --daemon  |  clipystory --show|
|----|--|
|roda desde o login| roda com chamada|
|vigia o clipboard|pede a lista ao deamon|
|guarda até 100 itens na memória|abre a janela|
|responde pedidos pelo socket|escreve o texto escolhido no clipboard|

> O socket fica em `$XDG_RUNTIME_DIR/clipystory.sock`, pasta acessível só ao seu usuário.

## Compatibilidade

O jeito de descobrir que algo foi copiado depende do compositor:

| Ambiente | Como vigia o clipboard | Dependências |
|---|---|---|
| GNOME (Wayland ou Xorg) | evento do `clipnotify`, lendo com `xclip` (via XWayland no Wayland) | `xclip`, `clipnotify` | 
| Sway, Hyprland, KDE (Wayland) | `wl-paste --watch` | `wl-clipboard` |
| Qualquer outro caso | cai no modo `xclip` + `clipnotify` | `xclip`, `clipnotify` |

**Por que o GNOME é diferente:** o `wl-paste --watch` depende de um protocolo (data-control) que o compositor do GNOME não oferece para apps comuns. Por isso, no GNOME, o clipystory usa o X11 do XWayland. O programa escolhe o modo sozinho ao iniciar.

## Requisitos

- Um driver gráfico com OpenGL 3 funcionando (a janela é feita com [DearPyGui](https://github.com/hoffstadt/DearPyGui), que é instalado automaticamente)
- [`uv`](https://docs.astral.sh/uv/)

- [`clipnotify`](https://github.com/cdown/clipnotify)
- [`python 3.14`](https://www.python.org/downloads/) ou superior
- [`wl-clipboard`](https://github.com/bugaevc/wl-clipboard) ou [`xclip`](https://github.com/astrand/xclip) (normalmente um desses já vem no sistema, confira)

## Instalação

1. Instale as dependências

2. clone do repo

```bash
git clone <url-do-repo>
cd clipystory
uv tool install .
```

Se o comando `clipystory` não for encontrado depois, rode `uv tool update-shell` e abra um novo terminal. Confira com `which clipystory`.

3. Ligue o autostart para o deamon subir no login

```bash
clipystory --install
```

Isso cria `~/.config/autostart/clipystory.desktop`. Para subir o daemon agora, sem relogar:

```bash
gio launch ~/.config/autostart/clipystory.desktop
```

> O `--install` só funciona com a versão instalada por `uv tool install`, não com `uv run`. Ele grava o caminho do comando instalado no `.desktop`.

4. Configure o atalho `Super+V` (ou qualquer outro de sua prefeência). Esse passo é manual.

Garanta que o atalho escolhido chame o comando `clipystory --show`, rode `witch clipystory`, pegue o caminho absoluto e faça o atalhochamar exatamente ele com a flag `--show`

## Uso

| Comando | O que faz |
|---|---|
| `clipystory --daemon` | vigia o clipboard e guarda o histórico (roda uma vez, normalmente pelo autostart) |
| `clipystory --show` | abre a janela com o histórico (é o que o atalho chama) |
| `clipystory --install` | cria o autostart |
| `clipystory --uninstall` | remove o autostart |

### Na janela:

| Tecla | Ação |
|---|---|
| `↑` / `↓` | navega entre os itens |
| `Enter` ou clique | copia o item de volta para o clipboard e fecha |
| `Esc` | fecha sem escolher |

Depois de escolher, aperte `Ctrl+V` no app onde quer o texto. Se o texto já estava no histórico e você o copiar de novo, ele sobe para o topo, sem duplicar.

## Limitações

- **Só texto.** Imagens e arquivos copiados são ignorados.
- **O histórico vive na memória do daemon.** Ele é perdido quando o daemon reinicia (relogin, `pkill`, queda). O limite é de 100 itens.
- **Senhas entram no histórico.** Tudo que for copiado é guardado, inclusive o que vem de gerenciadores de senha. Nada é gravado em disco, e o socket só é acessível ao seu usuário, mas não existe filtro para conteúdo sensível.
- **Não cola sozinho.** O clique coloca o texto no clipboard e você cola com `Ctrl+V`.
- **Posição e foco da janela dependem do compositor.** No GNOME a janela roda via XWayland, e o compositor pode ignorar a posição pedida e decidir o foco. Se a janela abrir sem foco, clique nela antes de usar o teclado.
- **O daemon não é reiniciado se cair.** O autostart do GNOME só inicia o processo uma vez por sessão.

## Solução de problemas

**`erro: daemon não está rodando`**
O daemon não está ativo. Confira com `pgrep -af clipystory`. Para subir: `gio launch ~/.config/autostart/clipystory.desktop`.

**A janela abre vazia**
O daemon não capturou nada. Confirme que `xclip` e `clipnotify` (ou `wl-clipboard`) estão instalados e que o daemon foi iniciado depois disso. Lembre que só entra o que foi copiado **depois** de o daemon subir.

**Erro ao subir o daemon**
Rode `clipystory --daemon` num terminal para ver a mensagem. Quando ele sobe pelo autostart, a saída de erro não aparece em lugar nenhum. Para depurar, edite o `Exec` do `.desktop` para `sh -c 'clipystory --daemon >> /tmp/clipystory.log 2>&1'` (com o caminho absoluto do comando).

**Dois daemons ao mesmo tempo**
Não rode `clipystory --daemon` manualmente enquanto o do autostart estiver ativo: o segundo cria um novo socket e o primeiro continua capturando sem que ninguém consiga falar com ele. Para reiniciar limpo: `pkill -f "clipystory --daemon"` e depois suba um só.

**A fonte aparece minúscula**
A fonte embutida não foi empacotada ou não foi encontrada, e a janela caiu na fonte padrão do DearPyGui. Reinstale com `uv tool install --reinstall .`.

## Estrutura
```
src/clipystory/
├── main.py         # argumentos e despacho (--daemon, --show, --install, --uninstall)
├── clipboard.py    # escolhe a ferramenta, lê, escreve e espera mudanças
├── daemon.py       # histórico em memória e servidor do socket
├── window.py       # janela DearPyGui
├── autostart.py    # cria e remove o .desktop
└── fonts/          # fonte embutida na janela
```