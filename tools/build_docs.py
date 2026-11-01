#!/usr/bin/env python3
"""Generate planning documents and issue payloads; this is not a secrets runtime."""
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'gntik-ai/falcone-secrets'
DATE = '2026-11-01'
BASELINE = 'ed04fe7269d32f3f3e3cbc434ab5168389153ed6'
EPICS = []

def epic(code, title, outcome):
    value=dict(id=f'SEC-{code}', category=code.lower(), title=title, outcome=outcome, stories=[])
    EPICS.append(value)
    return value

def story(e, title, persona, want, benefit, phase, effort, deps, requirements, acceptance):
    sid=f"{e['id']}-{len(e['stories'])+1:03d}"
    e['stories'].append(dict(id=sid,title=title,description=want[0].upper()+want[1:]+'.',
      story=f'As {persona}, I want {want}, so that {benefit}.',phase=phase,effort=effort,dependencies=deps,
      requirements=[dict(id=f'FR-{sid[4:]}-{i+1}',statement=x) for i,x in enumerate(requirements)],acceptance=acceptance))

e=epic('CON','Falcone contracts and replacement scope','Define an evidence-based replacement boundary without changing Falcone product semantics.')
story(e,'Freeze the current secret-management contract inventory','a Falcone maintainer','versioned fixtures for every secret consumer','migration preserves existing behavior','P0','M',[],[
 'The project must inventory every OpenBao client, mount, auth path, secret reference, rotation consumer and non-OpenBao key lifecycle against a pinned Falcone commit.',
 'The system must preserve approved Falcone API routes, metadata fields, status codes and error precedence through contract tests.'
],[ 'Cover workspace secret CRUD, inventory domains, rotation, consumer acknowledgements, BYOK, function projection and workflow credential references.', 'Distinguish code, documentation, deployment evidence and planned sibling-service contracts; record actual OpenBao/ESO versions separately.', 'Identify direct Vault-compatible callers and make an explicit adapter/retirement decision for each; do not promise the entire Vault API.' ])
story(e,'Define ownership and first-party service boundaries','a platform architect','one owner per secret, policy, credential and projection','services do not compete to manage security state','P0','M',['SEC-CON-001'],[
 'The system must define a single authoritative writer for secret versions, rotation state, leases, policies and backend credentials throughout migration.',
 'Falcone IAM must remain the owner of users, roles and federation, while Falcone quota services remain the owner of entitlements and accounting.'
],[ 'Document IAM/secrets/bootstrap dependencies and the transition from OpenBao to falcone-secrets without modifying sibling repositories implicitly.', 'Map legacy domains platform, tenant, functions, gateway and iam to canonical scoped resources; ownership is not inferred from a caller path.', 'Separate operator bootstrap material, IAM session credentials, backend credentials and tenant application secrets, with named custodians.' ])
story(e,'Qualify implementation components and license provenance','a maintainer','reviewed cryptographic and protocol components','custom product behavior does not require custom cryptography','P0','L',['SEC-CON-001'],[
 'The implementation must use maintained cryptographic, TLS and identity libraries with pinned versions and an upgrade owner.',
 'Dependency intake must distinguish open-source references from source-available and enterprise-only code and record provenance before copying or embedding code.'
],[ 'Prototype the proposed TypeScript/Node service and key-provider adapter against required algorithms, throughput and memory exposure; record alternatives if qualification fails.', 'Review OpenBao MPL-2.0, current Vault BSL, Infisical editions and each chosen dependency; the project license remains an owner decision.', 'Do not treat an upstream certification, feature advertisement or reference design as certification of the configured Falcone service.' ])

e=epic('AUTH','Identity, policy and tenant isolation','Authorize each metadata, value, key and lifecycle operation using trusted Falcone context.')
story(e,'Integrate user and service authorization with Falcone IAM','a service owner','audience-bound identities and scoped authorization decisions','secrets are accessible only to approved callers','P1','L',['SEC-CON-002'],[
 'Every online secret operation must authenticate its caller and authorize action, resource, tenant/workspace, audience and delegated authority.',
 'Metadata listing, value resolution, key use, key administration, rotation and destruction must be distinct permissions with deny-by-default behavior.'
],[ 'Test Keycloak-era and falcone-iam adapters without adding a second login/federation stack to secrets; preserve SAML/OIDC/LDAP/AD/SCIM identity handling through IAM.', 'Reject forged gateway headers, wrong audiences, cross-tenant IDs, untrusted resource owners and stale policy revisions.', 'Preserve current public role/error contracts through an adapter while reviewing legacy role-name aliases; a platform role does not automatically reveal values.' ])
story(e,'Implement canonical namespaces and reference validation','a tenant administrator','stable scoped secret references','a reference cannot escape its tenant or environment','P1','M',['SEC-AUTH-001'],[
 'Secret IDs and references must bind domain, tenant, workspace/environment, secret identity and permitted version selection without accepting arbitrary backend paths.',
 'All list, count, search and lookup operations must filter by authorized scope before pagination and avoid cross-tenant existence disclosure.'
],[ 'Normalize or reject ambiguous encoding, traversal, mixed separators, duplicate names and conflicting tenant/workspace fields.', 'Test the same secret name in two tenants/workspaces; references are locators requiring authorization, not bearer authority.', 'Keep metadata-only public schemas distinct from internal resolution contracts and preserve legacy name aliases where required.' ])
story(e,'Implement workload credentials and bounded policy freshness','a runtime operator','short-lived workload access with a finite freshness budget','cancelled or deauthorized work cannot keep fetching secrets','P1','L',['SEC-AUTH-001','SEC-BOOT-002'],[
 'Workload authentication must bind the verified service or execution identity to tenant/workspace, attempt, resource, audience and expiry.',
 'Resolution and lease renewal must deny when required authorization freshness cannot be established within the approved bound.'
],[ 'Use Falcone execution grants or a qualified workload identity; guest-supplied scope and Kubernetes labels alone never grant access.', 'No cluster-wide TokenReview permission is required by the baseline; document offline JWT revocation limitations or separately approved reviewer integration.', 'Test expired/cancelled attempts, delegated scope reduction, IAM outage and same-name service accounts across namespaces and tenants.' ])

