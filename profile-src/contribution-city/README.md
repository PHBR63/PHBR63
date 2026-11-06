# Cidade de contribuições

O workflow `.github/workflows/profile-3d.yml` consulta o calendário público de
PHBR63 diariamente às **06:17 UTC (03:17 em Brasília)** e permite execução manual
em **Actions → Cidade de contribuições → Run workflow**. O agendamento depende
da fila e da disponibilidade do GitHub Actions; não é uma execução em tempo real.

## Arquivos e fluxo

1. O workflow executa `test_generate.py` antes de consultar a rede.
2. `generate.py` recebe `--username` (PHBR63 por padrão) e `--output` opcional;
   consulta `https://github.com/users/PHBR63/contributions` por HTTPS, sem token.
3. O parser valida datas únicas, sequência contínua, níveis entre 0 e 4 e recência.
   O calendário contém aproximadamente um ano; os níveis não são contagens.
4. O renderizador mantém a paleta, as bases fixas e as barras ascendentes da cidade.
   Somente após a validação o SVG é substituído atomicamente.
5. O workflow faz commit apenas de `profile-3d-contrib/profile-night-rainbow.svg`,
   utilizado pelo README do perfil e sua versão estática.

O `GITHUB_TOKEN` temporário do workflow é usado pelo checkout/git para gravar o
arquivo, com permissão `contents: write`. Nenhum token pessoal ou segredo novo
é necessário. Não há banco, API própria ou dependências Python externas.

## Testar localmente

```sh
python -B -m unittest discover -s profile-src/contribution-city -v
python -B profile-src/contribution-city/generate.py --username PHBR63 --output city-preview.svg
```

Os testes verificam rejeição de dados inválidos sem perda da imagem anterior,
alturas ascendentes com bases fixas e repetição sem alterações no mesmo dia.
Abra o SVG gerado no navegador para conferir a aparência.

## Falhas e manutenção

Falhas HTTP, calendário incompleto ou mudanças no HTML do GitHub interrompem a
execução, preservando a cidade anterior. O erro fica no log do Actions. O gerador
depende dos atributos públicos `data-date` e `data-level`; uma mudança no site pode
exigir ajuste do parser. Se houver alteração concorrente no repositório, o push
falha sem sobrescrever commits; execute novamente após verificar o log.

O workflow só faz commit se o SVG mudar. A data de consulta é registrada em sua
descrição acessível. O GitHub pode atrasar execuções e desativar agendamentos de
repositórios públicos inativos; o estado pode ser conferido na aba Actions.

Para pausar, use **Disable workflow** na página do workflow. Para reverter o visual,
pause o workflow e restaure o SVG de um commit anterior. A automação não altera
os outros cards, GIFs, textos ou links do perfil.
