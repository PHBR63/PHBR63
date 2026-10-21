# Yellow Protocol — perfil PHBR63

Esta é a identidade atual do README do perfil: amarelo #FCEE09, preto #080C12, acentos ciano #00F0FF e atmosfera urbana inspirada em Cyberpunk 2077.

## Edição

Edite o README.md da raiz diretamente. Os assets publicados estão em assets/yellow-protocol. Os geradores históricos em profile-src e profile-src/cyberpunk agora salvam README.legacy.md em suas próprias pastas.

- banners: arte horizontal e composição compacta selecionada por picture até 600 px.
- projetos: três capas ilustradas em WebP, com descrição e link em texto no README.
- tecnologias: oito badges SVG, gerados por build_badges.py.
- animacoes: terminal e divisória em GIF, PNG estático e SVG editável.

As imagens WebP mantêm as dimensões das artes originais, com qualidade de exportação 88. Não há widgets externos ou requisições a serviços de estatísticas. A atividade é consultada no próprio GitHub.

## Regenerar badges

A partir da raiz do repositório:

```sh
python profile-src/yellow-protocol/build_badges.py
```

Python 3 e sua biblioteca padrão são suficientes. Edite a lista BADGES no script para mudar os rótulos. O gerador não altera o README.

## Regenerar animações

A partir da raiz, com Node.js e sharp instalados localmente:

```sh
node profile-src/yellow-protocol/build_animations.mjs
```

O script produz SVG, PNG e GIF; não altera o README. O terminal usa loop de 10 segundos e a divisória, de 12 segundos. A geração também aceita uma instalação de sharp indicada pela variável CODEX_PRIMARY_RUNTIME_NODE_MODULES.

No README, o GIF fica no source com prefers-reduced-motion: no-preference; o img usa PNG estático. O HTML deve preservar essa seleção na renderização de destino. Não há JavaScript nem CSS inline no perfil.

## Conteúdo e origem

A apresentação profissional e as tecnologias foram preservadas a partir do README anterior. O texto original completo continua em profile-src/texto-aprovado.md e profile-src/cyberpunk/about.md.

Os projetos apontam para os repositórios públicos de PHBR63: 3dGame, jogo-vr, lets-roll-cursor e anime-check. O README de 3dGame identifica o jogo da turma da ESPM; jogo-vr contém estrutura e pacotes Unity; Let's Roll se descreve como plataforma para RPG de mesa online em desenvolvimento.

As capas são artes conceituais, não capturas das aplicações. Os prompts de criação estão em prompts-imagens.json; as duas artes extras descritas nesse arquivo pertencem ao kit visual e não são usadas nesta composição.

Os badges são marcas tipográficas autorais, sem percentuais de domínio. A apresentação não inclui contadores de contribuições ou indicadores de atividade estáticos.

## Conferência após alterações

Confirme os links e arquivos locais do README. Revise em desktop e celular, nos temas claro e escuro. Em um navegador, compare currentSrc das imagens animadas com movimento normal e reduzido: o esperado é GIF no primeiro caso e PNG no segundo. Verifique também a seleção do banner compacto em até 600 px.

Use alt descritivo nas imagens de conteúdo e alt vazio na divisória decorativa. Mantenha nomes, descrições e links dos projetos em texto nativo.
