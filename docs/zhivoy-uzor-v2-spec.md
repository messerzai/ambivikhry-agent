# «Живой узор» 2.0 — продуктовая спецификация MVP

Статус: проектная спецификация для обсуждения и реализации. Это не утверждение, что UI или backend уже существуют.

## 1. Продуктовая цель

Помочь человеку перевести собственное желание в проверяемый результат, проект и ближайшее действие, сохранив авторство пользователя. AI предлагает варианты; пользователь решает, что считать верным.

Основной цикл: желание → уточнение → карта целей/ограничений → проект → действие → обратная связь → обновление.

## 2. Пользовательский сценарий (вертикальный срез)

1. Пользователь создаёт карточку и сохраняет исходную формулировку без перефразирования.
2. Система задаёт до 5 уточняющих вопросов: желаемый результат, личная значимость, срок, ресурсы/ограничения, признак успеха.
3. AI формирует черновик карточки и маркирует каждый вывод как user_stated, observation или hypothesis.
4. Пользователь может изменить, подтвердить или отклонить каждый блок.
5. Пользователь нажимает «Создать проект»; поля карточки переносятся в проект как редактируемые данные.
6. Проект предлагает 1–3 ближайших действия с владельцем, сроком, зависимостями и критерием завершения.
7. Пользователь отмечает результат и даёт обратную связь; история сохраняет изменение состояния.

## 3. Модель данных (предлагаемый минимум)

### DesireCard
- id, owner_id, title, original_text
- why_it_matters
- desired_outcome
- success_criteria[]
- target_date (nullable)
- resources[], constraints[]
- open_questions[]
- conflict_hypotheses[] — каждая с альтернативным объяснением и вопросом проверки
- status: draft | active | achieved | paused | archived
- created_at, updated_at, version

### AIProposal
- id, card_id, field, suggested_value
- evidence_kind: user_stated | observation | hypothesis
- rationale, confidence (0..1), status: draft | user_confirmed | rejected
- created_at, reviewed_at

### Project
- id, owner_id, source_desire_card_id (nullable)
- name, description, status: idea | active | blocked | completed | archived
- goal_ids[], participant_ids[], created_at, updated_at, version

### ProjectItem
- id, project_id, kind: idea | decision | task | resource | link | note
- title, body, status, owner_id (nullable), due_at (nullable)
- acceptance_criteria, created_at, updated_at

### Relation
- id, owner_id, from_type, from_id, relation_type, to_type, to_id
- Validate that both endpoints are accessible to the owner; prevent dangling links.

### AuditEvent
- id, owner_id, actor, entity_type, entity_id, action, timestamp, change_summary
- Never put secrets or unnecessary sensitive text in audit summaries.

## 4. Conflict exploration — not diagnosis

The system may identify candidate tensions, for example:
- stated outcome vs. time available;
- priority vs. current commitments;
- desired collaboration vs. absence of a concrete request;
- multiple goals competing for the same resources.

For every candidate, show:
1. what user-provided facts triggered the question;
2. at least one plausible alternative explanation;
3. a neutral question the user can answer;
4. buttons to accept as useful, edit, dismiss, or mark unknown.

Do not infer mental disorders, hidden motives, or stable personality traits from a card. Do not label an inconsistency as a fact until the user confirms it.

## 5. Social graph and collaboration

Node types: person, team, project, goal, action, resource.
Relationship examples: can_help_with, collaborates_on, needs_resource, depends_on, supports_goal.

- Add people only when the user enters them or explicitly imports them.
- Record the proposed contribution and what the user is willing to offer in return.
- No automated messages, invitations, or disclosure of a desire to another person without explicit user action.
- Sharing defaults to private. Invitees receive only the selected project and fields.

## 6. «Грань самости» — visual layer

Input: themes and imagery the user voluntarily selects, plus confirmed card content only.
Output: editable visual metaphor / abstract pattern, not a psychological measurement.

Controls:
- regenerate;
- edit or remove motifs;
- toggle which confirmed themes are included;
- export image;
- delete generated artifact and its source selection.

The text card and graph remain the source of truth. Never require interpretation of an image to use core functionality. Provide text labels and accessible navigation.

## 7. Project workspace

MVP page areas:
- Overview: objective, current status, next action.
- Ideas: capture and link an idea to a goal or task.
- Tasks: owner, status, due date, acceptance criterion.
- Decisions: decision, rationale, date, affected items.
- People: collaborators and permissions.
- History: chronological changes and completed outcomes.

Required interactions: create/edit/archive project; add/edit/complete task; add idea; record decision; link desire card; search/filter; export JSON; delete project and its associated data subject to explicit confirmation.

## 8. API proposal (adapt to existing stack after repository inspection)

