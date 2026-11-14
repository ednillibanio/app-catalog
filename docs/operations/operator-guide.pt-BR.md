[English](operator-guide.md) | Português

# Guia do operador

Este repositório define padrões reutilizáveis para os repositórios de aplicações. Ele não acompanha as aplicações que os usam, não roda builds de aplicações nem hospeda workflows de CI reutilizáveis; isso pertence a cada app e ao repositório publicado `ci-workflows`. Este catálogo usa localmente os hooks de pre-commit versionados desse repositório.

## Preparar um checkout

Instale o Git. Clone o repositório público e entre no diretório:

```sh
git clone https://github.com/ednillibanio/app-catalog.git
cd app-catalog
```

A branch de integração é a `main`. Para contribuir, identifique primeiro uma issue neste repositório; trabalho entre repositórios também deve ter uma issue em cada repositório afetado, ligada à issue mãe. Crie uma branch de tópico curta a partir da `main` atual, faça uma mudança focada, valide e abra um pull request para a `main`. Não edite código de aplicação a partir deste checkout do catálogo.

## Rodar os hooks do repositório

Instale o Git, o Python 3 e o `pre-commit` (por exemplo, `pipx install pre-commit`). Na raiz do repositório, instale o hook do Git e valide todos os arquivos versionados:

```sh
pre-commit install
pre-commit run --all-files
```

O `.pre-commit-config.yaml` fixa `sem-env`, `check-exec-bit` e `check-shdoc` na tag publicada `v0.1.0` do `ci-workflows`. Mantenha arquivos de ambiente reais fora do repositório; só `.env.example` e `.env.prod.example` são permitidos. Os checks de shell validam o modo de execução e os cabeçalhos de documentação quando há scripts de shell.

## Validar os links

Valide os links locais de Markdown durante a revisão com o check de [Manter os dois idiomas](#manter-os-dois-idiomas); nenhum job de CI o roda ainda.

## Manter os padrões e as iterações

Comece pelo [índice de padrões](../standards/README.pt-BR.md). O fluxo de iterações define os arquivos de plano, os valores de status, as aprovações de etapa, as evidências e o encerramento. Mantenha o trabalho aceito e não planejado em [`iterations/BACKLOG.md`](../../iterations/BACKLOG.md) (em inglês), com responsável e issue. Atualize o registro da iteração e a checklist da issue mãe quando o status de uma etapa mudar. Mantenha o trabalho pendente visível até ser resolvido; não marque uma etapa como concluída enquanto seus critérios de aceite não forem atendidos.

## Manter os dois idiomas

Os documentos para leitores existem em inglês (`name.md`, canônico) e em português do Brasil (`name.pt-BR.md`); o [padrão de documentação](../standards/documentation.pt-BR.md#idiomas) define quais arquivos são bilíngues e como se ligam. Quando alterar um, altere o outro no mesmo pull request, com o mesmo sentido. Para criar um documento, crie os dois arquivos, cada um começando com o link de troca de idioma, e aponte para o arquivo em português a partir das outras páginas em português.

É preciso ter Python 3 e Git. Na raiz do repositório, confira os pares de idioma, os links relativos e as âncoras de todos os arquivos Markdown, incluindo os ainda não versionados:

```sh
python3 scripts/check_docs.py
```

Uma execução limpa imprime `OK:` com o número de pares de idioma e termina com status 0. Caso contrário, lista cada par ausente, link de troca de idioma ausente, diferença no número de títulos, link ou âncora quebrados, ou página em português que aponta para a versão em inglês de um documento traduzido, e termina com status 1. Ele entende links inline (com título opcional e um nível de parênteses no destino), destinos entre sinais de menor e maior e definições de referência, decodifica caminhos e âncoras com codificação percentual e ignora blocos de código cercados e código inline. Blocos de código indentados são lidos como texto e títulos Setext (sublinhados com `===` ou `---`) não são reconhecidos, então use blocos cercados e títulos com `#`. O check compara a estrutura, não o sentido: revise cada par alterado lado a lado antes de pedir revisão.

## Solução de problemas

- Um link está quebrado: corrija o Markdown de origem e rode a validação correspondente de novo antes de abrir o PR.
- O check de idiomas aponta um par ausente ou uma diferença no número de títulos: crie ou complete o arquivo do outro idioma para que os dois tenham as mesmas seções e rode o check de novo.

## Limitações atuais

O catálogo não tem CI automatizado. Os hooks de pre-commit e o check de idiomas e links (`scripts/check_docs.py`) rodam localmente; não substituem um workflow do GitHub Actions. A validação no Linux e no Windows não é declarada.
