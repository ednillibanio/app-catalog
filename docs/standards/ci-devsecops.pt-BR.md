[English](ci-devsecops.md) | Português

# Resultados de CI e DevSecOps

Cada app documenta seus comandos de validação e seus responsáveis. O CI deve cobrir higiene do repositório, detecção de segredos, metadados do pull request, build e testes relevantes, análise estática, dependências e SBOMs (software bills of materials), quando se aplicarem. Identifique os checks obrigatórios e os informativos, e mostre as falhas de execução dos scanners separadas dos achados. Registre achados aceitos, responsáveis e issues de acompanhamento; não declare cobertura sem evidência.

O repositório público e pessoal `ci-workflows` publica hooks de pre-commit e workflows reutilizáveis do GitHub Actions. Fixe os hooks numa tag SemVer publicada e os workflows reutilizáveis em SHAs completos de commit. Este catálogo usa os hooks localmente; ainda não roda CI automatizado. Os apps mantêm o CI que já têm até que um plano de adoção autorize e valide as interfaces relevantes. Dê ao CI só as permissões necessárias e não exponha segredos a pull requests não confiáveis. Este padrão não implementa jobs, não publica imagens, não faz deploy nem especifica a instalação de ambientes de desenvolvimento.
