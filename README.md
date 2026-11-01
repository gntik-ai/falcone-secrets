# falcone-secrets

Architecture and delivery backlog for **Falcone's custom secret-management service**, intended to replace OpenBao while preserving Falcone interfaces, tenant/workspace isolation and application behavior.

**Status: proposed design and planning artifacts. No secrets runtime has been implemented, deployed or migrated by this repository bootstrap.** The service owns secret custody, resolution, key operations and credential lifecycle; `falcone-iam` owns identity, roles and federation. Falcone remains the product and policy authority.

Research date: 2026-11-01. Source baseline: [`gntik-ai/falcone@ed04fe7`](https://github.com/gntik-ai/falcone/tree/ed04fe7269d32f3f3e3cbc434ab5168389153ed6). Documentation and code establish contract evidence, not blanket production qualification.

## Documentation

| Document | Contents |
|---|---|
| [Scope and current integrations](docs/scope-and-baseline.md) | Observed OpenBao and independent key lifecycles |
| [Reference project survey](docs/open-source-survey.md) | 10 references, feature selection, licensing and trade-offs |
| [Architecture](docs/architecture.md) | Components, stack, ownership, data flow and storage model |
| [Bootstrap and recovery](docs/bootstrap-and-recovery.md) | Root trust, IAM dependency cycle and recovery profiles |
| [Integration matrix](docs/integration-matrix.md) | Falcone APIs, IAM, workflows, serverless, data, eventing and storage |
| [Security](docs/security.md) | Encryption, plaintext boundaries, revocation and qualification |
| [Operations](docs/operations.md) | Proposed objectives, deployment, failure behavior and ownership |
| [Migration](docs/migration.md) | OpenBao cutover, key/lease portability and rollback |
| [Requirements](docs/requirements.md) | 84 testable statements |
| [Epics and stories](docs/backlog.md) | 14 epics and 42 stories with criteria, dependencies and effort |
| [Architecture decision](docs/decisions/0001-baseline.md) | Proposed baseline and alternatives |
| [Open questions](docs/open-questions.md) | Decisions required before implementation and production gates |
| [Sources](docs/sources.md) | Primary references and pinned source evidence |

## Implementation path

1. **P0:** freeze contracts, qualify root custody and bootstrap, choose components and measure demand.
2. **P1:** identity boundary, encrypted versioned KV, write-only APIs, audit/outbox, rotation state and restricted delivery.
3. **P2:** credential adapters, signing/transit, integration qualification, consumer convergence and recovery drills.
4. **P3:** scoped canaries, single-writer handoff, rollback rehearsal and separately approved OpenBao retirement.

The [GitHub issues](https://github.com/gntik-ai/falcone-secrets/issues) are linked by stable SEC IDs, epic task lists, parent references and dependencies. [CSV](docs/backlog.csv), [JSON](docs/backlog.json), [issue payloads](docs/issue-payloads.json) and the [issue map](docs/github-issues.json) support board population. A CSV is portable planning data, not a claim that GitHub Projects provides a universal native CSV importer. This bootstrap does not create a Project board or native sub-issue links.

## Maintaining the plan

Edit `tools/build_docs.py` and run `python3 tools/build_docs.py` to regenerate requirements/backlog artifacts. It validates unique story IDs, references and dependency cycles. Existing issue numbers come from `docs/github-issues.json`; regeneration does not automatically modify GitHub. Maintain architecture documents directly.

The project license remains an owner decision before implementation/code distribution. Reference projects are sources of requirements and patterns; no upstream runtime source is copied in this planning package.