e=epic('KV','Versioned secret storage and lifecycle','Store recoverable values encrypted while preserving write-only product APIs.')
story(e,'Implement write-only workspace secret CRUD','a workspace administrator','the existing Falcone secret APIs on the new backend','applications can migrate without exposing their values','P1','L',['SEC-AUTH-002','SEC-KEY-001'],[
 'Workspace create, replace, metadata read, list and delete must preserve Falcone write-only value semantics and the approved response schemas.',
 'Create must be atomic and create-only, replacement must not leak prior values, and public delete must remove all versions from live resolution as contracted.'
],[ 'Verify 201 create, 409 duplicate without overwrite, 200 metadata/replace, 204 delete and 404 absent behavior with existing error precedence.', 'Preserve secretName/name alias, timestamps, description and resolvedRefCount; expose neither value nor internal version through FunctionWorkspaceSecret.', 'Enforce the current name rule and value limit, sanitized failures and reference-registry errors; no console reveal action is introduced.' ])
story(e,'Implement internal versions, concurrency and retention','a service developer','immutable internal versions and compare-and-swap writes','concurrent updates cannot silently corrupt state','P1','L',['SEC-KV-001'],[
 'The store must assign immutable version IDs and use atomic revision checks for create/replace, active-version selection and metadata changes.',
 'Internal soft deletion, recovery and irreversible destruction must be distinct operations with explicit retention and authorization rules.'
],[ 'Test concurrent writers, idempotency-key conflicts, retry after commit and references pinned to removed versions.', 'Do not turn the existing public delete-all route into a recoverable soft delete or resurrect a revoked version through rollback.', 'Document backup retention and historical-key exposure: deleting live records is not proof of immediate physical erasure from every backup.' ])
story(e,'Implement inventory, reference tracking and tenant purge','an operator','scope-filtered inventory and dependency tracking','secret cleanup does not leave hidden references or access','P2','M',['SEC-KV-002','SEC-AUD-001'],[
 'Inventory and metadata endpoints must preserve approved domains and legacy compatibility fields without returning values or ciphertext.',
 'Tenant/workspace purge must tombstone identity and references, block new resolution and expose retryable consumer cleanup progress.'
],[ 'Maintain value-free resource references and correct distinct-function counts even when a referenced secret has been deleted.', 'A delayed event or stale projection cannot recreate purged secrets; incomplete cleanup is reported rather than marked complete.', 'Metadata exports, search indexes and support diagnostics obey scope and redaction rules, including user-supplied descriptions.' ])

e=epic('KEY','Encryption, key custody and rewrapping','Protect values with independently rooted encryption and explicit key-version lifecycle.')
story(e,'Implement authenticated envelope encryption','a security engineer','encrypted values bound to their resource context','database access alone cannot reveal or relocate secrets','P1','L',['SEC-CON-003','SEC-BOOT-001'],[
 'Secret values must use reviewed authenticated encryption with fresh per-version data keys and authenticated tenant/resource/version context.',
 'Root key-encryption authority must be outside the ciphertext database, with a documented KMS/HSM or approved operator-unlock custody profile.'
],[ 'Use a supported AEAD library and managed nonce generation; reject modified ciphertext, AAD, key IDs and cross-resource substitution.', 'Store only ciphertext, wrapped data keys and required metadata; PostgreSQL/WAL and backups must never contain plaintext value columns.', 'Separate platform/domain wrapping keys where policy requires; document that an online authorized service can still decrypt and process values.' ])
story(e,'Implement key rotation, rewrap and compromise response','a key custodian','versioned key rotation and resumable rewrapping','key replacement does not lose data or revive compromised access','P1','L',['SEC-KEY-001'],[
 'Key rotation must distinguish root/KEK rewrapping, data-key re-encryption and external credential replacement, with separate state and permissions.',
 'Old keys must not be destroyed until retained ciphertext, backups and restore requirements have been reconciled under an approved retirement policy.'
],[ 'Resume interrupted batches with checkpoints and compare-and-swap; concurrent writes use the designated active key version.', 'Test mixed replicas, KMS outage and lost acknowledgements without claiming rewrap re-encrypts plaintext under a fresh data key.', 'Emergency key compromise procedures include external credential rotation and assessed backup exposure; rewrapping alone cannot undo prior key compromise.' ])
story(e,'Protect memory, transport and key-provider boundaries','a security operator','explicit plaintext exposure and transport limits','the implementation avoids misleading encryption guarantees','P2','L',['SEC-KEY-001','SEC-BOOT-002'],[
 'All value-bearing service traffic must use authenticated TLS and explicit size/time limits, with debugging and request-body capture disabled in production.',
 'Key-provider interfaces must distinguish non-exportable operations from exported software keys and fail safely on unsupported algorithms or custody mode.'
],[ 'Exclude values from logs, traces, core dumps, metrics and error bodies; qualify crash diagnostics and proxy capture settings.', 'Document Node/GC zeroization limits, ephemeral plaintext lifetime and optional isolated crypto workers; never claim guaranteed process-memory erasure.', 'Exercise provider outages, invalid certificates, algorithm mismatch and excessive decrypt/sign requests with bounded resource use.' ])

