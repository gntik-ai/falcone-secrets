# Security model and qualification

This document defines target controls and evidence. It does not claim production readiness, compliance certification or that all reference-product features have been implemented.

## Threat boundaries

Protect against cross-tenant access, forged workload scope, database-only compromise, ciphertext substitution, stale grants, credential replay, compromised consumers, dependency failure and secret leakage through observability/history. Explicit residual boundaries include host/cluster administrators, an attacker controlling the authorized online secret process, and tenant code legitimately given plaintext.

IAM authentication is separate from permission to resolve a particular value or use a signing key. Separate metadata/list, write, resolve, rotate, revoke, destroy, key-use and key-admin actions. Administrators may manage metadata or replace a secret without receiving its previous value. Bind trusted gateway/workload identities and authoritative resource scope; do not trust header presence, arbitrary vault paths or guest-supplied tenant labels.

All four enterprise protocols mandated for `falcone-iam` remain IAM responsibilities. Directory/federation deprovisioning affects secret authorization through IAM revisions and workload grants; adding a second LDAP/SAML login database to secrets would create conflicting authority.

## Cryptography and exposure

- Use reviewed authenticated encryption and per-version data keys. Authenticate resource scope, purpose, version and algorithm metadata; reject tampering before returning plaintext.
- Keep root wrapping authority independently recoverable and outside the ciphertext database. Envelope encryption protects stored values from database-only access; it does not stop an authorized online process from decrypting.
- Scope keys and operations by purpose. Signing, decrypt, rewrap and key administration are different permissions. An IAM workload bootstrap identity cannot call a generic root signer or enumerate secrets.
- Qualify exact algorithms/providers and cryptographic policy. Do not implement custom ciphers, nonce schemes, threshold sharing or protocol signatures. No FIPS/HSM guarantee follows from using a familiar algorithm name.
- Use TLS with certificate validation and explicit endpoint allowlists where needed. Metadata discovery and provider requests must not become SSRF routes. Preserve BYOK destination policy before attaching credentials.
- No plaintext in database value columns, WAL, outbox, audit, traces, application histories, backups, manifests, command-line arguments or diagnostic snapshots. Ciphertext/metadata may themselves be sensitive and require scoped access.
- Node/GC and copied buffers limit guaranteed zeroization. Bound plaintext lifetime and cache sizes, suppress core dumps/body tracing and document software-key memory exposure. A restricted container cannot guarantee protection from its host administrator.

## Revocation is not byte recall

| Action | Guarantee to implement | What it does not guarantee |
|---|---|---|
| Deny further secret resolution | New reads fail after the documented IAM freshness bound | A previously returned password disappears from a process |
| Delete a live secret/version | No new resolution from the live store under that reference | Physical erasure from all backups or copies |
| Update a projected Kubernetes Secret | New desired value is delivered to the API object | Running environment variables change automatically |
| Receive consumer ACK | Registered workload reports a particular adoption stage | Untrusted code erased every old copy |
| Expire a lease record | New authorized renewal/use through the service is denied | External DB/S3/broker credentials are unusable without backend enforcement |
| Revoke a provider credential | Verified backend invalidation under its supported semantics | Every already-authenticated connection or already-delivered object is recalled |
| Rewrap encryption keys | Wrapped key material now depends on the new wrapping key | Prior compromised credentials become safe or old stolen backups become undecryptable |

Proposed online authorization freshness is at most 30 seconds from authoritative IAM change to denied new resolve/renew, using invalidation plus leases that fail closed when stale. High-risk key administration requires a current decision. Measure external directory detection and provider revocation separately; no universal 30-second backend invalidation claim is made.

## Audit integrity

Persist an allowlisted audit intent before value release and final/unknown outcome afterward. Commit security mutations with audit acceptance and outbox intent. If required durable audit acceptance is unavailable, deny the sensitive operation; a Kafka outage may be tolerated with bounded durable backlog. Never log full upstream error bodies or values merely to diagnose a failed rotation.

Current secret event schemas permit paths/names; those can contain sensitive free text. Validate names, sanitize text and restrict audit access. Export checks apply per tenant. Use protected independent audit anchoring/retention if administrator-tamper detection is required: a hash chain stored only in the same writable database is insufficient by itself.

## Adversarial qualification

| Threat | Required evidence |
|---|---|
| Cross-tenant reference or encoded-path escape | Tests with duplicate names, malformed encoding, forged ownership and unauthorized pagination/counts |
| Ciphertext/key substitution | Wrong AAD, scope, algorithm, version and modified ciphertext all fail authentication |
| Confused deputy / forged consumer ACK | Registered principal, tenant, version and permitted purpose must match |
| Stale authorization or replay | Expired attempts, revoked grants, restored old state and duplicate provider jobs cannot regain access |
| Secret leakage | Canary values absent from responses where forbidden, logs, traces, manifests, history, errors and exports |
| Bootstrap takeover or signing abuse | One-time initialization, independent workload trust, exact IAM key-purpose restriction and no broad escalation |
| External side-effect ambiguity | Crash/timeout tests across provider activation, DB commit, delivery and revocation; unresolved results remain visible |
| Noisy neighbor / denial of service | Bounded requests, crypto concurrency, tenant limits and provider timeouts under approved quota ownership |
| Lost key / corrupt backup | Isolated paired-key restore, missing-key failure and no automatic reinitialization over old data |

Independent security review must cover the configured service, adapters and deployment, followed by owned remediation of findings. The team must confirm cryptographic constraints, custody policy and privacy retention; this plan assigns no compliance badge.