- POST /desire-cards
- GET /desire-cards/{id}
- PATCH /desire-cards/{id}
- POST /desire-cards/{id}/proposals
- POST /proposals/{id}/confirm
- POST /proposals/{id}/reject
- POST /desire-cards/{id}/projects
- GET /projects/{id}
- PATCH /projects/{id}
- POST /projects/{id}/items
- PATCH /project-items/{id}
- POST /relations
- GET /projects/{id}/history
- GET /export
- DELETE /projects/{id}

These are conceptual routes, not a claim that an HTTP server exists. Reuse current infrastructure rather than introducing a new framework before discovery.

## 9. Privacy and permissions

- Every query and mutation is scoped to authenticated owner_id.
- Default-private data; least-privilege sharing.
- Validate input and relationship endpoints server-side.
- Log structural events, not secrets.
- User can export and delete their data.
- AI proposals never silently overwrite confirmed user fields.
- External side effects require explicit user action and pass the existing Policy Gate.

## 10. Acceptance tests

1. Original desire text remains available after AI refinement.
2. Every AI-proposed field is editable and has an evidence kind/status.
3. Rejected proposals do not reappear as confirmed values.
4. A desire card can create a project with traceable provenance.
5. A project supports ideas, decisions, tasks and a first action.
6. User A cannot read or mutate User B's card, project, graph links or export.
7. Invalid/dangling graph edges are rejected.
8. Private projects are not visible to invitees until explicitly shared.
9. No social contact is messaged automatically.
10. Visual motif deletion does not delete the underlying desire card; deleting source selections removes them from future generations.
11. Export is readable and includes linked items.
12. Delete operations require confirmation and leave only the minimum legally/operationally necessary audit record.

## 11. Сателлиты: исследование внешних решений (2026-10-22)

Это сравнительный обзор публичных страниц и описаний проектов, а не полный аудит кода, безопасности, эффективности или лицензий. Сателлиты — источники проверяемых инженерных идей, а не зависимости, которые нужно бездумно копировать.

### A. Yggdrasil — семантический дневник и «живая карта мышления»
Источник: https://github.com/astrayama/yggdrasil
- Описывает извлечение тем, эмоций, сущностей и паттернов из записей, затем граф и семантические кластеры.
- Заимствовать как принцип: показывать человеку повторяющиеся темы на протяжении времени, а не только пересказывать последнюю запись.
- Адаптация: каждая грань/паттерн должна ссылаться на конкретные добровольно сохранённые записи и показывать период наблюдения; пользователь подтверждает или отклоняет её.
- Не заимствовать автоматически эмоциональные ярлыки как объективную истину.

### B. Personal Brain — local-first граф, затухание памяти, интерактивная визуализация
Источник: https://github.com/alvinekelund/personal-brain
- README описывает локальное хранение, типизированные узлы/рёбра, семантический поиск, визуальный граф, источники и ослабление неиспользуемых узлов.
- Заимствовать как принцип: раздельно хранить исходные заметки и производный граф; граф можно перестроить из источников.
- Адаптация: карточка/заметка — первичный источник; связи и «грани» являются производными с происхождением, датой и возможностью пересборки.
- Не удалять личные данные только из-за низкой частоты обращения. В «Живом узоре» затухание может менять приоритет показа, но не уничтожать исходную информацию.

### C. Synapse — рефлексия с памятью и вопросами к накопленному графу
Источник: https://github.com/jawciu/synapse
- Описывает поток рефлексии, извлечение тем/паттернов, хранение графа и вопросы к истории.
- Заимствовать как сценарий: «Что повторяется?», «Что изменилось?», «Какие примеры подтверждают это?» — с ответами, привязанными к источникам.
- Адаптация: добавить к карточке раздел «Наблюдения во времени» и вопросы к собственной истории, но не превращать категории терапевтических моделей в диагнозы.

### D. Atomic — открытый knowledge graph и пространственная карта идей
Источник: https://atomicapp.ai/
- Публичная страница описывает semantic search, синтез заметок с цитатами, агентный чат и пространственный граф.
- Заимствовать как принцип UX: пользователь может переходить от общего рисунка к конкретной заметке и видеть, почему элементы связаны.
- Адаптация: к каждому ребру показывать тип связи и основания; поддерживать поиск и локальное раскрытие подграфа, а не перегружать экран всеми узлами.

### E. Graphlink — ветвящиеся разговоры, рабочий холст и отменяемые действия
Источник: https://github.com/dovvnloading/Graphlink
- Описывает canvas с узлами разных типов, исследовательскими ветками, выполнением многошаговых задач и undo.
- Заимствовать как принцип: идеи могут развиваться в отдельные ветки, не теряя исходный контекст; действия агента должны быть обозримыми и отменяемыми.
- Адаптация: в рабочем пространстве проекта дать ветки «идея → проверка → решение → задача» и журнал изменений; агентные изменения — через preview/confirm/undo, где технически возможно.