e=epic('BOOT','Bootstrap, sealing and recovery trust','Start and recover secrets and IAM without a circular dependency or permanent root token.')
story(e,'Define and implement root-of-trust bootstrap','a platform installer','a concrete first-install and unlock profile','secrets can start before it stores platform credentials','P0','L',['SEC-CON-002','SEC-CON-003'],[
 'The deployment must define independent custody for root wrapping authority, startup database access and recovery authorization before production initialization.',
 'Bootstrap must not require a credential retrievable only from the uninitialized secrets service or a token signed only by an unavailable IAM dependency.'
],[ 'Specify external KMS/HSM workload identity as preferred profile and a separately approved offline operator-unlock alternative; no external KMS availability is assumed.', 'Use a one-time authenticated initialization transaction, no default root password and no key material in Helm values or release manifests.', 'Test fresh install and total restart with IAM offline and record the exact bootstrap trust dependencies.' ])
story(e,'Implement narrow IAM signing bootstrap and sealed-state behavior','an IAM maintainer','a restricted bootstrap signing path','identity recovery does not require tenant secret access','P1','L',['SEC-BOOT-001'],[
 'A pre-enrolled IAM workload identity must be able to perform only approved signing-key operations needed to start IAM, independently of IAM-issued end-user tokens.',
 'Sealed or unavailable key state must deny value/sign operations and expose sanitized readiness/status without restarting endlessly through liveness failure.'
],[ 'Bind operator-provisioned mTLS identity or another independently verifiable workload identity to an exact IAM key purpose; no wildcard secret reads.', 'After IAM is available, normal secret authorization uses IAM policy; bootstrap credentials cannot be exchanged for general tenant access.', 'Test issuer/key rotation, IAM down, secrets restart, expired bootstrap identity and recovery access without calling workflows/serverless.' ])
story(e,'Implement break-glass, recovery and custodian procedures','a recovery custodian','audited emergency access and restoration','key loss or platform outage has a controlled recovery path','P2','L',['SEC-BOOT-002','SEC-KEY-002','SEC-AUD-001'],[
 'Recovery access must be strongly authenticated, time-bounded, narrowly scoped and auditable independently of ordinary tenant credentials.',
 'Recovery material and its backups must be held separately from encrypted application data and tested under the approved custody policy.'
],[ 'Define named custodian roles and dual control for destructive key retirement; use vetted threshold tooling only if that custody profile is selected.', 'Run an isolated loss-of-IAM and key-provider recovery exercise; prove that stolen ciphertext backups alone cannot unlock the service.', 'Expire/revoke emergency credentials after use and document the consequences of permanently lost keys without inventing a decryption backdoor.' ])

e=epic('DYN','Dynamic credentials and leases','Issue bounded backend credentials and track actual revocation rather than metadata expiry alone.')
story(e,'Implement durable lease issuance and lifecycle','a workload developer','renewable short-lived credentials','tasks use bounded access instead of shared permanent passwords','P2','L',['SEC-AUTH-003','SEC-KV-002'],[
 'Dynamic credential issuance must persist a tenant/workload-bound lease with backend identity, maximum TTL, renewal conditions and revocation status.',
 'Lease renewal must require current authorization and cannot extend past parent grant, job deadline or configured maximum lifetime.'
],[ 'Handle client retries and unknown provider outcomes without duplicate untracked credentials; mark unresolved attempts for reconciliation.', 'Test expiration, cancellation, revoke/renew races and recovery after worker crash using fenced claims.', 'An expired database lease does not mean the backend credential is revoked; report pending/failed revocation until verified.' ])
story(e,'Implement PostgreSQL credential adapter','a data-service owner','scoped dynamic PostgreSQL identities','database activity has accountable least-privilege credentials','P2','L',['SEC-DYN-001'],[
 'The PostgreSQL adapter must create and revoke credentials through approved role templates with tenant/workspace and RLS-compatible privileges.',
 'Provider administration credentials must be separated from issued workload credentials and limited to approved lifecycle operations.'
],[ 'Test login expiry, pooling/session behavior, active-session termination policy and schema/role privileges; never give workload users ownership or superuser rights.', 'Escape identifiers through vetted APIs/templates and reject tenant-supplied arbitrary SQL for role creation/revocation.', 'Reconcile orphan roles after ambiguous create/drop outcomes and provider outage; keep credential bytes out of history and audit.' ])
story(e,'Qualify S3, event and external-provider credential adapters','an integration owner','a capability matrix for backend credential lifecycle','unsupported TTL or rotation behavior is visible','P2','L',['SEC-DYN-001','SEC-CON-001'],[
 'Every provider adapter must declare issuance, renewal, overlap, expiry and revocation capabilities and reject unsupported guarantees.',
 'SeaweedFS, Kafka-compatible eventing and external-provider credential integrations must preserve Falcone resource-scoping rules.'
],[ 'Preserve per-bucket S3 grants and verify actual SeaweedFS release/mode behavior; do not assume AWS STS equivalence.', 'Distinguish broker ACL changes, static-password rotation and true dynamic credentials; test connection reuse after revoke.', 'External providers without a rotation API use an explicit operator-supplied replacement flow and do not receive fabricated automatic-rotation support.' ])

