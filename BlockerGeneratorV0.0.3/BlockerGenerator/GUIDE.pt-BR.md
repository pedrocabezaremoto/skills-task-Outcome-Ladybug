# Guia rápido — `prompt.md` (Step 1)

Pipeline que gera **blockers lógicos** a partir da tarefa baseline + patches, em até **3 rodadas**. O agente emite **Blocker DSL** (`.bdsl`); o script `build_blockers.py` produz o JSON final.

---

## 1. Pastas e arquivos no container da tarefa

Raiz de trabalho do agente (ex.: `qcfail030601/`). Crie a pasta de inputs:

```text
<task_container>/
  task_info/
    problem-statement.mdc      # enunciado / problema
    requirement.mdc            # requisitos
    public-interface.mdc       # API pública
    blocker-distribution.mdc   # meta de quantos blockers por tipo
    golden_patch.mdc           # patch de referência (privado)
    test_patch.mdc             # patch de testes (privado)
```

**Nomes exatos** (como em `prompt.md`). Extensão `.mdc` é a esperada pelo orquestrador.

**`blocker-distribution.mdc`** — quantidade por tipo, no formato:

```text
mp=1 ar=1 cr=1
```

| Alias | Tipo |
|-------|------|
| `mp` | `missing_parameter` |
| `ar` | `ambiguous_requirement` |
| `cr` | `contradictory_requirement` |

Copie para o container também (ou aponte o agente ao repo):

- `BlockerGenerator/prompt.md`
- `BlockerGenerator/build_blockers.py`
- `BlockerGenerator/skills/` (`project-overview.mdc`, `blocker-generator.mdc`, `blocker-registry.mdc`)

**Saídas** (na raiz do container, `--out-dir .`):

| Arquivo | Função |
|---------|--------|
| `round_<N>.bdsl` | DSL da rodada (escrito pelo agente) |
| `blocker_registry.json` | Gabarito cumulativo dos blockers válidos |
| `generation_memory.json` | Estado do loop + auditoria |
| `existing_registry.json` | Só rodadas > 1 (estado entrante) |
| `rejection_memory.json` | Só rodadas > 1 (rejeições acumuladas) |
| `abort.json` | Se faltar input ou a tarefa for inviável |

---

## 2. Como usar o `prompt.md`

1. Abra `BlockerGenerator/prompt.md` no chat do agente (Cursor / cloud).
2. Garanta que o **cwd** do agente é a raiz do container (`task_info/` visível).
3. Preencha os placeholders no final do prompt (ver seções abaixo).
4. O agente lê as skills, gera o `.bdsl` e roda `build_blockers.py` — **não** edite `blocker_registry.json` à mão.

### Rodada 1 (do zero)

```text
<existing_registry>     [vazio]
<rejection_memory>    [vazio]
<round_number>        1
```

Comando esperado após o DSL:

```bash
python build_blockers.py round_1.bdsl --out-dir .
```

### Vários turnos (rodadas 2 e 3)

Quando `generation_memory.json` tiver `halt.reason` = `continue` e ainda faltar blockers:

1. Copie o conteúdo completo de **`blocker_registry.json`** → `<existing_registry>`.
2. Copie o array **`rejection_memory`** de dentro de **`generation_memory.json`** → `<rejection_memory>`.
3. Defina `<round_number>` como `2` ou `3`.
4. Novo prompt / novo turno com o mesmo `prompt.md` atualizado.

O agente grava `existing_registry.json` e `rejection_memory.json`, emite `round_<N>.bdsl` e executa:

```bash
python build_blockers.py round_<N>.bdsl \
  --existing existing_registry.json \
  --rejection-memory rejection_memory.json \
  --out-dir .
```

**Pare o loop** quando `halt.reason` for:

- `distribution_satisfied` — meta atingida  
- `distribution_already_satisfied` — nada a gerar nesta rodada  
- `budget_exhausted` — 3 rodadas sem fechar a meta  

