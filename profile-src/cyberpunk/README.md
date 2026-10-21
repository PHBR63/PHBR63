# PHBR63 — Cyberpunk

> **Material legado.** O `README.md` da raiz agora é editado diretamente; os assets atuais ficam em `assets/yellow-protocol`.
>
> Os geradores antigos servem somente às versões legadas: gravam `README.legacy.md` na própria pasta de fontes, sem sobrescrever o README da raiz. A documentação abaixo registra a versão anterior.

## Resultado

Redesign do perfil pessoal inspirado na identidade de Cyberpunk 2077: amarelo, preto, ciano, recortes angulares e uma arte urbana de cabeçalho. A estrutura parte do README (8).md enviado pelo usuário: projetos abertos e demais seções expansíveis.

O texto profissional aprovado e os dois projetos selecionados foram preservados. A apresentação atual não importa nem exibe os recursos do tema anterior.

## Arquivos e responsabilidades

- `README.md`: composição publicada no perfil. Usa as imagens em `assets/cyberpunk`, os links dos repositórios e os blocos `details`.
- `assets/cyberpunk/hero.png`: arte do cabeçalho produzida com imagegen integrada.
- `assets/cyberpunk/signal.svg`: faixa de identificação com movimento discreto, respeitando movimento reduzido.
- `assets/cyberpunk/lets-roll.svg` e `anime-check.svg`: cartões clicáveis dos projetos. Cada um tem uma variante `-mobile.svg`.
- `assets/cyberpunk/stack.svg`: painel de tecnologias e variante `stack-mobile.svg`.
- `assets/cyberpunk/stats.svg`: contagens verificadas e variante `stats-mobile.svg`.
- `assets/cyberpunk/activity.svg`: calendário de contribuições e variante `activity-mobile.svg`.
- `assets/cyberpunk/contact.svg`: cartão que abre o perfil público do GitHub.
- `build_profile.py`: gerador em Python com biblioteca padrão. Lê os arquivos locais abaixo, valida a conta, calcula a maior sequência de contribuições e escreve README/SVGs.
- `github-public-data.json`: snapshot da consulta pública do GitHub. Não inclui credenciais.
- `about.md`: apresentação profissional preservada.
- `title-paths.json`: contornos dos títulos usados nos painéis. Evita depender das fontes instaladas no navegador de quem visita o perfil.
- `PROMPT-ARTE.md`: prompt da imagem de cabeçalho e ferramenta utilizada.
- `preview.html` e `preview-mobile.html`: prévias locais aproximadas. Não são publicadas no perfil.
- `prepare_titles.py`: etapa local e opcional de autoria dos contornos, usando fontTools já disponível e a fonte Bahnschrift instalada no Windows. Não é necessária para executar o gerador ou exibir o perfil; o arquivo de fonte não é publicado.

No repositório, o gerador e as entradas ficam em `profile-src/cyberpunk`. Execute `python profile-src/cyberpunk/build_profile.py` a partir do repositório para regenerar o README e os painéis. O gerador mantém os mesmos caminhos de saída.

## Fluxo dos dados

Dados públicos + apresentação aprovada + contornos de títulos → gerador → README e SVGs → GitHub renderiza o perfil.

As imagens ficam no próprio repositório. Os cartões abrem Let's Roll e Anime Check. O tema não adiciona API, coleta de dados, autenticação, banco de dados ou serviço remoto. O calendário é um snapshot datado, não uma consulta em tempo real.

Para atualizar métricas, substitua o JSON pela nova consulta, atualize `DATE` no gerador e regenere os arquivos. Títulos novos sem contorno preparado usam texto normal como fallback.

## Verificação

- README e SVGs gerados sem erro.
- Caminhos das imagens validados pelo gerador.
- Tipografia e composição inspecionadas em desktop.
- Variante mobile conferida em iframe de 390px.
- Abertura das seções de tecnologias, números e atividade conferida no navegador.
- Antes da publicação, o patch passa por verificação de espaços e o estado remoto é comparado ao checkout local.

## Referências

- Estrutura: README (8).md fornecido pelo usuário.
- Direção visual: https://www.cyberpunk.net/br/pt-br/cyberpunk-2077

Arte de cabeçalho original criada com IA. A personalização é de fã, não representa material oficial da CD PROJEKT RED. O tema altera o README; a navegação e o fundo geral do GitHub permanecem sob controle da plataforma.