e=epic('ROT','Rotation and consumer convergence','Coordinate secret-version changes with real target activation and authenticated consumer evidence.')
story(e,'Implement resumable rotation orchestration','a service operator','a durable staged rotation operation','partial failures cannot leave the platform silently inconsistent','P1','L',['SEC-KV-002','SEC-AUTH-001'],[
 'Rotation must use a persisted state machine for prepare, provider activation, consumer delivery, acknowledgement and old-credential revocation.',
 'Local secret/version changes and propagation intent must commit atomically while external provider effects use fenced, retryable reconciliation.'
],[ 'Map current active/grace/expired/revoked states and API grace limits to internal operation states without silently changing contracts.', 'Serialize or fence overlapping rotations of one resource and test crash/timeout at every provider/commit boundary.', 'Preserve justified force/immediate paths with explicit consequences; do not claim database transactions make external credential changes atomic.' ])
story(e,'Implement authenticated acknowledgements and convergence status','a rotation owner','per-consumer adoption evidence','a successful store write is not mistaken for completed rollout','P2','L',['SEC-ROT-001','SEC-DEL-001'],[
 'Only the registered authenticated consumer for the correct tenant/resource/version may acknowledge receipt or successful reload.',
 'Rotation status must distinguish persisted, delivered, loaded, validated and revoked outcomes with consumer deadlines and retryable failures.'
],[ 'Preserve principal-to-consumer matching and reject forged IDs, cross-tenant ACKs, stale versions and unregistered consumers.', 'Treat Kubernetes Secret update as delivery only; environment-variable consumers require rollout/reload and validation before acknowledgement.', 'Expose missing-consumer and timeout status in the Falcone console; force completion is an audited exception, not evidence of successful adoption.' ])
story(e,'Implement grace expiry, revocation and stalled-work recovery','an on-call engineer','bounded grace and visible failed revocation','old credentials do not remain active indefinitely without notice','P2','L',['SEC-ROT-002','SEC-DYN-001','SEC-AUD-002'],[
 'Grace expiry and revocation jobs must persist deadlines and survive restarts, duplicate delivery and clock-skew limits.',
 'Old credential revocation must be verified per backend and unresolved operations must remain visible for operator action.'
],[ 'Test offline consumer, provider outage, database failover, duplicate job and revoke/renew races with leases and fencing.', 'Emergency revoke can prioritize access removal over availability; planned grace completion requires configured adoption evidence.', 'Document that deleting stored bytes or disabling reads cannot recall a credential already copied by a process; rotate at its accepting backend.' ])

e=epic('DEL','Secret delivery and workload confinement','Deliver only authorized material through existing Falcone execution and deployment boundaries.')
story(e,'Implement namespaced delivery and optional ESO adapters','a platform operator','secret delivery without a mandatory new operator','the service can run in restricted OpenShift environments','P1','L',['SEC-AUTH-003','SEC-KV-002'],[
 'The baseline delivery path must use approved SDK/host-side resolution or a namespace-scoped projector without requiring new CRDs or cluster-wide privileges.',
 'Existing ESO consumers must have a tested explicit provider adapter or limited compatibility surface before their OpenBao backing store is removed.'
],[ 'Inventory current ClusterSecretStore/ExternalSecret usage; retain approved installed ESO during migration but do not require installing it for the native baseline.', 'A namespace projector writes only owned approved Secret names and never honors arbitrary target paths or namespaces from a tenant.', 'Document Kubernetes Secret/etcd exposure and RBAC; mounted files may update, but environment variables require process restart and all delivery modes need adoption evidence.' ])
story(e,'Integrate trusted serverless hosts and function projections','a function developer','scoped secret handles in function execution','untrusted code cannot read platform or neighboring secrets','P2','L',['SEC-DEL-001','SEC-ROT-002'],[
 'Current function deployment must preserve named secret declarations and owned secretKeyRef projection without embedding values in pod specs or saved revisions.',
 'Native serverless secret resolution must follow approved host/shim and per-attempt identity contracts without exposing host credentials to guest code.'
],[ 'Test missing/deleted references, simultaneous deploy/rotate/delete, stale revisions and cross-pool/workspace attempts.', 'Preserve serverless ADR status and the existing ESO-delivery proposal until separately reviewed; do not silently replace its host trust design.', 'For approved narrow guest grants, document that code receiving plaintext can exfiltrate it; use host-mediated operations where the application permits.' ])
story(e,'Integrate workflow activities and execution credential references','a workflow author','freshly authorized secrets at activity boundaries','long-running execution does not persist reusable secrets in history','P2','L',['SEC-DEL-001','SEC-DYN-001'],[
 'Temporal-era and native workflow adapters must resolve secret references only for the verified tenant/workspace and authoritative execution lineage.',
 'Workflow histories, checkpoints, retries and task payloads must not contain resolved secret values or reusable bearer credentials.'
],[ 'Test paused/retried workflows beyond token expiry, cancellation, reset/run lineage and unauthorized reference reuse.', 'Define pinned-versus-current secret version semantics explicitly; a pinned reference does not override revocation or extend lease lifetime.', 'Keep IAM token issuance and workflow lineage ownership separate from secret custody; encrypt any retained platform credential records and avoid bearer handles in logs.' ])

