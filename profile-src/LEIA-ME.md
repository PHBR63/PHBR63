# Perfil PHBR63 — Aincrad v2

> **Material legado.** A versão atual é mantida em [`neon-protocol`](./neon-protocol/README.md). Os assets ficam em `assets/neon-protocol` e `assets/yellow-protocol`; `neon-protocol/build_readme.py` monta o README da raiz.
>
> Os geradores antigos servem somente às versões legadas: gravam `README.legacy.md` na própria pasta de fontes, sem sobrescrever o README da raiz. A documentação abaixo registra a versão anterior.

## Direção visual

A referência enviada pelo usuário é `README (8).md`, um perfil com imagens de seções, painéis de projetos, stack, atividade e blocos expansíveis. Esta versão recria essa composição com identidade própria de Aincrad: azul noturno, ciano, prata e pequenos acentos em âmbar.

Arte ilustrada do castelo e menu Link Start gerada com a ferramenta integrada imagegen. Os demais painéis são SVGs autorais gerados localmente. Nenhuma imagem do GitSkins é utilizada no perfil final.

### Refinamento pela referência Aincrad Memory Archive

O usuário indicou https://aincrad-archive.hecate2.chatgpt.site/ como referência adicional e autorizou imagens do anime e wallpapers. A versão refinada usa painéis claros com amarelo, uma variante escura e títulos com a tipografia SAO UI observada nessa referência. Os contornos apenas dos títulos usados estão em `heading-paths.json`; os arquivos de fonte não são publicados no repositório.

O cabeçalho `assets/aincrad-hero-reference.png` foi editado com imagegen a partir do wallpaper de https://wallpapersafari.com/w/F8j0Gb (imagem: https://cdn.wallpapersafari.com/23/83/F8j0Gb.jpg), preservando o desenho reconhecível do castelo. O wallpaper original é uma referência local; o README utiliza a arte adaptada. Créditos das referências aparecem no rodapé do perfil.

As imagens `*-light.svg` e `*-light-mobile.svg` acompanham o tema claro. Os demais painéis servem ao tema escuro. O elemento `picture` combina a preferência de cor com a largura da tela. As prévias locais em claro e escuro são aproximações, pois o estilo do texto é aplicado pelo próprio GitHub.

`heading-paths.json` é lido pelo gerador junto com o texto e os dados públicos. Ausência de contorno para um título novo usa texto normal como fallback. A preparação dos contornos é uma etapa local opcional em `prepare_type.py`, que usa fontTools já disponível no computador e os arquivos de fonte fornecidos pelo site de referência. Não há fonte remota nem biblioteca carregada pelo perfil publicado.

## Arquivos e responsabilidades

- `README.md`: documento exibido no GitHub. Lê as imagens em `assets`, oferece navegação interna, abre seções e aponta para os repositórios Let's Roll e Anime Check.
- `assets/aincrad-hero.png`: ilustração do cabeçalho.
- `assets/system-link.svg`: faixa de identificação com uma animação discreta, respeitando a preferência por movimento reduzido.
- `assets/quest-lets-roll.svg` e `assets/quest-anime-check.svg`: cartões de projetos, acompanhados das variantes `-mobile.svg` para telas de até 600px.
- `assets/skill-records.svg`: painel de tecnologias; a variante `-mobile.svg` distribui as categorias em uma coluna.
- `assets/activity-record.svg`: métricas e calendário de contribuições; a variante `-mobile.svg` adapta a composição.
- `build_profile.py`: gerador sem dependências externas. Recebe as fontes descritas abaixo, escapa os textos SVG, valida a conta e a existência das imagens; salva o README e os painéis.
- `github-public-data.json`: resposta pública consultada via GitHub GraphQL em 21/10/2026. Não contém tokens. É uma fotografia dos dados, não uma integração em tempo real.
- `texto-aprovado.md`: apresentação profissional da versão revisada pelo usuário, preservada na seção Player Profile.
- `preview.html` e `preview-mobile.html`: prévias locais aproximadas; o GitHub aplica seu próprio estilo ao documento.
- `referencia.md`: cópia local da referência enviada pelo usuário. Não é publicada.
- `PROMPT-ARTE.md`: prompt usado na geração do cabeçalho e identificação da ferramenta.

## Fluxo e manutenção

Dados públicos do GitHub + texto aprovado → `build_profile.py` → SVGs e README → GitHub renderiza o perfil.

O gerador só lê arquivos locais. Não consulta serviços, não recebe credenciais e não altera os projetos vinculados. Para atualizar as métricas, obtenha novamente os dados públicos, atualize também a data de consulta no gerador e execute `python build_profile.py`. A arte PNG precisa permanecer em `assets`.

O repositório de perfil recebe apenas README, assets e os arquivos necessários para manutenção do gerador. Prévias e referência ficam locais. As imagens antigas são preservadas no histórico e não precisam ser excluídas para o novo visual funcionar.

## Validação

- Geração dos SVGs e validação dos caminhos locais concluídas.
- Composição desktop inspecionada no navegador.
- Variantes móveis inspecionadas em um viewport de iframe com 390px.
- A versão final deve ser conferida no perfil publicado, incluindo imagens, links dos projetos e abertura das seções.

O banner é uma interpretação artística inspirada em Aincrad, sem pretensão de mapa ou arquitetura canônica. A personalização ocupa o README; os menus e o tema geral do GitHub são controlados pela plataforma.

