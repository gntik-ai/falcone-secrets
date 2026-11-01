# Functional requirements

Planning baseline: 2026-11-01. Requirements describe target behavior, not delivered functionality. Each requirement traces to one story. Read with [architecture](architecture.md), [security](security.md), [bootstrap](bootstrap-and-recovery.md) and [integration matrix](integration-matrix.md).

## Falcone contracts and replacement scope

| ID | Requirement | Story |
|---|---|---|
| FR-CON-001-1 | The project must inventory every OpenBao client, mount, auth path, secret reference, rotation consumer and non-OpenBao key lifecycle against a pinned Falcone commit. | [SEC-CON-001](https://github.com/gntik-ai/falcone-secrets/issues/15) |
| FR-CON-001-2 | The system must preserve approved Falcone API routes, metadata fields, status codes and error precedence through contract tests. | [SEC-CON-001](https://github.com/gntik-ai/falcone-secrets/issues/15) |
| FR-CON-002-1 | The system must define a single authoritative writer for secret versions, rotation state, leases, policies and backend credentials throughout migration. | [SEC-CON-002](https://github.com/gntik-ai/falcone-secrets/issues/16) |
| FR-CON-002-2 | Falcone IAM must remain the owner of users, roles and federation, while Falcone quota services remain the owner of entitlements and accounting. | [SEC-CON-002](https://github.com/gntik-ai/falcone-secrets/issues/16) |
| FR-CON-003-1 | The implementation must use maintained cryptographic, TLS and identity libraries with pinned versions and an upgrade owner. | [SEC-CON-003](https://github.com/gntik-ai/falcone-secrets/issues/17) |
| FR-CON-003-2 | Dependency intake must distinguish open-source references from source-available and enterprise-only code and record provenance before copying or embedding code. | [SEC-CON-003](https://github.com/gntik-ai/falcone-secrets/issues/17) |

## Identity, policy and tenant isolation

| ID | Requirement | Story |
|---|---|---|
| FR-AUTH-001-1 | Every online secret operation must authenticate its caller and authorize action, resource, tenant/workspace, audience and delegated authority. | [SEC-AUTH-001](https://github.com/gntik-ai/falcone-secrets/issues/18) |
| FR-AUTH-001-2 | Metadata listing, value resolution, key use, key administration, rotation and destruction must be distinct permissions with deny-by-default behavior. | [SEC-AUTH-001](https://github.com/gntik-ai/falcone-secrets/issues/18) |
| FR-AUTH-002-1 | Secret IDs and references must bind domain, tenant, workspace/environment, secret identity and permitted version selection without accepting arbitrary backend paths. | [SEC-AUTH-002](https://github.com/gntik-ai/falcone-secrets/issues/19) |
| FR-AUTH-002-2 | All list, count, search and lookup operations must filter by authorized scope before pagination and avoid cross-tenant existence disclosure. | [SEC-AUTH-002](https://github.com/gntik-ai/falcone-secrets/issues/19) |
| FR-AUTH-003-1 | Workload authentication must bind the verified service or execution identity to tenant/workspace, attempt, resource, audience and expiry. | [SEC-AUTH-003](https://github.com/gntik-ai/falcone-secrets/issues/20) |
| FR-AUTH-003-2 | Resolution and lease renewal must deny when required authorization freshness cannot be established within the approved bound. | [SEC-AUTH-003](https://github.com/gntik-ai/falcone-secrets/issues/20) |

## Versioned secret storage and lifecycle

| ID | Requirement | Story |
|---|---|---|
| FR-KV-001-1 | Workspace create, replace, metadata read, list and delete must preserve Falcone write-only value semantics and the approved response schemas. | [SEC-KV-001](https://github.com/gntik-ai/falcone-secrets/issues/21) |
| FR-KV-001-2 | Create must be atomic and create-only, replacement must not leak prior values, and public delete must remove all versions from live resolution as contracted. | [SEC-KV-001](https://github.com/gntik-ai/falcone-secrets/issues/21) |
| FR-KV-002-1 | The store must assign immutable version IDs and use atomic revision checks for create/replace, active-version selection and metadata changes. | [SEC-KV-002](https://github.com/gntik-ai/falcone-secrets/issues/22) |
| FR-KV-002-2 | Internal soft deletion, recovery and irreversible destruction must be distinct operations with explicit retention and authorization rules. | [SEC-KV-002](https://github.com/gntik-ai/falcone-secrets/issues/22) |
| FR-KV-003-1 | Inventory and metadata endpoints must preserve approved domains and legacy compatibility fields without returning values or ciphertext. | [SEC-KV-003](https://github.com/gntik-ai/falcone-secrets/issues/23) |
| FR-KV-003-2 | Tenant/workspace purge must tombstone identity and references, block new resolution and expose retryable consumer cleanup progress. | [SEC-KV-003](https://github.com/gntik-ai/falcone-secrets/issues/23) |

## Encryption, key custody and rewrapping

| ID | Requirement | Story |
|---|---|---|
| FR-KEY-001-1 | Secret values must use reviewed authenticated encryption with fresh per-version data keys and authenticated tenant/resource/version context. | [SEC-KEY-001](https://github.com/gntik-ai/falcone-secrets/issues/24) |
| FR-KEY-001-2 | Root key-encryption authority must be outside the ciphertext database, with a documented KMS/HSM or approved operator-unlock custody profile. | [SEC-KEY-001](https://github.com/gntik-ai/falcone-secrets/issues/24) |
| FR-KEY-002-1 | Key rotation must distinguish root/KEK rewrapping, data-key re-encryption and external credential replacement, with separate state and permissions. | [SEC-KEY-002](https://github.com/gntik-ai/falcone-secrets/issues/25) |
| FR-KEY-002-2 | Old keys must not be destroyed until retained ciphertext, backups and restore requirements have been reconciled under an approved retirement policy. | [SEC-KEY-002](https://github.com/gntik-ai/falcone-secrets/issues/25) |
| FR-KEY-003-1 | All value-bearing service traffic must use authenticated TLS and explicit size/time limits, with debugging and request-body capture disabled in production. | [SEC-KEY-003](https://github.com/gntik-ai/falcone-secrets/issues/26) |
| FR-KEY-003-2 | Key-provider interfaces must distinguish non-exportable operations from exported software keys and fail safely on unsupported algorithms or custody mode. | [SEC-KEY-003](https://github.com/gntik-ai/falcone-secrets/issues/26) |

## Bootstrap, sealing and recovery trust

| ID | Requirement | Story |
|---|---|---|
| FR-BOOT-001-1 | The deployment must define independent custody for root wrapping authority, startup database access and recovery authorization before production initialization. | [SEC-BOOT-001](https://github.com/gntik-ai/falcone-secrets/issues/27) |
| FR-BOOT-001-2 | Bootstrap must not require a credential retrievable only from the uninitialized secrets service or a token signed only by an unavailable IAM dependency. | [SEC-BOOT-001](https://github.com/gntik-ai/falcone-secrets/issues/27) |
| FR-BOOT-002-1 | A pre-enrolled IAM workload identity must be able to perform only approved signing-key operations needed to start IAM, independently of IAM-issued end-user tokens. | [SEC-BOOT-002](https://github.com/gntik-ai/falcone-secrets/issues/28) |
| FR-BOOT-002-2 | Sealed or unavailable key state must deny value/sign operations and expose sanitized readiness/status without restarting endlessly through liveness failure. | [SEC-BOOT-002](https://github.com/gntik-ai/falcone-secrets/issues/28) |
| FR-BOOT-003-1 | Recovery access must be strongly authenticated, time-bounded, narrowly scoped and auditable independently of ordinary tenant credentials. | [SEC-BOOT-003](https://github.com/gntik-ai/falcone-secrets/issues/29) |
| FR-BOOT-003-2 | Recovery material and its backups must be held separately from encrypted application data and tested under the approved custody policy. | [SEC-BOOT-003](https://github.com/gntik-ai/falcone-secrets/issues/29) |

## Dynamic credentials and leases

| ID | Requirement | Story |
|---|---|---|
| FR-DYN-001-1 | Dynamic credential issuance must persist a tenant/workload-bound lease with backend identity, maximum TTL, renewal conditions and revocation status. | [SEC-DYN-001](https://github.com/gntik-ai/falcone-secrets/issues/30) |
| FR-DYN-001-2 | Lease renewal must require current authorization and cannot extend past parent grant, job deadline or configured maximum lifetime. | [SEC-DYN-001](https://github.com/gntik-ai/falcone-secrets/issues/30) |
| FR-DYN-002-1 | The PostgreSQL adapter must create and revoke credentials through approved role templates with tenant/workspace and RLS-compatible privileges. | [SEC-DYN-002](https://github.com/gntik-ai/falcone-secrets/issues/31) |
| FR-DYN-002-2 | Provider administration credentials must be separated from issued workload credentials and limited to approved lifecycle operations. | [SEC-DYN-002](https://github.com/gntik-ai/falcone-secrets/issues/31) |
| FR-DYN-003-1 | Every provider adapter must declare issuance, renewal, overlap, expiry and revocation capabilities and reject unsupported guarantees. | [SEC-DYN-003](https://github.com/gntik-ai/falcone-secrets/issues/32) |
| FR-DYN-003-2 | SeaweedFS, Kafka-compatible eventing and external-provider credential integrations must preserve Falcone resource-scoping rules. | [SEC-DYN-003](https://github.com/gntik-ai/falcone-secrets/issues/32) |

## Rotation and consumer convergence

| ID | Requirement | Story |
|---|---|---|
| FR-ROT-001-1 | Rotation must use a persisted state machine for prepare, provider activation, consumer delivery, acknowledgement and old-credential revocation. | [SEC-ROT-001](https://github.com/gntik-ai/falcone-secrets/issues/33) |
| FR-ROT-001-2 | Local secret/version changes and propagation intent must commit atomically while external provider effects use fenced, retryable reconciliation. | [SEC-ROT-001](https://github.com/gntik-ai/falcone-secrets/issues/33) |
| FR-ROT-002-1 | Only the registered authenticated consumer for the correct tenant/resource/version may acknowledge receipt or successful reload. | [SEC-ROT-002](https://github.com/gntik-ai/falcone-secrets/issues/34) |
| FR-ROT-002-2 | Rotation status must distinguish persisted, delivered, loaded, validated and revoked outcomes with consumer deadlines and retryable failures. | [SEC-ROT-002](https://github.com/gntik-ai/falcone-secrets/issues/34) |
| FR-ROT-003-1 | Grace expiry and revocation jobs must persist deadlines and survive restarts, duplicate delivery and clock-skew limits. | [SEC-ROT-003](https://github.com/gntik-ai/falcone-secrets/issues/35) |
| FR-ROT-003-2 | Old credential revocation must be verified per backend and unresolved operations must remain visible for operator action. | [SEC-ROT-003](https://github.com/gntik-ai/falcone-secrets/issues/35) |

## Secret delivery and workload confinement

| ID | Requirement | Story |
|---|---|---|
| FR-DEL-001-1 | The baseline delivery path must use approved SDK/host-side resolution or a namespace-scoped projector without requiring new CRDs or cluster-wide privileges. | [SEC-DEL-001](https://github.com/gntik-ai/falcone-secrets/issues/36) |
| FR-DEL-001-2 | Existing ESO consumers must have a tested explicit provider adapter or limited compatibility surface before their OpenBao backing store is removed. | [SEC-DEL-001](https://github.com/gntik-ai/falcone-secrets/issues/36) |
| FR-DEL-002-1 | Current function deployment must preserve named secret declarations and owned secretKeyRef projection without embedding values in pod specs or saved revisions. | [SEC-DEL-002](https://github.com/gntik-ai/falcone-secrets/issues/37) |
| FR-DEL-002-2 | Native serverless secret resolution must follow approved host/shim and per-attempt identity contracts without exposing host credentials to guest code. | [SEC-DEL-002](https://github.com/gntik-ai/falcone-secrets/issues/37) |
| FR-DEL-003-1 | Temporal-era and native workflow adapters must resolve secret references only for the verified tenant/workspace and authoritative execution lineage. | [SEC-DEL-003](https://github.com/gntik-ai/falcone-secrets/issues/38) |
| FR-DEL-003-2 | Workflow histories, checkpoints, retries and task payloads must not contain resolved secret values or reusable bearer credentials. | [SEC-DEL-003](https://github.com/gntik-ai/falcone-secrets/issues/38) |

## Falcone product and infrastructure integrations

| ID | Requirement | Story |
|---|---|---|
| FR-INT-001-1 | APISIX, both control-plane paths, consoles and supported SDKs must preserve approved Falcone secret metadata and lifecycle contracts. | [SEC-INT-001](https://github.com/gntik-ai/falcone-secrets/issues/39) |
| FR-INT-001-2 | Provisioning and quota integrations must use Falcone ownership and accounting decisions without duplicating user or billing databases. | [SEC-INT-001](https://github.com/gntik-ai/falcone-secrets/issues/39) |
| FR-INT-002-1 | LLM/embedding secret resolution must preserve workspaceSecret and approved reserved-env reference rules and endpoint confinement. | [SEC-INT-002](https://github.com/gntik-ai/falcone-secrets/issues/40) |
| FR-INT-002-2 | Provider token caches must be scoped to connection identity/version and be invalidated on credential rotation, permission loss or endpoint changes. | [SEC-INT-002](https://github.com/gntik-ai/falcone-secrets/issues/40) |
| FR-INT-003-1 | Platform webhook master keys, flow-trigger keys, IAM signing/federation secrets and platform database credentials must retain their distinct lifecycle and recovery contracts. | [SEC-INT-003](https://github.com/gntik-ai/falcone-secrets/issues/41) |
| FR-INT-003-2 | Migration of a non-OpenBao key custodian must require a versioned adapter and paired ciphertext/key recovery evidence before changing its source. | [SEC-INT-003](https://github.com/gntik-ai/falcone-secrets/issues/41) |

## Cryptographic operations and certificate custody

| ID | Requirement | Story |
|---|---|---|
| FR-SIG-001-1 | Signing APIs must bind key purpose, caller, allowed algorithms and message context, with separate permissions for use and administration. | [SEC-SIG-001](https://github.com/gntik-ai/falcone-secrets/issues/42) |
| FR-SIG-001-2 | IAM integration must publish compatible public key metadata and support tested signing-key rotation without exposing private keys to tenants. | [SEC-SIG-001](https://github.com/gntik-ai/falcone-secrets/issues/42) |
| FR-SIG-002-1 | Transit encrypt/decrypt, data-key generation and rewrap must use versioned authenticated formats with resource/context binding and explicit permissions. | [SEC-SIG-002](https://github.com/gntik-ai/falcone-secrets/issues/43) |
| FR-SIG-002-2 | Transit services must not persist caller plaintext and must separate plaintext-returning operations from ciphertext-only rewrapping. | [SEC-SIG-002](https://github.com/gntik-ai/falcone-secrets/issues/43) |
| FR-SIG-003-1 | The system must support scoped storage and delivery of certificate/private-key pairs with expiry metadata and validated ownership. | [SEC-SIG-003](https://github.com/gntik-ai/falcone-secrets/issues/44) |
| FR-SIG-003-2 | Any enabled certificate issuance adapter must restrict names, usages, TTL and issuer authority and expose renewal/revocation limitations. | [SEC-SIG-003](https://github.com/gntik-ai/falcone-secrets/issues/44) |

## Audit, durable events and observability

| ID | Requirement | Story |
|---|---|---|
| FR-AUD-001-1 | Sensitive reads, writes, decrypt/sign operations and denied access must emit scoped audit records without plaintext values, reusable credentials or request bodies. | [SEC-AUD-001](https://github.com/gntik-ai/falcone-secrets/issues/45) |
| FR-AUD-001-2 | Security mutations must atomically accept audit records, and value release must fail safely if its required durable audit acceptance cannot be recorded. | [SEC-AUD-001](https://github.com/gntik-ai/falcone-secrets/issues/45) |
| FR-AUD-002-1 | Metadata changes and propagation intent must commit in one PostgreSQL transaction and deliver through the existing event bus with at-least-once semantics. | [SEC-AUD-002](https://github.com/gntik-ai/falcone-secrets/issues/46) |
| FR-AUD-002-2 | Workers must use idempotency, aggregate revisions and fenced claims to prevent stale rotations or events from resurrecting revoked state. | [SEC-AUD-002](https://github.com/gntik-ai/falcone-secrets/issues/46) |
| FR-AUD-003-1 | The service must expose bounded-cardinality metrics for key/seal state, auth freshness, leases, rotation adoption, failed revocation and audit backlog. | [SEC-AUD-003](https://github.com/gntik-ai/falcone-secrets/issues/47) |
| FR-AUD-003-2 | Audit and metadata retention/export must enforce Falcone tenant permissions and an approved privacy/retention policy. | [SEC-AUD-003](https://github.com/gntik-ai/falcone-secrets/issues/47) |

## Restricted deployment and reliable operation

| ID | Requirement | Story |
|---|---|---|
| FR-OPS-001-1 | Baseline workloads must run as arbitrary non-root UID with dropped capabilities, restricted mounts and no privileged containers, host access or new CRDs. | [SEC-OPS-001](https://github.com/gntik-ai/falcone-secrets/issues/48) |
| FR-OPS-001-2 | Installation must document external database, root-key provider, TLS, eventing, audit and bootstrap prerequisites and their precise permissions. | [SEC-OPS-001](https://github.com/gntik-ai/falcone-secrets/issues/48) |
| FR-OPS-002-1 | The project must benchmark metadata, resolution, key use, lease issuance and rotation/consumer adoption separately under a documented workload. | [SEC-OPS-002](https://github.com/gntik-ai/falcone-secrets/issues/49) |
| FR-OPS-002-2 | Availability, latency, freshness, recovery and data-loss objectives must state topology, dependency boundaries and measurement assumptions. | [SEC-OPS-002](https://github.com/gntik-ai/falcone-secrets/issues/49) |
| FR-OPS-003-1 | Backup and restore procedures must coordinate ciphertext, metadata, key versions, revocation state, outstanding leases and consumer state. | [SEC-OPS-003](https://github.com/gntik-ai/falcone-secrets/issues/50) |
| FR-OPS-003-2 | Production release must name runtime, on-call, key-custody and independent security-qualification owners. | [SEC-OPS-003](https://github.com/gntik-ai/falcone-secrets/issues/50) |

## OpenBao migration and retirement

| ID | Requirement | Story |
|---|---|---|
| FR-MIG-001-1 | Migration tools must inventory secret/version metadata, auth policies, consumers, mounts, leases and special key engines without exposing values in reports. | [SEC-MIG-001](https://github.com/gntik-ai/falcone-secrets/issues/51) |
| FR-MIG-001-2 | Value migration must use a scoped encrypted transfer channel, destination envelope encryption and resumable identity/version mapping. | [SEC-MIG-001](https://github.com/gntik-ai/falcone-secrets/issues/51) |
| FR-MIG-002-1 | Migration must maintain one authoritative writer per scope and record a cutover revision before changing resolver and projector routing. | [SEC-MIG-002](https://github.com/gntik-ai/falcone-secrets/issues/52) |
| FR-MIG-002-2 | Canaries must verify value-free public contracts, scoped resolution, rotation, revocation and recovery for every enabled consumer. | [SEC-MIG-002](https://github.com/gntik-ai/falcone-secrets/issues/52) |
| FR-MIG-003-1 | OpenBao retirement must require signed-off contract, consumer, custody, lease, cryptographic and disaster-recovery evidence for all in-use engines. | [SEC-MIG-003](https://github.com/gntik-ai/falcone-secrets/issues/53) |
| FR-MIG-003-2 | Retirement must remove obsolete trust, credentials and backend routes only after the approved rollback and key-retention requirements are satisfied. | [SEC-MIG-003](https://github.com/gntik-ai/falcone-secrets/issues/53) |

## Developer tooling and security qualification

| ID | Requirement | Story |
|---|---|---|
| FR-DEV-001-1 | The project must publish OpenAPI/event schemas and TypeScript/Go examples distinguishing metadata, value resolution, key use and lifecycle operations. | [SEC-DEV-001](https://github.com/gntik-ai/falcone-secrets/issues/54) |
| FR-DEV-001-2 | Local fixtures must include multiple tenants, scoped workloads, rotation failures and synthetic secrets without embedding real or provider-shaped credentials. | [SEC-DEV-001](https://github.com/gntik-ai/falcone-secrets/issues/54) |
| FR-DEV-002-1 | Release builds must pin dependencies, publish an SBOM and signed image provenance, and review protocol/crypto updates against compatibility tests. | [SEC-DEV-002](https://github.com/gntik-ai/falcone-secrets/issues/55) |
| FR-DEV-002-2 | The project must define vulnerability reporting, patch ownership, dependency license review and secure diagnostic defaults. | [SEC-DEV-002](https://github.com/gntik-ai/falcone-secrets/issues/55) |
| FR-DEV-003-1 | A release candidate must pass cross-tenant, tamper, replay, stale-policy, secret-leakage and dependency-failure tests for all enabled engines and delivery paths. | [SEC-DEV-003](https://github.com/gntik-ai/falcone-secrets/issues/56) |
| FR-DEV-003-2 | Production cutover must require independent security review of key custody, bootstrap, secret handling, authorization and external revocation guarantees. | [SEC-DEV-003](https://github.com/gntik-ai/falcone-secrets/issues/56) |