e=epic('INT','Falcone product and infrastructure integrations','Preserve native consumers including BYOK and independent key lifecycles.')
story(e,'Integrate gateway, consoles, SDKs and provisioning','a Falcone user','consistent secret administration through existing interfaces','the backend replacement is transparent to supported clients','P2','L',['SEC-KV-003','SEC-ROT-002'],[
 'APISIX, both control-plane paths, consoles and supported SDKs must preserve approved Falcone secret metadata and lifecycle contracts.',
 'Provisioning and quota integrations must use Falcone ownership and accounting decisions without duplicating user or billing databases.'
],[ 'Test gateway/header trust, secret inventory pagination, write-only forms, cleared input state and existing degraded-backend errors.', 'Preserve config.secretRefs and bootstrap-created/adopted Kubernetes Secret keys; never print values in Helm templates, diffs or releases.', 'Publish compatibility fixtures for existing provider-neutral adapters and explicit schema versions for new internal methods.' ])
story(e,'Integrate BYOK and provider credential brokers','a workspace owner','provider credentials confined to the connection scope','LLM requests cannot leak unrelated secrets','P2','L',['SEC-DEL-001','SEC-AUTH-002'],[
 'LLM/embedding secret resolution must preserve workspaceSecret and approved reserved-env reference rules and endpoint confinement.',
 'Provider token caches must be scoped to connection identity/version and be invalidated on credential rotation, permission loss or endpoint changes.'
],[ 'Resolve under authoritative connection/execution scope, not a worker default; reject mixed references and cross-workspace reads.', 'Preserve SSRF, TLS and redirect checks before sending resolved credentials; changing the secrets backend must not widen destination trust.', 'Test current fetch-per-request keys separately from short-lived exchanged token caches, workflow-worker gaps and failed provider refresh without logging credentials.' ])
story(e,'Integrate webhook, IAM and platform key lifecycles','a platform security owner','explicit adapters for independently managed keys','migration cannot make encrypted state unrecoverable','P2','L',['SEC-SIG-001','SEC-BOOT-002','SEC-CON-001'],[
 'Platform webhook master keys, flow-trigger keys, IAM signing/federation secrets and platform database credentials must retain their distinct lifecycle and recovery contracts.',
 'Migration of a non-OpenBao key custodian must require a versioned adapter and paired ciphertext/key recovery evidence before changing its source.'
],[ 'Preserve the existing webhook lifecycle contract and its draft/qualification status; no external-manager in-place mutation is assumed safe.', 'Separate IAM-owned password verifiers/API-key hashes from recoverable bytes; keep SAML/OIDC/LDAP/AD/SCIM protocol implementation inside IAM.', 'Test old/new ciphertext readability, application startup checks, backup key matching and provider identity rotation; do not rotate platform roots as ordinary tenant values.' ])

e=epic('SIG','Cryptographic operations and certificate custody','Offer reviewed key operations without turning secrets into an unrestricted signing oracle.')
story(e,'Implement purpose-bound signing and verification','an IAM service owner','managed signing operations with exact key policy','authentication keys stay outside ordinary application runtimes','P2','L',['SEC-KEY-002','SEC-BOOT-002','SEC-AUTH-001'],[
 'Signing APIs must bind key purpose, caller, allowed algorithms and message context, with separate permissions for use and administration.',
 'IAM integration must publish compatible public key metadata and support tested signing-key rotation without exposing private keys to tenants.'
],[ 'Qualify the actual IAM protocol-library remote-signing adapter; encrypted key export is a distinct documented fallback, not non-exportable signing.', 'Protect bootstrap signing with exact key and message-purpose constraints, including validated IAM token/header fields where relevant.', 'Test cross-purpose signing, algorithm confusion, key retirement, verification overlap and compromise handling; no generic unrestricted root signer.' ])
story(e,'Implement transit encryption and data-key operations','an application developer','scoped encryption operations using managed keys','sensitive application payloads can remain encrypted outside the secret store','P2','L',['SEC-KEY-002','SEC-AUTH-001'],[
 'Transit encrypt/decrypt, data-key generation and rewrap must use versioned authenticated formats with resource/context binding and explicit permissions.',
 'Transit services must not persist caller plaintext and must separate plaintext-returning operations from ciphertext-only rewrapping.'
],[ 'Test altered context, cross-tenant ciphertext, retired keys and idempotent retries without nonce reuse; disable convergent encryption by default.', 'Set bounded message sizes and request quotas; no arbitrary large-file encryption service is implied.', 'Differentiate opaque application ciphertext from stored KV values and retain old-key/backups evidence before key retirement.' ])
story(e,'Qualify certificate custody and optional CA integration','a platform TLS operator','a supported certificate lifecycle boundary','TLS renewal and key custody remain recoverable','P2','M',['SEC-KEY-001','SEC-CON-001'],[
 'The system must support scoped storage and delivery of certificate/private-key pairs with expiry metadata and validated ownership.',
 'Any enabled certificate issuance adapter must restrict names, usages, TTL and issuer authority and expose renewal/revocation limitations.'
],[ 'Integrate existing approved cert-manager or external CA paths without requiring a new operator or replacing the root CA.', 'Publish a capability decision for optional step-ca/PKI and SSH signing; these extensions are not assumed required for OpenBao retirement unless inventory proves current use.', 'Test pair mismatch, expiry alert, rollout and recovery; offline certificate verification does not provide universal instant revocation.' ])