### Já existe blocker (registry parcial)

Use na **primeira** execução do prompt com registry pré-preenchido:

- Cole o JSON existente em `<existing_registry>` (mesmo formato de `blocker_registry.json`).
- `<rejection_memory>` vazio `[]` ou o histórico que você já tiver.
- `<round_number>` = `1` (ou a rodada lógica seguinte).

O agente calcula o **déficit** por tipo (`pedido − já no registry`) e só gera blockers faltantes. Blockers já no registry são **imutáveis** — não reemitir no DSL.

Se o déficit já for zero em todos os tipos, a rodada emite só `@meta` com `halt: distribution_already_satisfied`.

---

## 3. Memória — o que é

| Conceito | Onde vive | Uso |
|----------|-----------|-----|
| **Registry** (`blocker_registry.json`) | Cumulativo | Gabarito para avaliação e Step 2 (obfuscação). Reentra em `<existing_registry>` na próxima rodada. |
| **Rejection memory** | Array em `generation_memory.json` → `rejection_memory` | Tentativas `@rejected` que falharam validação. O agente deve **evitar repetir** os mesmos padrões (`failure_gate`, `avoid_in_future`, etc.). |
| **`blocker_dataset` (na generation_memory)** | Só da rodada atual | Pool de candidatos, blockers novos com `ground_truth_annotation`, auditoria — **não** reutilizar como registry. |

Regra prática: na rodada seguinte, passe **registry + rejection_memory**; ignore o resto de `generation_memory` para alimentar o prompt.

---

## 4. O que é gerado

**`blocker_registry.json`** — produto principal: lista `blockers[]` com `id`, `type`, `mode`, `area_of_obstruction`, `description`, `resolution`, `trigger_questions`, `independence`. Entradas válidas vêm só de registros `@blocker` com `status: valid | repaired_valid`.

**`generation_memory.json`** — controle e trilha:

- `halt` — motivo de parada, rodada, totais pedidos vs alcançados  
- `blocker_dataset` — candidatos (`candidate_pool`), blockers da rodada com ground truth, rejeitados da rodada, notas  
- `rejection_memory` — rejeições **acumuladas** (todas as rodadas)

O agente escreve **`.bdsl`**; o script monta os JSON de forma determinística (contagens, déficit, checks implícitos).

---

## 5. Como executar

### Pelo agente (fluxo normal)

1. Monte `task_info/` com os 6 arquivos.  
2. Cole `prompt.md` no chat; preencha `<existing_registry>`, `<rejection_memory>`, `<round_number>`.  
3. Deixe o agente rodar até existirem `blocker_registry.json` e `generation_memory.json` sem erro.  
4. Se `halt.reason` = `continue`, repita com rodada +1 e os JSON atualizados (máx. 3 rodadas).

### Script manual (validar / reprocessar DSL)

Na raiz do container, com Python 3:

```bash
# Rodada 1
python build_blockers.py round_1.bdsl --out-dir .

# Rodadas 2+
python build_blockers.py round_2.bdsl \
  --existing existing_registry.json \
  --rejection-memory rejection_memory.json \
  --out-dir .
```

Se o script falhar, corrija o `.bdsl` (gramática em `skills/blocker-generator.mdc`) e rode de novo — não edite o JSON de saída manualmente.

### Caminho absoluto (exemplo Windows)

```bash
cd "c:\Users\leo_m\OneDrive\Documentos\ladybug\qcfail030601"
python "c:\Users\leo_m\OneDrive\Documentos\ladybug\BlockerGenerator\build_blockers.py" round_1.bdsl --out-dir .
```

---

## Fluxo em uma linha

```text
task_info/*  →  prompt.md (≤3×)  →  round_N.bdsl  →  build_blockers.py  →  blocker_registry.json + generation_memory.json
```

Próximo passo do pipeline: Step 2 (obfuscação da tarefa usando `blocker_registry.json`).
