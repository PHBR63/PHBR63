# Neon Protocol — perfil PHBR63

Identidade visual do README de Pedro Zampronha, inspirada em Cyberpunk 2077. A composição usa fundos opacos e grandes superfícies de amarelo `#FCEE09`, ciano `#00F0FF` e vermelho `#FF375A`, com acentos magenta `#F35CDB` sobre preto `#080C12`.

## Composição

O README contém banner, apresentação ilustrada, terminal animado, tecnologias por área, quatro projetos, trajetória e acesso aos repositórios. As imagens ocupam toda a largura disponível da coluna. Nomes, descrições, tecnologias e links também estão preservados em Markdown nativo na seção expansível **Ler perfil em texto**.

- `assets/neon-protocol`: painéis SVG de 1200 px e variantes de 600 px, terminal mobile e capa de Anime Check.
- `assets/yellow-protocol`: banner horizontal e compacto, capas dos outros três projetos e animações desktop.
- `build_primary.py`: apresentação, cabeçalho de projetos e terminal mobile estático.
- `build_secondary.py`: tecnologias, trajetória, descrições dos projetos e rodapé.
- `build_mobile_animation.mjs`: terminal mobile animado, gerado a partir do SVG estático.
- `build_readme.py`: composição HTML/Markdown e texto completo do perfil.
- `anime-cover-prompt.json`: prompt, referências e origem da capa de Anime Check.
- `manifest-assets.json`: dimensões, tamanhos e hashes dos arquivos desta versão.

As capas são ilustrações conceituais. Nenhum painel representa captura da aplicação, medição de domínio técnico ou indicador de atividade em tempo real.

## Espaçamento e organização

Cada painel tem um contêiner de parágrafo próprio no README, para que as margens nativas do GitHub produzam intervalos consistentes. Uma quebra adicional marca a entrada de Tecnologias, Projetos e Trajetória. Dentro de cada projeto, capa e descrição permanecem no mesmo link e no mesmo parágrafo. As imagens usam `align="top"` para reduzir a emenda causada pelo alinhamento de linha de base.

Os painéis usam margens horizontais de 40 px nos arquivos desktop e 32 px nos arquivos mobile. O ritmo interno segue intervalos de 8, 16, 24, 32 e 48 px, com altura dos cartões de projeto calculada a partir do conteúdo. Tecnologias, descrição e chamada para abrir o repositório são grupos separados. A conferência final de espaçamento ocorre no perfil publicado, porque o GitHub aplica seu próprio renderizador ao HTML.

## Atualizar

A partir da raiz do repositório:

```sh
python profile-src/neon-protocol/build_primary.py
python profile-src/neon-protocol/build_secondary.py
node profile-src/neon-protocol/build_mobile_animation.mjs
python profile-src/neon-protocol/build_readme.py
```

O primeiro e o último scripts usam apenas Python 3 e sua biblioteca padrão. O gerador secundário usa Pillow para medir textos e as fontes DejaVu Sans/Mono instaladas em `/usr/share/fonts/truetype/dejavu`. O gerador de GIF usa Node.js e `sharp`; aceita instalação local ou a variável `CODEX_PRIMARY_RUNTIME_NODE_MODULES` apontando para os módulos. Essas dependências só participam da geração. Os arquivos publicados são autossuficientes e não carregam fontes ou scripts externos.

Edite o conteúdo textual em `build_readme.py` e os trechos correspondentes nos geradores gráficos. Depois execute os scripts e confira o resultado. O gerador atual escreve o README da raiz; os geradores anteriores de Aincrad e Cyberpunk continuam restritos aos seus arquivos `README.legacy.md`.

## Responsividade e movimento

O elemento `picture` seleciona os painéis mobile em telas de até 600 px. O breakpoint se refere à largura da janela, não à coluna interna do GitHub. As capas dos projetos mantêm a proporção 2:1; suas descrições têm composição própria para celular.

O terminal possui duas animações: desktop e mobile. As fontes animadas exigem `prefers-reduced-motion: no-preference`. Quando essa condição não é atendida, o README seleciona SVG estático no celular e PNG estático no desktop. A divisória também tem GIF e PNG estático. Não há animações por JavaScript nem CSS injetado no perfil.

As imagens possuem fundo opaco para manter as cores nos temas claro e escuro. A personalização ocupa o conteúdo do README; o GitHub controla a moldura, os menus e o tema geral da página.

## Conteúdo

A biografia e a experiência profissional foram preservadas a partir do texto aprovado em `profile-src/texto-aprovado.md` e da apresentação anterior. Os projetos são os repositórios públicos `3dGame`, `jogo-vr`, `lets-roll-cursor` e `anime-check` da conta PHBR63.

Não há widgets de estatísticas, números de proficiência, disponibilidade profissional presumida ou contatos não fornecidos. O rodapé abre a lista real de repositórios.

## Conferência

Antes de publicar, confira os caminhos locais, XML dos SVGs, dimensões, medidas de texto e os hashes dos arquivos. Veja as composições desktop e mobile, inclusive as linhas mais longas. Após publicar, confira no perfil se todas as imagens carregaram, se as fontes de `picture` foram preservadas e se os projetos e a seção expansível continuam acessíveis.

Os SVGs usam fontes locais com alternativas do sistema. Pequenas diferenças de tipografia podem ocorrer entre navegadores. As imagens têm descrições alternativas e o conteúdo completo permanece disponível na versão em texto.