e=epic('AUD','Audit, durable events and observability','Record security actions durably without turning evidence into a second secret store.')
story(e,'Implement value-free audit and read-release evidence','a security auditor','durable correlated access records','sensitive value access can be investigated','P1','L',['SEC-CON-002','SEC-AUTH-001'],[
 'Sensitive reads, writes, decrypt/sign operations and denied access must emit scoped audit records without plaintext values, reusable credentials or request bodies.',
 'Security mutations must atomically accept audit records, and value release must fail safely if its required durable audit acceptance cannot be recorded.'
],[ 'Preserve approved SecretAuditEvent fields through versioned mapping, including legacy vaultRequestId where needed; free-text fields are sanitized.', 'Audit intent is committed before value release and outcome after; a disconnect after send is recorded as unknown delivery rather than a false success.', 'Tenant administrators cannot rewrite audit history; test read-path durability, leak fixtures, correlation and cross-tenant export denial.' ])
story(e,'Implement transactional outbox and reconciliation workers','an operator','durable versioned lifecycle events','broker outages and duplicate delivery cannot lose security changes','P1','L',['SEC-AUD-001','SEC-KV-002'],[
 'Metadata changes and propagation intent must commit in one PostgreSQL transaction and deliver through the existing event bus with at-least-once semantics.',
 'Workers must use idempotency, aggregate revisions and fenced claims to prevent stale rotations or events from resurrecting revoked state.'
],[ 'Crash before/after commit, publish and ACK without secret loss or duplicate logical effects; event payloads contain identifiers only.', 'Implement backoff, dead-letter handling and authorized replay with reconciliation rather than assuming exactly-once provider effects.', 'Event backlog capacity and IAM freshness failures are explicit; Kafka availability is not required to decrypt an already authorized request with durable local audit.' ])
story(e,'Implement metrics, inventory alerts and audit retention','an on-call engineer','redacted diagnostics and lifecycle alerts','secret failures are visible before dependent workloads fail','P2','M',['SEC-AUD-002','SEC-OPS-002'],[
 'The service must expose bounded-cardinality metrics for key/seal state, auth freshness, leases, rotation adoption, failed revocation and audit backlog.',
 'Audit and metadata retention/export must enforce Falcone tenant permissions and an approved privacy/retention policy.'
],[ 'Separate expected denies from service errors and report consumer/target progress without secret-name or user-ID metric explosions.', 'Alert on stale auth, expiring provider identity, stalled rotation, orphan lease, root-key loss and certificate expiry with runbooks.', 'Test sanctioned audit export and protected external anchoring/tamper evidence; a database hash chain alone is not proof against an administrator who controls all copies.' ])

e=epic('OPS','Restricted deployment and reliable operation','Operate a native service on Kubernetes/OpenShift with explicit custody and recovery ownership.')
story(e,'Package restricted namespace deployments','a platform operator','reproducible nonprivileged deployment artifacts','corporate OpenShift can run the service without a new cluster operator','P1','M',['SEC-BOOT-002','SEC-KEY-001'],[
 'Baseline workloads must run as arbitrary non-root UID with dropped capabilities, restricted mounts and no privileged containers, host access or new CRDs.',
 'Installation must document external database, root-key provider, TLS, eventing, audit and bootstrap prerequisites and their precise permissions.'
],[ 'Provide API/worker roles, probes, network policy, graceful shutdown, rolling migrations and bounded temporary storage.', 'Qualify administrator-approved Kubernetes minors and exact OpenShift build; do not infer product support from Kubernetes patch numbers alone.', 'Do not require mlock capabilities or promise protection against cluster administrators; qualify process/core-dump/swap behavior under available policy.' ])
story(e,'Benchmark and agree service objectives','a product owner','separate measured secret-service objectives','capacity reflects secret operations instead of event throughput','P0','M',['SEC-CON-001'],[
 'The project must benchmark metadata, resolution, key use, lease issuance and rotation/consumer adoption separately under a documented workload.',
 'Availability, latency, freshness, recovery and data-loss objectives must state topology, dependency boundaries and measurement assumptions.'
],[ 'Use operations.md targets as hypotheses and include cold KMS calls, audit commit cost, tenant skew and provider outages.', 'Do not interpret 10,000 deployed functions or 100k event messages per second as secret-read or signing QPS.', 'Determine replica, database and key-provider capacity from measured concurrency and payload size before accepting an SLA.' ])
story(e,'Implement backups, restore, upgrades and ownership','an SRE','tested restoration with the matching key material','a disaster does not restore inaccessible or previously revoked credentials','P2','L',['SEC-OPS-001','SEC-BOOT-003','SEC-ROT-003'],[
 'Backup and restore procedures must coordinate ciphertext, metadata, key versions, revocation state, outstanding leases and consumer state.',
 'Production release must name runtime, on-call, key-custody and independent security-qualification owners.'
],[ 'Restore in an isolated environment with egress blocked; reconcile actual backend credentials and IAM epochs before enabling resolution or rotation.', 'Test PITR, missing old KEK, incompatible schema and outstanding external leases; no rollback silently revives revoked credentials.', 'Exercise root-key compromise, KMS outage, IAM unavailable and broker/database failure with measured RPO/RTO and reviewed upgrade runbooks.' ])

