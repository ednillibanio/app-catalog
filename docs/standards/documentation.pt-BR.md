[English](documentation.md) | Português

# Documentação

Escreva para um leitor que não conhece o projeto. Descreva finalidade, pré-requisitos, configuração, comandos, efeitos, validação e solução de problemas, quando se aplicarem. Baseie as afirmações sobre comportamento na implementação, identifique as suposições e separe exemplos de checagens executadas. Mantenha a navegação e os links locais válidos. Não exponha credenciais nem dados privados de organizações. Registre exceções e responsáveis como descrito no [índice de padrões](README.pt-BR.md).

## Idiomas

Este catálogo mantém seus documentos para leitores (`README.md`, `CONTRIBUTING.md` e `docs/`) em inglês e em português do Brasil. `name.md` é a versão canônica em inglês e `name.pt-BR.md`, na mesma pasta, é a tradução. Altere os dois no mesmo pull request e mantenha cada regra, comando, link e exceção com o mesmo sentido; quando divergirem, corrija o arquivo em português para ficar igual ao em inglês.

Cada arquivo começa com um link para o outro idioma. Num arquivo em português, aponte para a versão em português de um documento traduzido e para o título correspondente; links para arquivos só em inglês, para arquivos que não são Markdown e para URLs externas ficam como estão. Instruções para agentes, procedência, registros de iteração, issues, pull requests e commits são só em inglês. Preserve nomes e o idioma do produto quando necessário.

O catálogo não define o idioma do produto nem da documentação de um app. Cada app declara seu idioma nas próprias instruções para agentes e aponta para a versão do catálogo nesse idioma. Ferramentas e automação (scripts, executores de tarefas, arquivos do Compose, `.env.example` e workflows de CI) são escritos em inglês, um idioma por arquivo, como exige o padrão de [ambiente de desenvolvimento local](dev-environment.pt-BR.md#10-idioma-das-ferramentas).

Cada app mantém um mapa de idiomas nas suas instruções para agentes: uma tabela que diz, para cada tipo de artefato, qual idioma ele usa e por quê. Assim ninguém precisa adivinhar, e um arquivo que mistura idiomas fica evidente. Por exemplo:

| Artefato | Idioma | Motivo |
| --- | --- | --- |
| Scripts, executor de tarefas, arquivos do Compose, `.env.example`, workflows de CI | Inglês | Os comandos das ferramentas são em inglês ([ambiente de desenvolvimento local](dev-environment.pt-BR.md#10-idioma-das-ferramentas)) |
| Identificadores do código | O idioma que o app escolheu | Padrões de backend e frontend: um vocabulário por app |
| Textos do produto e mensagens ao usuário | O idioma do produto | Os usuários os leem |
| Documentação, iterações, issues, pull requests, descrições de commit | O idioma que o app declara | Quem mantém e contribui os lê |