### F. Heartwood — гипотезы, противоречия и ревизия убеждений
Источник: https://github.com/rodspeed/heartwood
- Описывает поиск скрытых связей, противоречий, недостающих связей и пересмотр утверждений с отслеживанием источников и уверенности.
- Заимствовать как принцип: конфликт между целями — кандидат на исследование, а не окончательный вывод о человеке.
- Адаптация: хранить альтернативные объяснения, происхождение свидетельств, уверенность и решение пользователя; не давать модели самой превращать гипотезу в подтверждённый факт.

### G. Jarvis — обратная запись в память и прозрачные связи
Источник: https://github.com/Szesnasty/Jarvis
- Описывает граф заметок, гибридный поиск, запись итогов разговоров обратно в пользовательскую память и визуальный просмотр связей.
- Заимствовать как принцип: после диалога предлагать компактные изменения карточки/проекта, но не менять подтверждённые данные без согласия.
- Адаптация: очередь «Предлагаемые обновления» с diff, источником, подтверждением и отклонением.

### H. Bezial — временная достоверность, проверяемость и выборочное забывание
Источник: https://bezial.com/
- Описывает инспектируемый временной граф, редактируемые исходники, архивирование устаревшего и разрешённые пространства команды.
- Заимствовать как принцип: различать «было верно тогда» и «верно сейчас»; пользователь может просмотреть, исправить и восстановить архивную информацию.
- Адаптация: у фактов и отношений предусмотреть valid_from/valid_until или equivalent temporal metadata, если это поддерживается текущей моделью; не усложнять MVP до появления реального требования.

### I. Evidence of Life — план и факт в одной временной линии
Источник: https://github.com/Cyriellewu/evidenceoflife-v2
- Описывает планирование, фактическое выполнение, историю и контекст событий.
- Заимствовать как принцип: проект должен помогать сравнивать ожидаемый следующий шаг с реальным результатом без стыда и морализаторства.
- Адаптация: простая отметка «планировал / сделал / изменилось / почему (необязательно)» и недельный обзор, который предлагает корректировку плана, а не оценку личности.

## 12. Сводные решения для «Живого узора»

Приоритетные идеи, которые входят в продуктовую спецификацию:
1. **Происхождение каждого вывода**: источник, дата, тип свидетельства, уверенность, состояние подтверждения.
2. **Граф с объяснимыми связями**: клик по узлу показывает исходный материал; клик по ребру объясняет, почему связь предложена.
3. **Память, которую можно исправить**: версии, временная актуальность, архивирование вместо скрытого удаления, явный экспорт/удаление.
4. **Очередь изменений от ИИ**: diff → подтверждение/отклонение → журнал; никакой тихой перезаписи подтверждённых данных.
5. **Разветвление идей и отменяемость**: проектный холст с узлами идеи, гипотезы, решения и действия; destructive actions требуют подтверждения.
6. **План против факта без наказания**: фиксировать результаты и менять план на основании опыта.
7. **Грань самости как визуальная гипотеза**: строить её только из выбранных/подтверждённых тем, с обратными ссылками к источникам и возможностью убрать любой мотив.
8. **Режим локальности/приватности как архитектурное решение**: перед выбором стека сравнить self-host/local-first с существующей инфраструктурой; не вводить новый storage или графовую БД без доказанной необходимости.

## 13. Что НЕ делать после исследования

- Не импортировать чужой код или зависимости, пока не проверены лицензия, активность, security posture и соответствие существующему стеку.
- Не объявлять проект клиническим, диагностическим или «читающим истинную личность».
- Не добавлять автоматический сбор чувствительных данных, контактов, биометрии или сообщений.
- Не считать число звёзд GitHub доказательством качества.
- Не переносить описанные функции в статус «реализовано» без работающего кода и тестов.

## 14. Delivery sequence

- M0 — Discovery: inspect existing app stack, models, auth, persistence, AI pipeline and current desire-card UI. Map this spec to existing code.
- M1 — Data model: schema/migrations, ownership checks, audit events.
- M2 — Vertical slice: create card → confirm/edit → create project → add first task → record outcome.
- M3 — Graph: relations, people/resources, conflict candidates.
- M4 — Visual layer: editable image generation from explicitly selected/confirmed motifs.
- M5 — Hardening: access-control tests, export/delete, accessibility, regression suite.

Do not begin M3/M4 until M2 is usable and tested. Do not merge to main without review and passing tests.
