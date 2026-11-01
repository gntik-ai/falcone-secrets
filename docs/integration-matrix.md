# Falcone integration matrix

Every row requires tenant/workspace negative tests, value-leak checks and consumer-specific failure/revocation evidence. Source presence is not proof of current deployment. See [sources](sources.md) for pinned versions and [scope](scope-and-baseline.md) for exact public anchors.

| System / consumer | Required behavior | Qualification and ownership |
|---|---|---|
| APISIX and Falcone facade | Existing public routes, verified actor context, stripped untrusted headers, metadata-only schemas | Gateway authentication does not replace per-resource authorization; body logging must be disabled for sensitive requests |
| Control plane and executor | Workspace stores, inventory, role/error ordering, rotation and provider adapters | Test both paths; preserve provider-neutral interfaces rather than proliferating raw Vault calls |
| Current/next consoles and SDKs | Write-only values, masked/cleared input, metadata/inventory and rotation status | No value reveal/readback, URL payload or cached form values; preserve supported response fields and degraded-backend errors |
| `falcone-iam` / current identity adapter | Audience-bound authorization, scoped secret access, signing/federation material and revocation revisions | IAM owns users, custom roles and mandatory SAML/OIDC/LDAP/AD/SCIM support. Secrets supplies custody/key operations; bootstrap trust is independently scoped |
| Current Knative function deployment | Value-free declarations, owned namespaced Secret projection, required secretKeyRefs, stale-revision cleanup | Updating a Secret does not update environment variables in running pods; rollout/validation is required |
| `falcone-serverless` | Scoped material to trusted host bindings/OCI shim and per-attempt authorization | Respect ADR 0006's proposed ESO path and ADR 0010 amendment; no silent change to approved/proposed trust or exposure rules. Guest code gets no host identity |
| Temporal-era workflows | Execution/run-bound reference resolution, short-lived credentials and activity authorization | No resolved secret in history/checkpoints/logs; distinguish sensitive bearer handles from ordinary locators |
| `falcone-workflow` | Authoritative native run lineage, current policy on resume, references and managed credential renewal | Its TypeScript engine/lineage decisions remain intact; secret workers do not depend on workflows for core renewal or recovery |
| LLM and embedding BYOK | Workspace confinement, reserved-prefix env references where approved, fresh resolution and endpoint SSRF rules | Separate static key reads from exchanged OAuth token caches; scope caches to tenant/workspace/connection/config version and invalidate appropriately |
| MCP / external application adapters | Narrow per-tool/provider credentials and IAM audience/scope checks | MCP transports are not a secret authorization model; do not expose broad provider keys through tool results |
| PostgreSQL data APIs / direct DB access | Approved dynamic role templates, RLS-compatible scopes, credential/session expiry policy | Dedicated provider administration role; changing a password need not terminate existing connections |
| FerretDB / DocumentDB | Store and rotate actual backend credentials through its owning adapter | Do not assume generic PostgreSQL credential changes cover all document gateway pool/session behavior |
| SeaweedFS S3 | Preserve per-bucket credentials, rotation/revocation and object-access scope | Qualify release and identity mode; no accumulation of bucket grants or assumed AWS STS/TTL parity |
| Kafka-compatible eventing | Authenticated lifecycle event publishing and scoped broker credentials/ACL adapters | Events contain IDs/revisions only. Existing producer/consumer connections may need independent invalidation |
| Realtime/WebSockets | Scope-aware provider access and credential/policy refresh for long-lived connections | No secret bytes in event envelopes; disconnect/revalidation and downstream credential rotation have separate completion states |
| Webhooks | Retain existing master-key custody and tenant signing-secret encryption lifecycle | Current global webhook key is not simply an OpenBao KV item. Preserve key/database pairing, adoption and finalization procedures |
| Flow-trigger webhook encryption | Preserve separate executor key format/ownership during migration | Do not substitute a generic new root or normalize keys differently without versioned ciphertext migration |
| Platform bootstrap / provisioning | Create/adopt existing Kubernetes Secrets, preserve config.secretRefs and expected key names | Database, gateway TLS and initial identities must work before the secret backend is ready; no plaintext in manifests or release artifacts |
| External Secrets Operator | Preserve installed approved delivery while replacing backend through a qualified provider/subset | Inventory ClusterSecretStore and CRDs; optional existing integration, not a required new operator in the baseline |
| TLS / certificate services | Scoped key/certificate custody, pair validation, expiry visibility and rollout | Existing cert-manager/external CA remains authority unless a separate PKI decision changes it |
| Quota / metering | Apply authoritative Falcone quotas and emit bounded usage events | Keep plan definitions, failed-attempt/retry accounting and execution quotas in Falcone |
| Audit / SIEM / observability | Existing event schemas, correlation, redaction, scoped export and durable acceptance | A healthy log pipeline is not proof of durable audit; sensitive value release needs its own acceptance boundary |
| Backup / disaster recovery | Restore ciphertext with matching keys, policy epochs and lease state | Block ordinary access and provider mutations until stale-state reconciliation completes |

## Reference and event contracts

A canonical internal reference identifies secret object, tenant/workspace, domain, permitted use and version selection (`current` or an approved pinned version). Exact serialized fields are implementation schemas, not a replacement for existing public APIs. A reference alone never grants access. Execution bearer handles, where legacy contracts require them, are treated as credentials with protected storage, expiry and lineage binding.

Lifecycle events carry event ID, schema version, aggregate ID/revision, scope, actor/correlation reference, operation type and status reference. Keep values, wrapped payloads, raw keys, passwords, provider tokens and reusable handles out of the event bus. Preserve existing event names through mappings when consumers depend on them; version new schemas explicitly.

Consumer states distinguish `requested`, `delivered`, `loaded`, `validated`, `failed` and `revoked` as proposed internal vocabulary. Current public schemas remain compatible projections. ACKs bind an authenticated registered principal to exact scope/version. A namespaced Secret update is not a reload acknowledgement, and a workload ACK is not cryptographic evidence that old bytes were erased.

## Cross-repository handoff

The IAM design currently names OpenBao/KMS custody. Workflow names existing Falcone secret services. Serverless contains a proposed OpenBao/ESO delivery ADR with explicit review gates. This repository defines the new adapter target and backlog; actual changes to those repositories and deployment charts require their own reviewed integration changes. Full replacement depends on completing those handoffs, not merely publishing this design.
