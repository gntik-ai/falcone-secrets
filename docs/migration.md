# OpenBao migration and retirement

This is a plan. No existing secrets, credentials, keys or deployments are changed by publication of this repository.

## Inventory first

Capture actual OpenBao version, storage/seal mode, auth mounts, policies, KV mounts/versions, dynamic engines, leases, transit keys, certificate authorities, audit devices, direct clients and ESO resources. Map each object to Falcone scope and consumers. Read only metadata for planning; operational secret migration requires a scoped migration identity and a reviewed execution environment.

Also inventory material outside OpenBao: bootstrap Kubernetes Secrets, database access credentials, gateway TLS, platform webhook master key, executor flow-trigger key and platform execution-token records. The current webhook runbook's release and verification status must be preserved, not assumed completed because a new backend exists.

## Portability matrix

| Source material | Proposed migration | Gate / limitation |
|---|---|---|
| KV values and versions | Scoped read/transfer in memory over TLS; destination envelope encryption; resumable ID/version map | No plaintext files, CLI arguments, logs or public value hashes; preserve API metadata/version mapping |
| KV metadata, domains, references and consumer registry | Explicit schema and ownership mapping | Legacy fields remain compatibility projections; no caller path becomes authority |
| OpenBao auth tokens and policies | Translate approved authorization intent to Falcone IAM/workload contracts | Do not import broad root tokens or assume policy syntax/lease equivalence |
| Active dynamic credentials/leases | Drain, revoke/reissue or explicitly retain temporary source ownership | Provider state is external; duplicate issuance and stale renewals must be fenced |
| Transit ciphertext and non-exportable keys | Controlled source decrypt/re-encrypt where permitted, fresh-key rotation, or bounded retained bridge | Non-exportable keys cannot be magically exported; retain source until dependent ciphertext/operations are migrated |
| PKI roots/intermediates and issued certificates | Preserve trust chain or separately plan CA rollover | Old trust/revocation/validity obligations may outlive API cutover |
| ESO/direct Vault consumers | Qualified narrow compatibility endpoint/provider adapter or rewrite | A KV path match does not prove auth/renewal/metadata behavior |
| Kubernetes bootstrap Secrets | Adopt existing expected names/keys; validate ownership and source transition | Avoid regenerating working credentials or letting two controllers overwrite one object |
| Webhook/flow-trigger keys | Dedicated versioned lifecycle migration with matching ciphertext and backups | No in-place replacement of key bytes under old ciphertext format |

## Dry-run and import

Produce sanitized counts, mappings, unsupported cases and effective authorization comparisons. Data transfer uses dedicated least-privilege identities, bounded batches, audited source access and encrypted destination writes. Equal-value verification uses protected keyed digests or isolated consumer checks, not public hashes of guessable secrets. No production plaintext belongs in this repository, CI artifacts or a shared report.

For recoverable private keys, assess whether the source permits secure export and whether the destination format is compatible. Re-encrypting exported values does not automatically solve migration of active sessions, provider credentials or root trust. Keep keys/leases in a separate migration ledger.

## Shadow and cutover

Shadow metadata/authorization checks must not create, rotate or revoke real provider credentials twice. Use synthetic canaries for side-effecting operations. Each tenant/domain/consumer has one authoritative writer. Freeze writes briefly or use an ordered change capture with a final cutover revision, then fence old writes and switch routing/projectors.

Canary criteria cover write-only APIs, errors, IAM authorization, BYOK destination confinement, function projection/reload, workflow resumption/lineage, dynamic leases, rotation/ACK/revoke, bootstrap and restore. Verify the exact installed ESO and Kubernetes auth behavior where retained. A denied or missing destination read must not silently fall back to a broader source store.

The first-party IAM design still references OpenBao/KMS custody, workflow uses existing secret services and serverless has a proposed ESO-based trust boundary. Create reviewed consumer/chart changes under those repositories' rules; this planning publication does not amend their accepted decisions or execute production rollout.

## Rollback

Rollback must reconcile changes made after cutover: new values, rotated provider passwords, dropped roles, revoked tokens, destroyed versions and keys. An old database snapshot may contain now-invalid or previously revoked credentials. Define forward repair and the irreversible boundary for key destruction/CA changes before migration begins.

Prove rollback using a canary with post-cutover writes and rotations, not only an idle snapshot. Keep source recovery material protected for the approved window. Dual-write without fencing and reconciliation is not a rollback strategy.

## Retirement gates

Require parity for every in-use consumer/engine, independent security review, key custody sign-off, disaster recovery evidence, operating owners and no unresolved provider revocation. Retire old auth identities/routes and delivery ownership only after the rollback window and retention requirements. Non-exportable keys or unresolved historical ciphertext requiring OpenBao mean retirement is incomplete, even if normal KV reads have moved.

Full production removal is a separately authorized deployment action. Archive sanitized evidence and retain encrypted backups/keys according to approved policy; do not describe live deletion as proof that every historical copy has been erased.
