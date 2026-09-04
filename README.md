# Agent Skills

A collection of reusable skills for coding agents. Each skill turns a recurring workflow into a scoped, evidence-aware set of instructions, references, and, where useful, validation scripts.

## Available skills

| Skill | Use it for |
| --- | --- |
| [architecture-design](skills/architecture-design/SKILL.md) | Designing and reviewing cross-module changes in an established repository. |
| [repository-structure](skills/repository-structure/SKILL.md) | Auditing and evolving directory, component, ownership, dependency, and local-context boundaries. |
| [greenfield-foundation](skills/greenfield-foundation/SKILL.md) | Defining an initial architecture foundation for a new system before implementation. |
| [git-commit-series](skills/git-commit-series/SKILL.md) | Planning and, after approval, executing a reviewable Git commit series. |
| [implementation-rationale](skills/implementation-rationale/SKILL.md) | Documenting public APIs and preserving implementation rationale in code, tests, and records. |
| [readme-authoring](skills/readme-authoring/SKILL.md) | Auditing, drafting, and revising repository README files from verified project facts. |

The project also uses [writing-for-agents](.agents/skills/writing-for-agents/SKILL.md), sourced from the Git repository [mattpocock/skills](https://github.com/mattpocock/skills) at [`skills/productivity/writing-for-agents/SKILL.md`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents/SKILL.md), to create and maintain documents consumed by agents.

## Installation

Choose one of the following paths.

### 1. Install from a cloned repository

Clone the repository, then point `npx skills` at the local `skills/` directory:

```sh
git clone https://github.com/ken-builds/skills.git
cd skills

npx --yes skills add ./skills \
  --skill readme-authoring \
  --agent codex \
  --yes
```

This path is useful when you want to inspect or modify the skill source locally. Replace `readme-authoring` with another skill name when needed. List the available local skills without installing them:

```sh
npx --yes skills add ./skills --list
```

To restore all project skills recorded in [skills-lock.json](skills-lock.json), run:

```sh
npx --yes skills experimental_install
```

### 2. Install directly from GitHub

Install without cloning the repository:

```sh
npx --yes skills add https://github.com/ken-builds/skills.git \
  --skill readme-authoring \
  --agent codex \
  --yes
```

This path reads the selected branch from the remote repository. The requested skill must be committed and pushed before it can be installed this way; local, unpushed changes are not included.

## Quick start

Install a skill, confirm that it is listed for the project, and invoke it from your agent:

```sh
npx --yes skills add ./skills \
  --skill readme-authoring \
  --agent codex \
  --yes
npx --yes skills list
```

Then ask your agent:

```text
Use $readme-authoring to audit and update README.md.
```

## Repository layout

```text
skills/                         first-party skill definitions
├── architecture-design/
├── git-commit-series/
├── greenfield-foundation/
├── implementation-rationale/
├── repository-structure/
└── readme-authoring/
.agents/skills/                 project-installed copies
skills-lock.json                installation sources and content hashes
```

Each source skill has a required `SKILL.md` and may include `agents/`, `references/`, `scripts/`, and `tests/` when those resources support its workflow.

## Development

Edit source skills under `skills/`. This repository owns source definitions and does not install the skill being developed; a consuming project may refresh its own copy after explicit approval. Review source changes and run the focused checks for the skills you change:

```sh
python3 -m unittest skills/greenfield-foundation/tests/test_validate_foundation.py
python3 -m unittest skills/implementation-rationale/tests/test_validate_implementation_record.py
python3 -m unittest skills/repository-structure/tests/test_inventory_structure.py
python3 -m unittest skills/readme-authoring/tests/test_validate_readme.py
python3 skills/readme-authoring/scripts/validate_readme.py README.md \
  --profile monorepo \
  --strict
```

The README validator checks structure, local links, code fences, placeholders, repository references, and other repository-local invariants; it does not execute README commands or check network reachability.

For a read-only structure inventory, including tracked and non-ignored untracked paths:

```sh
python3 skills/repository-structure/scripts/inventory_structure.py . \
  --tracked \
  --format text
```

## Contributing

When adding or revising a skill:

1. Keep the skill's scope and invocation behavior explicit in `SKILL.md`.
2. Put branch-specific guidance in `references/` and deterministic helpers in `scripts/`.
3. Add focused fixtures or tests when a validator or other executable behavior is introduced.
4. Review the source diff and any explicitly targeted consuming-project copy, then run the relevant checks before committing.

Implementation records can be checked independently with:

```sh
python3 skills/implementation-rationale/scripts/validate_implementation_record.py \
  skills/implementation-rationale/tests/fixtures/valid-record.md \
  --require-complete
```

Replace the fixture path with the Implementation Record or record directory in the target
repository.

Use [writing-for-agents](.agents/skills/writing-for-agents/SKILL.md) when the change alters instructions that another agent will consume.