e=epic('MIG','OpenBao migration and retirement','Move by scoped consumer with one writer, controlled plaintext handling and explicit rollback.')
story(e,'Build a dry-run inventory and controlled importer','a migration engineer','repeatable scoped import with sanitized evidence','OpenBao data moves without untracked exports','P1','L',['SEC-CON-001','SEC-KV-002'],[
 'Migration tools must inventory secret/version metadata, auth policies, consumers, mounts, leases and special key engines without exposing values in reports.',
 'Value migration must use a scoped encrypted transfer channel, destination envelope encryption and resumable identity/version mapping.'
],[ 'Dry runs report counts, unsupported engines and source/destination mappings; migration never reads private deployment credentials into planning artifacts.', 'Use protected equality checks or isolated canaries rather than public unsalted secret hashes; no plaintext export files or CI artifacts.', 'Classify non-exportable transit keys, active leases, PKI roots and separately managed webhook keys as explicit bridge/rotation blockers rather than assuming KV export covers them.' ])
story(e,'Implement canary cutover and conflict-safe rollback','a rollout owner','fenced per-scope migration and consumer verification','a backend switch cannot lose rotations or widen access','P3','L',['SEC-MIG-001','SEC-INT-001','SEC-INT-002','SEC-INT-003','SEC-DEL-002','SEC-DEL-003','SEC-DEV-003'],[
 'Migration must maintain one authoritative writer per scope and record a cutover revision before changing resolver and projector routing.',
 'Canaries must verify value-free public contracts, scoped resolution, rotation, revocation and recovery for every enabled consumer.'
],[ 'Shadow comparison performs no duplicate external credential issuance or rotation; freeze or reconcile writes before authority handoff.', 'Test both direct Falcone adapters and approved ESO compatibility paths, including adopted Kubernetes Secrets and provider auth renewal.', 'Rollback reconciles post-cutover values, leases and key changes; it is not an unconditional old database restore or automatic fallback after denied reads.' ])
story(e,'Retire OpenBao after evidence gates','a Falcone product owner','a controlled retirement checklist','the first-party service becomes the supported secret backend','P3','M',['SEC-MIG-002','SEC-OPS-003'],[
 'OpenBao retirement must require signed-off contract, consumer, custody, lease, cryptographic and disaster-recovery evidence for all in-use engines.',
 'Retirement must remove obsolete trust, credentials and backend routes only after the approved rollback and key-retention requirements are satisfied.'
],[ 'No active consumer or non-exportable historical ciphertext remains dependent on OpenBao unless an explicitly scoped bridge postpones retirement.', 'Update deployment and sibling-service integration contracts through separately reviewed changes; this repository bootstrap does not modify those repositories.', 'Archive sanitized evidence, retain approved encrypted backups and key custody, and document residual exceptions and incident owners before production removal.' ])

e=epic('DEV','Developer tooling and security qualification','Make the custom service implementable and independently reviewable before production trust changes.')
story(e,'Publish schemas, SDK adapters and local fixtures','an integration developer','versioned APIs and synthetic test setups','I can integrate without production secrets','P1','M',['SEC-CON-001','SEC-AUTH-002'],[
 'The project must publish OpenAPI/event schemas and TypeScript/Go examples distinguishing metadata, value resolution, key use and lifecycle operations.',
 'Local fixtures must include multiple tenants, scoped workloads, rotation failures and synthetic secrets without embedding real or provider-shaped credentials.'
],[ 'Preserve public route schemas while versioning new internal methods; examples never return values through workspace metadata routes.', 'Provide a local no-production-trust profile and explicit synthetic key custody; production startup rejects development bypasses.', 'Document SDK retry/idempotency semantics and safe file/stdin handling without placing secret bytes in shell arguments or generated manifests.' ])
story(e,'Implement supply-chain and dependency release gates','a maintainer','attributable builds and maintained security dependencies','releases can be patched and reviewed','P1','M',['SEC-CON-003'],[
 'Release builds must pin dependencies, publish an SBOM and signed image provenance, and review protocol/crypto updates against compatibility tests.',
 'The project must define vulnerability reporting, patch ownership, dependency license review and secure diagnostic defaults.'
],[ 'CI scans for secrets, vulnerable dependencies, license conflicts and unsafe image permissions with owned time-limited exceptions.', 'Choose the repository license before code distribution and preserve required notices for reused open-source components.', 'Document supported runtime/provider versions and migration notes; no upstream certification or compliance label is inherited automatically.' ])
story(e,'Qualify isolation, cryptography and failure behavior','a security reviewer','adversarial and recovery evidence','OpenBao is replaced only after the native service proves its boundaries','P2','L',['SEC-KEY-003','SEC-AUTH-003','SEC-ROT-003','SEC-OPS-003','SEC-SIG-001','SEC-SIG-002','SEC-DEV-002'],[
 'A release candidate must pass cross-tenant, tamper, replay, stale-policy, secret-leakage and dependency-failure tests for all enabled engines and delivery paths.',
 'Production cutover must require independent security review of key custody, bootstrap, secret handling, authorization and external revocation guarantees.'
],[ 'Test modified AAD/ciphertext, wrong-key signing, forged consumer ACK, path injection, untrusted guest input and SSRF during provider use.', 'Inject crashes around audit/DB commit, provider activation, outbox delivery and key rotation; verify declared failure and recovery behavior.', 'Record residual memory/cluster-admin exposure, evidence gaps and owned exceptions; container hardening is not hostile-code isolation or a compliance certificate.' ])

