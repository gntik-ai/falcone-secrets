# Bootstrap, sealing and independent recovery

The central architecture risk is circular trust: IAM needs signing/federation secrets, while secret access normally requires IAM authorization. The database credential or key used to unlock secrets cannot itself be available only after secrets is unlocked.

## Required trust roots

| Material | Initial custody | Runtime use |
|---|---|---|
| Root wrapping authority | Existing external KMS/HSM using independent workload identity, or an approved offline operator-unlock profile | Unlocks wrapping hierarchy; no dependency on an IAM-issued session |
| Secrets database startup credential | Independently provisioned bootstrap channel or approved database workload identity | Limited to the service's own database; future rotation uses a tested reconnect handoff |
| TLS server identity and bootstrap trust | Approved platform certificate/identity mechanism | Secures startup endpoints before ordinary IAM authentication works |
| IAM bootstrap workload identity | Operator-pre-enrolled mTLS identity or qualified independent equivalent | Exact permitted IAM signing/key operation only, no tenant-secret enumeration |
| Recovery credentials/material | Separate named custodians and protected backups | Time-limited emergency access and restoration, never a tenant API |

Do not store the only unlock key beside the ciphertext or depend on OpenBao auto-unseal after claiming OpenBao retirement. A transit seal backed by another still-required OpenBao would retain that dependency. Kubernetes Secrets may transport approved startup material, but they are not an HSM and do not protect against the administrators who can read them.

## Startup sequence

1. The installer provides approved database access, TLS trust and root-provider identity. First initialization is an atomic one-time procedure, with no default admin password or permanent general-purpose root token.
2. The service connects to its dedicated database and obtains wrapping capability under the selected custody profile. It stays sealed/unready for value operations if unlock fails; liveness does not force an endless restart loop.
3. The independently authenticated IAM workload obtains only its approved signing/key capability. Its credential cannot call generic secret read, create users or alter tenant policy. The signing adapter restricts exact key/purpose and validates the permitted request shape; key authentication alone must not create an unrestricted signing oracle.
4. IAM starts, publishes its expected issuer/JWKS and decision interface. Normal user/workload resolution now requires current IAM permission. Bootstrap trust remains a separately managed narrow capability for future restart, not an emergency policy bypass.
5. Projection and provider workers reconcile persisted operations. Core unlock, signing, authorization and audit acceptance do not require Kafka, workflow or serverless availability.

A delegated signing operation is only viable if the selected IAM library supports it. If private key export is needed, use a separately approved encrypted delivery path and state that key material exists in the IAM process. Never label exported keys non-exportable. Fail closed if neither qualified integration works.

## Custody profiles

**Preferred managed profile:** an external KMS or network HSM independent of Falcone IAM and this database. Qualify provider authentication, algorithms, key policies, availability, export restrictions, backup/recovery and rate limits. No specific cloud provider is assumed. Remote KMS/HSM availability is a prerequisite to choose this profile, not an existing fact.

**Operator-unlock alternative:** a vetted cryptographic wrapper and protected offline key material supplied through an authenticated recovery/unlock procedure. This trades automation and availability for fewer external runtime dependencies and exposes software keys in process memory. Custodians, transport, ephemeral handling, replica unlock, backup and loss procedures must be approved. Threshold custody, if needed, uses qualified tooling; this project does not invent Shamir or a new key-sharing protocol.

Development may use synthetic local keys. Production configuration must reject development bypasses and clearly identify its actual custody profile. Never generate a new root automatically when expected key material is missing: that can make the existing database unreadable and conceal a failed restore.

## Recovery acceptance

Restore ciphertext/metadata and matching retained wrapping keys in an isolated environment with provider egress and normal resolution disabled. Reconcile IAM security epochs, lease expiries, provider credential state and tombstones before enabling traffic. A database snapshot can contain credentials revoked after the snapshot; replaying it cannot be treated as authorization to use them.

Practice total restart with IAM unavailable, loss of one replica, KMS outage, failed key rotation, expired bootstrap identity and missing historical KEK. Separate key loss from ciphertext loss: permanent loss of required decryption material may be unrecoverable. A recovery design must not promise a hidden bypass for cryptography.

The existing platform webhook and flow-trigger encryption keys need their own paired database/key recovery. Their migration is independent of unlocking this service and must preserve each established lifecycle contract.
