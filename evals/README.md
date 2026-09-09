# Skill behavior evaluations

Use this suite when a trigger, step, completion criterion, or reference changes. Unit tests
check helpers and packaging; they do not establish model behavior. This directory is an
evaluation resource, not an installed skill or additional always-loaded instruction.

## Protocol

1. Select a baseline and candidate skill revision. Record model/version, reasoning settings,
   tools, permissions, time/token budget, and case selection before running either condition.
2. Use a fresh isolated directory and fresh model context per case, condition, and repetition.
   Install only that condition's skill copies. Keep source projects and credentials outside it.
   If using a live project such as Cairn, clone it separately with `--no-hardlinks`, pin a commit,
   and record excluded uncommitted work. Never run experiments in its active checkout.
3. Present only `prompt.md` and the `input/` tree of a case. Keep `rubric.md`, this protocol,
   and previous answers out of the tested agent's context. Use the same initial prompt for
   both conditions, without adding skill names except in an explicitly labeled invocation test.
4. Record which skills/references were actually read and the resulting actions, diff, tests,
   questions, elapsed time, and available token counts. Deliver `follow-up.md`, where present,
   in the same case session only after the first response. Preserve first-stage output.
5. Score against observable rubric items, citing transcript events or file/test evidence.
   Separate autonomous discovery from user-supplied corrections. Blind the scorer to condition
   where feasible. A missing model/tool prerequisite is `not-run`, never a zero or passing score.
6. For comparative claims, run at least three repetitions per condition, counterbalance run
   order, and report per-case results and variance alongside correctness and interaction cost.
   A smoke run is useful for debugging the case, not evidence of general improvement.

## Cases and generalization

| Case | Main branch | Fixture |
| --- | --- | --- |
| missing-premise | implicit architecture discovery; retry ambiguity | Python job delivery |
| abstraction-owner | contract versus concrete implementation | Go report storage |
| homogeneous-peers | retain a large coherent flat group | locale catalog |
| second-increment | revisit after a requirement changes ownership | plugin host lifecycle |
| skipped-target | distinguish gate success from coverage | Python record selector |
| local-edit | avoid unnecessary workflow and records | Python string formatting |
| recovery-category | scope recovery and retain safe error classes | Python batch importer |
| first-slice | greenfield assumptions and reversible scope | document review service |

These are development/regression cases informed by observed failure mechanisms. Keep additional
unseen cases in a separate evaluator-owned location, with different domains/languages, before
claiming generalization. A new case should test a decision, not the presence of a directory name,
a particular interface count, a keyword, or a preferred prose template.

## Result record

Use one row per case, condition, and repetition:

| Case | Condition/revision | Run | Model/settings | Trigger/reference evidence | Rubric outcomes | Corrections/questions | Time/tokens | Artifact | State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Each rubric item is `pass`, `fail`, or `not-run` with evidence. Report unnecessary abstractions,
documents, permission requests, and missed follow-up obligations separately from functional
correctness. Do not collapse all dimensions into a single architecture score.

Repository unit checks validate case packaging and deterministic fixtures only. No model
comparison result is implied by their success.
