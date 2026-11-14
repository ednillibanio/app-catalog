[English](README.md) | Português

# Catálogo pessoal de apps

Padrões e inventário leve das aplicações mantidas por ednillibanio. O catálogo define os resultados esperados; a implementação pertence a cada aplicação e, depois de publicada, ao repositório pessoal `ci-workflows`. Este catálogo não oferece nenhum workflow reutilizável.

- Os [padrões](docs/standards/README.pt-BR.md) cobrem contribuição, iterações, revisão, documentação e CI/DevSecOps.
- O [guia do operador](docs/operations/operator-guide.pt-BR.md) explica como usar e manter este repositório.
- O [catálogo](catalog/README.pt-BR.md) descreve o schema e os apps registrados.
- As [iterações](iterations/README.md) acompanham o trabalho planejado e as evidências (em inglês).
- A [procedência](PROVENANCE.md) registra as referências de projeto (em inglês).

O catálogo usa a branch `main`. Os repositórios de apps podem manter regras locais mais estritas e suas próprias branches de integração. A adoção inicial é acompanhada provisoriamente na [issue #103 do sapl-next](https://github.com/ednillibanio/sapl-next/issues/103); a issue mãe do catálogo é a [#1](https://github.com/ednillibanio/app-catalog/issues/1).

## Validação

Na raiz do repositório, valide `catalog/apps/*.json` contra `catalog/app.schema.json` com um validador de JSON Schema Draft 2020-12. Confira os links locais de Markdown e os pares de idioma com `python3 scripts/check_docs.py` (veja o [guia do operador](docs/operations/operator-guide.pt-BR.md#manter-os-dois-idiomas)) e verifique os links e as evidências das iterações antes da revisão. Veja a [validação do catálogo](catalog/README.pt-BR.md). O schema e as entradas são dados, não evidência de adoção.

Licenciado sob a [Apache License 2.0](LICENSE).