def generate():
    mapping_path=ROOT/'docs/github-issues.json'
    mapping=json.loads(mapping_path.read_text()) if mapping_path.exists() else {}
    by_id={s['id']:s for e in EPICS for s in e['stories']}
    assert len(by_id)==sum(len(e['stories']) for e in EPICS)
    def visit(sid, stack):
        assert sid not in stack, f'Dependency cycle: {stack} -> {sid}'
        for d in by_id[sid]['dependencies']:
            assert d in by_id, f'Unknown dependency: {d}'
            visit(d,stack+[sid])
    for sid in by_id: visit(sid,[])
    def link(sid):
        n=mapping.get(sid,{}).get('number')
        return f'[{sid}](https://github.com/{REPO}/issues/{n})' if n else sid
    req=['# Functional requirements\n',f'Planning baseline: {DATE}. Requirements describe target behavior, not delivered functionality. Each requirement traces to one story. Read with [architecture](architecture.md), [security](security.md), [bootstrap](bootstrap-and-recovery.md) and [integration matrix](integration-matrix.md).\n']
    backlog=['# Epics and user stories\n','Generated by `python3 tools/build_docs.py`. S/M/L are relative complexity, not calendar promises. P0 = decisions and qualification; P1 = core; P2 = integrations and hardening; P3 = migration. Phase is the earliest stage, subject to dependencies.\n','Epics, parent links and task lists express hierarchy; no native GitHub sub-issues or Project board is implied. Each stable SEC identifier maps to an issue in github-issues.json.\n']
    issues=[]; rows=[]
    for e in EPICS:
        req += [f"## {e['title']}\n",'| ID | Requirement | Story |','|---|---|---|']
        backlog += [f"- **{link(e['id'])}: {e['title']}** — {e['outcome']}\n"]
        body=f"<!-- falcone-secrets:{e['id']} -->\n\n## Outcome\n\n{e['outcome']}\n\n## Scope\n\nCustom Falcone secret management, preserving Falcone contracts and tenant/workspace boundaries. See [architecture](https://github.com/{REPO}/blob/main/docs/architecture.md) and [requirements](https://github.com/{REPO}/blob/main/docs/requirements.md).\n\n## Stories\n\n"
        body+=''.join(f"- [ ] {link(s['id'])}: {s['title']}\n" for s in e['stories'])
        body+='\n## Exit criteria\n\nAll child criteria have linked evidence and the security/integration impact is reviewed. Planning publication does not mean implementation is complete.\n'
        if e['id'] in ('SEC-CON', 'SEC-BOOT'):
            body += f'\n## Accepted decisions\n\nOn 2026-11-01 the project owner accepted all open-point proposals without changes. [ADR 0002](https://github.com/{REPO}/blob/main/docs/decisions/0002-owner-acceptance.md) records the decision. Existing implementation and qualification criteria remain required; this epic is not completed by design acceptance.\n'
        issues.append(dict(id=e['id'],title=f"[Epic][{e['id']}] {e['title']}",body=body,labels=['type:epic',f"area:{e['category']}"]))
        rows.append(dict(ID=e['id'],Type='Epic',Title=e['title'],Parent='',Phase='',Effort='',Dependencies='',URL=mapping.get(e['id'],{}).get('url','')))
        for s in e['stories']:
            assert len(s['requirements'])==2 and len(s['acceptance'])>=3
            body=f"<!-- falcone-secrets:{s['id']} -->\n\nParent: {link(e['id'])}\n\n## User story\n\n{s['story']}\n\n## Description\n\n{s['description']}\n\nPhase: {s['phase']} · Effort: {s['effort']}\n\n## Requirements\n\n"
            for r in s['requirements']:
                req.append(f"| {r['id']} | {r['statement']} | {link(s['id'])} |")
                body+=f"- **{r['id']}**: {r['statement']}\n"
            body+='\n## Acceptance criteria\n\n'+''.join(f'- [ ] {a}\n' for a in s['acceptance'])
            body+='\n## Dependencies\n\n'+(', '.join(link(d) for d in s['dependencies']) or 'None; discovery can begin independently.')+'\n'
            body+=f"\n## Design references\n\n[Architecture](https://github.com/{REPO}/blob/main/docs/architecture.md) · [Integration matrix](https://github.com/{REPO}/blob/main/docs/integration-matrix.md) · [Security](https://github.com/{REPO}/blob/main/docs/security.md).\n"
            issues.append(dict(id=s['id'],title=f"[{s['id']}] {s['title']}",body=body,labels=['type:story',f"area:{e['category']}",f"phase:{s['phase'].lower()}",f"effort:{s['effort'].lower()}"]))
            backlog += [f"  - **{link(s['id'])}: {s['title']}** ({s['phase']}, {s['effort']})",f"    - {s['story']}",f"    - Description: {s['description']}",f"    - Requirements: {', '.join(r['id'] for r in s['requirements'])}",f"    - Dependencies: {', '.join(link(d) for d in s['dependencies']) or 'None'}"]
            backlog += [f"    - Acceptance: {a}" for a in s['acceptance']]+['']
            rows.append(dict(ID=s['id'],Type='Story',Title=s['title'],Parent=e['id'],Phase=s['phase'],Effort=s['effort'],Dependencies=';'.join(s['dependencies']),URL=mapping.get(s['id'],{}).get('url','')))
        req.append('')
    (ROOT/'docs/requirements.md').write_text('\n'.join(req)+'\n')
    (ROOT/'docs/backlog.md').write_text('\n'.join(backlog)+'\n')
    (ROOT/'docs/backlog.json').write_text(json.dumps(dict(schema_version=1,date=DATE,baseline=BASELINE,epics=EPICS),indent=2)+'\n')
    (ROOT/'docs/issue-payloads.json').write_text(json.dumps(issues,indent=2)+'\n')
    out=io.StringIO();writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (ROOT/'docs/backlog.csv').write_text(out.getvalue())
    print(json.dumps(dict(epics=len(EPICS),stories=len(by_id),requirements=sum(len(s['requirements']) for s in by_id.values()),issues=len(issues),mapped=len(mapping))))

if __name__=='__main__': generate()
