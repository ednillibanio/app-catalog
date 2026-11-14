[English](dev-environment.md) | Português

# Ambiente de desenvolvimento local

Este padrão vale para o ambiente de desenvolvimento local de um repositório de aplicação: as ferramentas que quem contribui instala, os serviços que sobem na sua máquina, a configuração que muda de uma máquina para outra e os comandos do dia a dia. Ele define como uma aplicação dá suporte a vários sistemas operacionais sem que um ambiente quebre outro, e como o guia de cada ambiente diz se ele foi validado. Cada aplicação registra no próprio repositório os ambientes suportados, os serviços, as portas, as variáveis, as versões exatas e as regras mais estritas, como descrito em [Como usar estes padrões](README.pt-BR.md#como-usar-estes-padrões).

Os exemplos usam o vocabulário neutro `inventory` do padrão de [backend Java/Quarkus](java-quarkus-backend.pt-BR.md), o Make como executor de tarefas e o Docker Compose para os serviços. Make e Compose são exemplos, não exigências. Os trechos marcados como "ilustrativos" mostram uma forma e não foram feitos para rodar sozinhos; os demais foram executados quando este padrão mudou, como registram as evidências da iteração.

## 1. Ambientes suportados

Cada aplicação declara os ambientes que suporta, nas suas instruções para agentes e no seu guia de desenvolvimento. Ela escolhe deste conjunto de referência e informa as versões exatas do sistema operacional e das ferramentas:

| Ambiente | Configuração típica |
| --- | --- |
| macOS | Um runtime de contêineres como o Colima com a CLI do Docker, ou o Docker Desktop; ferramentas de um gerenciador de pacotes como o Homebrew |
| Máquina virtual Linux | Uma VM gerenciada por uma ferramenta como o Vagrant, com Docker ou Podman dentro dela |
| Linux | Docker ou Podman nativo |
| WSL2 | Uma distribuição Linux no Windows, com Docker ou Podman |
| Windows | PowerShell com Docker Desktop |

Todo ambiente suportado tem um guia (§11), um script de setup (§5), uma checagem doctor (§6) e os comandos comuns (§8). Um ambiente sem algum desses itens é uma exceção e registra o responsável, o motivo, o escopo, a data de expiração ou de revisão e a issue de acompanhamento exigidos pelo [índice de padrões](README.pt-BR.md); o guia dele documenta os passos manuais que substituem o que falta, e o estado de validação é `Not validated` (§11). Este padrão não concede exceção permanente a nenhum ambiente.

## 2. Arquivos do repositório

| Arquivo | Papel |
| --- | --- |
| `.env.example` | Versionado. Lista toda variável que pode mudar entre máquinas, com o valor padrão |
| `.env` | Local e ignorado pelo Git. Guarda os valores desta máquina |
| Arquivo do Compose (por exemplo `compose.yaml`) | Versionado. Define os serviços de desenvolvimento |
| Arquivo do executor de tarefas (por exemplo `Makefile`) | Versionado. Define os comandos comuns (§8) |
| `scripts/<ambiente>/` | Versionado. Scripts de setup, doctor e bootstrap de um ambiente |
| Arquivos de versão (por exemplo `.nvmrc`, `.sdkmanrc`, `packageManager` no `package.json`, wrapper da ferramenta de build) | Versionados. Fonte única da versão de cada ferramenta (§4) |
| `.gitattributes` | Versionado. Fins de linha dos scripts (§9) |
| `docs/operations/` (ou o equivalente da aplicação) | Um guia por ambiente e um guia compartilhado (§11) |

## 3. Configuração e `.env`

1. As diferenças entre ambientes e máquinas ficam só no `.env` local. Os arquivos versionados guardam valores que funcionam em todos, e escolhas de um ambiente viram variáveis com valor padrão.
2. O `.env` nunca é commitado. O `.gitignore` o exclui e os hooks do repositório o rejeitam.
3. O `.env.example` documenta toda variável: finalidade, valor padrão, quando mudar e quais comandos a leem. Uma variável lida mas ausente do `.env.example` é um defeito.
4. O projeto funciona sem `.env`: toda variável tem um padrão de desenvolvimento no arquivo que a lê.
5. O `.env` usa um subconjunto portável, que o Compose e um shell POSIX que carrega o arquivo leem do mesmo jeito: um `NOME=valor` por linha, com um nome feito de letras, dígitos e sublinhados que não começa com dígito, e comentários com `#` em linhas próprias. Um valor ou fica sem aspas e só tem letras, dígitos e os caracteres `_ . - / : , @ + =`, ou fica inteiro entre aspas simples ou duplas, sem `$`, barra invertida, crase, o próprio caractere de aspas nem quebra de linha dentro. Não há expansão de variáveis, substituição de comandos, sequências de escape nem valores em várias linhas. O `.env.example` e o `.env` usam fim de linha LF, porque um shell mantém o retorno de carro no valor: o `.gitattributes` garante isso para o `.env.example` (§9), e a checagem doctor aponta um `.env` que tenha retornos de carro (§6).
6. O executor de tarefas e o arquivo do Compose leem o mesmo `.env`. Um valor derivado de outras variáveis (por exemplo, uma URL montada a partir de uma porta) é calculado num lugar só, em geral no executor de tarefas.
7. A aplicação documenta a precedência quando uma variável já está definida no shell. No exemplo abaixo, um comando rodado pelo executor de tarefas usa o valor do `.env`, porque carrega o `.env` antes de chamar o Compose, enquanto uma chamada direta ao Compose deixa o valor do shell vencer.
8. Um comando direto que não passa pelo executor de tarefas (por exemplo, a ferramenta de build rodada de uma subpasta) precisa das variáveis que lê definidas no shell. O guia compartilhado as lista.

```dotenv
# -----------------------------------------------------------------------------
# Compose (read by the Makefile)
# -----------------------------------------------------------------------------
# Default: Docker. For Podman, uncomment both lines.
# Some podman-compose versions do not support the --wait flag used by `make up`.
# COMPOSE=podman-compose
# COMPOSE_UP_FLAGS=-d

# Address where services publish their ports. Keep 127.0.0.1 unless a guide
# says otherwise for its environment.
# BIND_ADDRESS=127.0.0.1

# -----------------------------------------------------------------------------
# PostgreSQL (development credentials only)
# -----------------------------------------------------------------------------
POSTGRES_DB=inventory
POSTGRES_USER=inventory
POSTGRES_PASSWORD=inventory-dev
# Published host port. Change it when the default port is occupied.
POSTGRES_PORT=5432
```

## 4. Versões das ferramentas

1. Cada versão de ferramenta é fixada uma vez, no arquivo que o repositório já usa para ela: um arquivo de versão do runtime, o campo `packageManager` aplicado pelo Corepack, o wrapper da ferramenta de build ou a tag de imagem no arquivo do Compose.
2. Scripts de setup, checagens doctor e a CI leem esses arquivos; não repetem as versões.
3. A ferramenta de build roda pelo seu wrapper (por exemplo `mvnw`), e quem contribui não precisa instalá-la à parte.
4. As imagens usam nome totalmente qualificado e uma tag (por exemplo `docker.io/library/postgres:<tag>`). O Podman não resolve nomes curtos como o Docker resolve.
5. A escolha do runtime fixado não depende de um hook do shell estar ligado; o executor de tarefas a define explicitamente quando pode.

## 5. Setup

Cada ambiente suportado tem um script de setup que instala ou configura o que ele precisa.

1. É idempotente: cada passo confere antes de agir, e uma segunda execução não muda nada.
2. Aceita `--dry-run`, que mostra o que faria sem mudar nada.
3. Nunca apaga dados, o `.env` ou volumes, e nunca substitui um arquivo que não criou.
4. Não instala o gerenciador de pacotes base nem o gerenciador de SDKs do sistema operacional; diz a quem contribui como instalar e para.
5. Na própria máquina de quem contribui, não eleva privilégios e não muda padrões globais em silêncio (runtime padrão, contexto global de contêineres, perfil do shell). Quando uma mudança é necessária, ele avisa e pergunta ou mostra o comando.
6. Um provisionador que roda dentro de uma VM descartável pode usar passos privilegiados e definir os padrões da VM; o cabeçalho dele diz isso.
7. Termina indicando a checagem doctor (§6).

Ilustrativo: um passo que confere antes de instalar e aceita dry-run.

```bash
install_if_missing() {
  local command_name="$1"
  shift
  if command -v "$command_name" >/dev/null 2>&1; then
    echo "[ OK ] $command_name already installed"
  elif [[ "${DRY_RUN:-0}" == 1 ]]; then
    echo "[PLAN] would run: $*"
  else
    "$@"
  fi
}

install_if_missing colima brew install colima
```

## 6. Doctor

Cada ambiente suportado tem uma checagem doctor.

1. Ela só lê; não instala nem muda nada.
2. Confere cada pré-requisito: runtime de contêineres e Compose, a versão de cada runtime fixado, a versão do gerenciador de pacotes, o wrapper da ferramenta de build e o que mais o ambiente precisar.
3. Mostra uma linha por item e, para cada falha, o comando ou passo que a corrige.
4. Sai com status diferente de zero quando um item obrigatório falha, para que scripts e pessoas possam confiar nela. Itens opcionais viram avisos e não mudam o status de saída.

Um exemplo parcial: uma checagem doctor real também cobre o gerenciador de pacotes, o wrapper da ferramenta de build e os outros pré-requisitos do seu ambiente.

```bash
#!/usr/bin/env bash
# Read-only environment check. Exits 1 when a required check fails.
set -euo pipefail

failures=0

check() {
  local description="$1" fix="$2"
  shift 2
  if "$@" >/dev/null 2>&1; then
    echo "[ OK ] $description"
  else
    echo "[FAIL] $description -> $fix" >&2
    failures=$((failures + 1))
  fi
}

# Accepts a numeric pin such as 26, 26.13 or v26.13.0 in .nvmrc.
node_matches_nvmrc() {
  local pin current
  pin="$(tr -d '[:space:]v' < .nvmrc)"
  current="$(node --version)"
  [[ "$current" == "v$pin" || "$current" == "v$pin."* ]]
}

check "container runtime responds" "start the container runtime" docker info
check "Compose is available" "install the Compose plugin" docker compose version
env_has_lf_endings() {
  [[ -e .env || -L .env ]] || return 0
  [[ -f .env && -r .env ]] || return 1
  local status=0
  grep -q $'\r' .env || status=$?
  # grep exits 1 when no carriage return is found; 0 or an error fails.
  [[ "$status" -eq 1 ]]
}

check "Node matches .nvmrc" "run the setup command" node_matches_nvmrc
check ".env uses LF line endings" "convert .env to LF line endings" env_has_lf_endings

if ((failures > 0)); then
  echo "$failures check(s) failed." >&2
  exit 1
fi
echo "All checks passed."
```

## 7. Bootstrap

Recomenda-se um comando de bootstrap: um único comando que leva um clone novo a um ambiente funcionando.

1. Ele roda o setup, sobe os serviços, prepara o que os testes precisam (por exemplo, um banco de testes) e termina com a checagem doctor.
2. Cria o `.env` a partir do `.env.example` só quando o `.env` não existe. Mantém um `.env` existente e os volumes de dados existentes.
3. Pode ajustar valores de um `.env` que acabou de criar (por exemplo, escolher uma porta livre quando a padrão está ocupada); não reescreve um `.env` existente e, em vez disso, informa a variável a mudar.
4. Uma mudança de estado global de que precise (por exemplo, um contexto de contêineres) vale só para os próprios comandos, ou é desfeita quando ele termina.

```bash
if [[ ! -e .env ]]; then
  cp .env.example .env
  chmod 600 .env
  echo "Created .env from .env.example."
else
  echo "Keeping the existing .env."
fi
```

## 8. Comandos comuns

Todo ambiente suportado oferece o mesmo conjunto mínimo de comandos, com os mesmos nomes e o mesmo efeito, por um executor de tarefas ou um script wrapper que rode nele. Comandos diretos escritos num guia documentam o que um comando faz; não o substituem.

| Comando | Efeito |
| --- | --- |
| `help` | Lista os comandos disponíveis com uma descrição de uma linha |
| `setup` | Instala as ferramentas que faltam; idempotente (§5) |
| `doctor` | Confere o ambiente sem mudá-lo (§6) |
| `up` | Sobe os serviços de desenvolvimento e espera os health checks, ou diz como conferir se estão prontos quando a implementação do Compose não consegue esperar |
| `down` | Para os serviços e mantém os volumes de dados |
| `test` | Roda as suítes de teste |
| `dev` | Roda os servidores de desenvolvimento |
| `check` | Roda as checagens de build, lint e testes que a CI também roda, e diz quais jobs da CI ele não cobre |

1. Uma aplicação com vários componentes pode dividir `test` e `dev` por componente (por exemplo `backend-test` e `frontend-dev`), desde que os nomes sejam iguais em todos os ambientes.
2. Um comando que apaga dados, como remover volumes, tem nome próprio e explícito, e a descrição diz que ele é destrutivo. Nenhum comando do conjunto mínimo apaga dados.
3. Recomenda-se um comando `smoke`, que confere a aplicação rodando de ponta a ponta (por exemplo, um login real num navegador).
4. `help` é o comando padrão.

Ilustrativo: parte de um Makefile.

```make
# .env is read by the shell, not by Make, so quoted values keep shell meaning.
LOAD_ENV := $(if $(wildcard .env),set -a && . ./.env && set +a &&)
COMPOSE_CMD := $${COMPOSE:-docker compose}

.DEFAULT_GOAL := help
.PHONY: help up ps down clean-data

help: ## List the available commands
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*## "}; {printf "  %-12s %s\n", $$1, $$2}'

up: ## Start the services; wait for health checks when the flags include --wait
	$(LOAD_ENV) flags="$${COMPOSE_UP_FLAGS:--d --wait}" && \
		$(COMPOSE_CMD) up $$flags && \
		case " $$flags " in *" --wait "*) ;; \
		*) echo "Not waiting for health checks: run 'make ps' until every service is healthy." ;; esac

ps: ## Show the services and their health
	$(LOAD_ENV) $(COMPOSE_CMD) ps

down: ## Stop the services and keep their data volumes
	$(LOAD_ENV) $(COMPOSE_CMD) down

clean-data: ## DESTRUCTIVE: stop the services and delete their data volumes
	$(LOAD_ENV) $(COMPOSE_CMD) down -v
```

## 9. Compatibilidade entre ambientes

1. O arquivo do Compose funciona com Docker e Podman: nomes de imagem totalmente qualificados (§4), a opção `z` nos bind mounts para hosts com SELinux, health checks em todos os serviços e uma forma de conferir se estão prontos que não dependa só do `--wait`.
2. Os serviços publicam as portas em `127.0.0.1` por padrão. Publicar em outras interfaces é opcional, por uma variável do `.env`, e documentado com o seu risco (§13).
3. As portas são variáveis com valor padrão (§3), e quem contribui pode tirar um serviço de uma porta ocupada sem editar arquivos versionados.
4. Uma configuração de que um ambiente precisa e que os outros toleram fica no arquivo versionado, com um comentário que diz o ambiente e o motivo. Quem está em outro ambiente não a remove.
5. Numa VM, a aplicação documenta onde fica a árvore de trabalho. Um clone dentro da VM é a opção quando pastas compartilhadas causam problemas com links simbólicos, permissões ou desempenho. No WSL2, mantenha a árvore de trabalho no sistema de arquivos do Linux, e não em `/mnt/c`, como a documentação do WSL da Microsoft recomenda por desempenho.
6. Scripts de shell, o arquivo do executor de tarefas e outros arquivos que rodam no Linux mantêm fins de linha LF em qualquer checkout, inclusive no Windows; o `.gitattributes` garante isso.
7. Um script de shell POSIX rodado diretamente, como um script de setup ou de doctor ou o wrapper Unix da ferramenta de build (`mvnw`), começa com um shebang e fica no Git com modo `100755`. Uma biblioteca de shell que outros scripts carregam com `source` não tem shebang e fica com modo `100644`. Scripts PowerShell e batch não usam shebang nem o modo executável. No Windows o Git costuma rodar com `core.fileMode=false` e não registra o modo sozinho, então quem contribui de lá o define com `git update-index --chmod=+x <arquivo>`. Os hooks do repositório conferem os modos.

```yaml
services:
  postgres:
    image: docker.io/library/postgres:<tag>
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-inventory}
      POSTGRES_USER: ${POSTGRES_USER:-inventory}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-inventory-dev}
    ports:
      - "${BIND_ADDRESS:-127.0.0.1}:${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infra/postgres/init:/docker-entrypoint-initdb.d:ro,z
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

`<tag>` é um marcador para a tag que cada aplicação fixa neste arquivo (§4).

```gitattributes
* text=auto
*.sh text eol=lf
.env.example text eol=lf
Makefile text eol=lf
mvnw text eol=lf
*.cmd text eol=crlf
*.bat text eol=crlf
```

Ilustrativo: uma configuração mantida por causa de um ambiente.

```ini
# Required by the <environment> guide: its shared folders do not support symlinks.
node-linker=hoisted
symlink=false
```

## 10. Idioma das ferramentas

1. Scripts, o arquivo do executor de tarefas, arquivos do Compose, o `.env.example` e workflows de CI são escritos em inglês: os nomes que eles definem, as mensagens e os comentários. Seus comandos e ferramentas são em inglês, qualquer que seja o idioma que a aplicação usa no produto e na documentação.
2. Um arquivo, ou um conjunto de scripts que trabalham juntos, nunca mistura idiomas.
3. Identificadores do produto e do domínio que aparecem nas ferramentas, como um serviço, um banco ou um comando com nome de um conceito do domínio, mantêm o vocabulário que a aplicação escolheu.
4. A aplicação lista essas escolhas no seu mapa de idiomas, como descrito em [Documentação](documentation.pt-BR.md#idiomas).

## 11. Guias de ambiente

1. Cada ambiente suportado tem o próprio guia na documentação de operação da aplicação.
2. O conteúdo igual em todos os ambientes (rotina diária, serviços, testes, usuários de teste, problemas comuns que não dependem do ambiente) fica num guia compartilhado. O guia de um ambiente traz só o que muda e aponta para o guia compartilhado.
3. O guia de um ambiente cobre pré-requisitos, preparação, os valores do `.env` que esse ambiente muda, como conferi-lo (doctor e, se houver, smoke) e os problemas comuns específicos dele.
4. Cada guia começa com o seu estado de validação:
   - `Validated`: a data, a revisão do repositório, quem validou e os comandos rodados, pelo menos setup ou bootstrap, doctor, `check` e `smoke` quando existir.
   - `Not validated`: o guia foi revisado só contra o repositório; ele informa a issue de acompanhamento e quem pode validar, por exemplo alguém que use esse ambiente.
5. Um ambiente só é dado como validado com essa evidência. Uma mudança num arquivo compartilhado (§12) deixa os outros ambientes sem validação para aquela mudança até alguém rodá-la neles.

Ilustrativo: as primeiras linhas de dois guias.

```markdown
> **Validation state:** `Validated` on 2026-11-14 at revision `abc1234` by the maintainer.
> Commands run: `make bootstrap`, `make doctor`, `make check`, `make smoke`.
```

```markdown
> **Validation state:** `Not validated`. Reviewed against the repository at revision `abc1234`;
> not run on this environment. Tracking issue: #123. Can be validated by a contributor using
> Windows with Docker Desktop.
```

## 12. Mudar um ambiente

1. Teste a mudança no ambiente que você está usando e registre no pull request qual foi.
2. Não remova nem quebre algo de que outro ambiente depende (§9, regra 4). Quando um arquivo compartilhado muda (o arquivo do Compose, o do executor de tarefas, o `.env.example`, os arquivos de versão), revise os guias e scripts dos outros ambientes contra a mudança.
3. O pull request diz quais ambientes foram rodados e quais foram só revisados. Para cada ambiente não rodado, aponta a issue de acompanhamento ou abre uma para alguém que o use.
4. Uma mudança que cria ou renomeia uma variável atualiza o `.env.example` e os guias que a citam no mesmo pull request.

## 13. Segurança

1. O `.env.example` e os arquivos versionados têm só credenciais de desenvolvimento, reconhecíveis como tal. Credenciais reais nunca entram no repositório, no `.env.example` nem num guia.
2. Segredos locais gerados, como certificados de desenvolvimento e chaves privadas, ficam num diretório ignorado pelo Git.
3. Publicar um serviço além de `127.0.0.1` é opcional, limitado a redes confiáveis e documentado com os serviços que expõe. Serviços que guardam dados continuam locais, a não ser que um guia diga por que não podem.
4. A chave privada de uma autoridade certificadora local fica na máquina que a criou e nunca é compartilhada nem commitada. Dispositivos que precisam confiar nela recebem só o certificado público.
5. Scripts de setup baixam ferramentas só da fonte oficial de cada uma ou do gerenciador de pacotes do sistema operacional.

## 14. Antipadrões

| Não use | Use |
| --- | --- |
| Um valor de uma máquina num arquivo versionado | Uma variável com padrão e um valor no `.env` |
| Uma variável lida por um comando e ausente do `.env.example` | Uma entrada no `.env.example` com finalidade e padrão |
| Uma versão repetida num script | O arquivo de versão (§4) |
| Um nome curto de imagem | Um nome de imagem totalmente qualificado, com tag |
| Um passo de setup que reinstala ou sobrescreve sempre | Uma conferência antes de cada passo |
| Um script de setup que apaga o `.env` ou volumes | Um comando separado e explicitamente destrutivo |
| Uma checagem doctor que corrige coisas | Uma checagem só de leitura que mostra a correção |
| Um nome de comando que existe em um ambiente só | O conjunto de comandos comuns (§8) |
| Um `down` que apaga volumes | Um `down` que os mantém, mais um comando destrutivo |
| Remover uma configuração de que outro ambiente precisa | Um comentário com o ambiente e o motivo |
| Um guia que afirma que um ambiente funciona sem tê-lo rodado | O estado de validação (§11) |
| Scripts em dois idiomas | Ferramentas em inglês, um idioma por arquivo (§10) |
| Um script de shell rodado diretamente mas guardado sem o modo executável | Modo `100755` no Git, definido com `git update-index --chmod=+x` no Windows (§9) |
| Serviços publicados em todas as interfaces por padrão | `127.0.0.1` por padrão, publicação ampla opcional |

## 15. Checklist do pull request

Todo pull request que muda o ambiente de desenvolvimento segue as seções que se aplicam. Um desvio é uma exceção e registra o responsável, o motivo, o escopo, a data de expiração ou de revisão e a issue de acompanhamento exigidos pelo [índice de padrões](README.pt-BR.md), seja no pull request, seja nas regras locais da aplicação.

- [ ] Variáveis novas ou alteradas estão no `.env.example` com finalidade e padrão, e o `.env` não foi commitado (§3).
- [ ] As versões vêm dos arquivos de versão (§4).
- [ ] Os passos de setup são idempotentes e aceitam `--dry-run`, e a checagem doctor continua só de leitura (§5, §6).
- [ ] Os comandos comuns mantêm os mesmos nomes e efeitos em todos os ambientes (§8).
- [ ] Configurações de que outro ambiente precisa foram mantidas, e scripts de shell novos estão com o modo certo no Git (§9).
- [ ] Os arquivos de ferramentas estão em inglês, um idioma por arquivo (§10).
- [ ] O pull request diz quais ambientes foram rodados e quais foram só revisados, com issues de acompanhamento (§12).
- [ ] Os guias e o estado de validação deles batem com a mudança (§11).
- [ ] Nenhuma credencial real nem chave privada foi adicionada (§13).
