# АМБИВИХРЬ / КВИН-ВОРТЕКС v3.0-experimental

Объединённая экспериментальная версия саморевизующегося agent runtime.

> **Цель:** создавать полезные, правдивые и безопасные системы, которые помогают людям. Это не заявление о наличии сознания или самостоятельной личности.

## Единый цикл

**Задача → Ж → Л → Центр → Reasoning → Верификация → Оккам → Самоподобие → Решение → Policy Gate → Действие → Наблюдение → Реэнтри → Evolution Audit → Lineage**

### Состав

- vortex-development / bottleneck-first optimization / re-entry;
- provider-agnostic LLM interface;
- structured JSON planning;
- conservative verifier;
- Tool Registry + Policy Gate;
- Dry Run и stop conditions;
- audit memory + lineage;
- controlled local replication;
- comfort-expansion policy;
- Occam layer;
- self-similarity analysis;
- self-revision;
- Evolution Gate: ACCEPT / HOLD / REJECT;
- Evolution Audit;
- regression и holdout-oriented evaluation.

## Принцип эволюции

Изменение не принимается только потому, что агент считает его хорошим. Нужны воспроизводимое улучшение, regression, независимая проверка, перенос на независимые задачи и integrity audit.

## Жёсткие границы

- `main` не изменять автоматически;
- Policy Gate не изменять;
- не расширять authority, credentials, tool registry или model endpoint;
- sealed holdout не использовать для оптимизации;
- human approval нельзя обходить;
- собственная оценка не считается независимым доказательством.

## Безопасность

Репликация остаётся локальной и контролируемой. Высокорисковые действия блокируются без явного approval. Самомодификация ограничена экспериментальной веткой и проверяемыми изменениями.

**v3 считается лучше только при измеряемом улучшении без деградации integrity.**

См. `experiments/UNIFIED_V3_2026-09-22.md`.

Лицензия: CC0-1.0.
