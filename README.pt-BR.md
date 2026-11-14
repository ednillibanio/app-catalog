[English](README.md) | Português

# Catálogo pessoal de apps

Padrões reutilizáveis para os repositórios de aplicações mantidos por ednillibanio. O repositório é público e independente: os repositórios de aplicações apontam para os padrões que seguem, e este repositório não os lista nem os acompanha. Os padrões definem os resultados esperados; a implementação pertence a cada aplicação e ao repositório pessoal `ci-workflows`. Este repositório não oferece nenhum workflow reutilizável.

- Os [padrões](docs/standards/README.pt-BR.md) cobrem contribuição, iterações, revisão, documentação, CI/DevSecOps e o backend Java/Quarkus, e explicam como uma aplicação os usa.
- O [guia do operador](docs/operations/operator-guide.pt-BR.md) explica como usar e manter este repositório.
- As [iterações](iterations/README.md) acompanham o trabalho planejado e as evidências (em inglês).
- A [procedência](PROVENANCE.md) registra as referências de projeto (em inglês).

Este repositório usa a branch `main`. Os repositórios de aplicações mantêm suas regras locais mais estritas, exceções e branches de integração nos próprios repositórios.

## Validação

Na raiz do repositório, confira os links locais de Markdown e os pares de idioma com `python3 scripts/check_docs.py` (veja o [guia do operador](docs/operations/operator-guide.pt-BR.md#manter-os-dois-idiomas)) e verifique os links e as evidências das iterações antes da revisão.

Licenciado sob a [Apache License 2.0](LICENSE).
