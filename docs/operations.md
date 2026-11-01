# Operations and service objectives

## Initial targets to qualify

These are engineering hypotheses, not measured performance or a contractual SLA. Assume a single region with available failure domains and suitable PostgreSQL durability; size from actual secret workloads.

| Objective | Proposed target | Measurement boundary |
|---|---|---|
| Core API availability | 99.95% monthly | Supported authorized operations without platform-caused failure, including required IAM, database, audit and key-provider dependencies; expected denies tracked separately |
| Metadata latency | p95 ≤50 ms, p99 ≤150 ms | Service boundary, declared dataset/policy size/concurrency; excludes client internet latency |
| Secret resolution | p95 ≤100 ms, p99 ≤250 ms | Includes authorization, audit acceptance and required key operation in the qualified regional topology; publish cold-provider results separately |
| Purpose-bound signing | Profile-specific, initial p95 ≤100 ms | Measure exact IAM adapter and key-provider topology rather than treating local and network signing as identical |
| New resolve/renew denial after IAM revocation | ≤30 seconds | From IAM authoritative commit; local freshness leases fail closed when disconnected |
| Managed consumer adoption | Initial target ≤60 seconds for qualified online reloadable consumers | From active-version transition to validated adoption; pod restarts and backend sessions need separate measured budgets |
| Dynamic lease revocation | Deadline and retry policy per provider | Report pending/failed external revocation; no universal hard expiry claim for unsupported providers |
| Acknowledged mutation durability | No loss under tested process/replica failure | Requires the declared durable database topology; not a zero-loss regional disaster claim |
| Disaster recovery | RPO ≤5 min, RTO ≤60 min | Full ciphertext/key/policy/lease restoration and reconciliation drill; root-custody access is part of the objective |

Define burn-rate alerts and owner-approved failure thresholds before offering these objectives publicly. Availability and security freshness sometimes conflict; after a policy lease expires, do not continue granting access to hide an IAM outage.

## Capacity and dependencies

Measure secrets/versions per tenant, object size, resolve QPS, crypto operations, policy cache hits, signing demand, concurrent leases, rotation fan-out, audit writes, retention and cold-start bursts. Prior estimates of ~20 tenants, 10,000 deployed functions and 100k event messages/second are useful context but do not specify these dimensions. One function may resolve once per deployment or repeatedly per invocation; design and benchmark both allowed paths.

Per-read durable audit and KMS latency are real costs. Batch only when policy/semantics permit. Separate API and worker pools to prevent rotation backlog starving resolution. Avoid a distributed cache dependency until measured demand justifies its additional freshness/custody risk. No in-memory cache is authoritative for lease or revocation state.

Retain existing PostgreSQL, Kafka-compatible eventing, APISIX, Falcone IAM, observability and SeaweedFS interfaces. Root custody needs an available approved KMS/HSM or operator-unlock procedure; do not assume a specific cloud. Mail, PKI and optional external providers remain separately owned capabilities.

## Restricted Kubernetes/OpenShift

Use ordinary namespaced Deployments/Services/Jobs, approved ingress/Route, configuration references and narrowly scoped service accounts. Support arbitrary non-root UID, dropped capabilities, no privilege escalation, read-only root filesystem and bounded writable temporary space. No required operator, CRDs, host mounts, privileged containers, sandbox runtime or cluster-admin. Do not require `mlock` privileges as an unexamined prerequisite.

Normal API service should not need Kubernetes API access. A separately scoped projector may write only approved namespaced Secrets. Existing ESO can remain where already installed and authorized; its ClusterSecretStore and provider credentials must be inventoried. It cannot be assumed available in every corporate namespace.

Qualify the exact installed OpenShift product/build and approved Kubernetes minors. The earlier Kubernetes 1.33.12 reference does not identify an OpenShift support matrix by itself. Pin tested SeaweedFS, PostgreSQL, IAM and provider versions at release time. Air-gapped delivery needs immutable images, trust bundles and an approved update process.

## Failure behavior

| Failure | Required response |
|---|---|
| Root provider unavailable / sealed service | Deny operations requiring unavailable keys; expose sanitized degraded status; no automatic root replacement |
| IAM unavailable | Existing explicit freshness leases last only to their bound; normal new grants then deny. Narrow bootstrap IAM signing uses its independent approved trust path |
| PostgreSQL unavailable | Deny mutations, new leases and value release requiring durable audit/state; no broad plaintext-cache fallback |
| Kafka unavailable | Durable local outbox buffers within limits; workers reconcile; alert on backlog before security/capacity budgets are exhausted |
| External credential provider unavailable | Persist retry/uncertain outcome, bound retries, mark revocation pending and alert; do not call it completed |
| Consumer offline | Track outstanding adoption; planned rotation follows reviewed deadline/exception policy, emergency revoke may sacrifice availability |
| Worker/replica crash | Transactional intent, idempotency and fencing avoid stale completion or duplicated untracked effects |
| Database restore | Start isolated/sealed as needed; reconcile keys, IAM epochs, tombstones and backend leases before traffic |

## Ownership

| Responsibility | Typical accountable team | Required deliverable |
|---|---|---|
| Product contract and scope | Falcone product owner / architect | Approved API parity, feature boundaries and consumer migration gates |
| Runtime and adapters | Secrets/platform backend maintainers | Correctness, dependency/crypto patches, schema and provider compatibility |
| Identity and policy | IAM maintainers | Decision contract, workload identity, federation-driven revocation and bootstrap signing integration |
| On-call reliability | SRE / platform operations | Alerts, incident rotation, error budgets, capacity, restore and upgrade runbooks |
| Root keys and recovery | Security/infrastructure custodians | Key policy, independent custody, authorized recovery and retirement controls |
| Consumer adoption | Data, storage, workflow, serverless and app owners | Reload/revocation evidence, rollback and provider-specific behavior |
| Security qualification | AppSec / cryptography specialists / independent reviewer | Threat review, protocol/key-custody assessment and owned residual findings |
| Privacy and retention | Governance/data-protection owner | Audit/backup retention, scoped export and deletion policy |

Runtime ownership includes lifecycle correctness and external side effects, not only maintaining a container. On-call ownership includes restoring data with the right keys. Security qualification is independent evidence before replacing a trust service. Small teams may combine roles, but recovery cannot depend on one unavailable person. Actual names and schedules remain open.
