# Scope and observed baseline

## Goal and compatibility

Build a custom Falcone service replacing OpenBao's required roles. Preserve Falcone product APIs, URLs, metadata shapes, error behavior, secret references and authorization semantics. Use vetted cryptographic libraries and infrastructure key custody; a custom service does not require new cryptographic algorithms or an all-purpose Vault clone.

Raw Vault/OpenBao compatibility is limited to inventoried consumers. Existing ESO and direct KV clients need a tested adapter or narrow compatibility endpoint. A matching path or header is not evidence of full compatibility with Vault authentication, leases, plugins or policies.

## Source evidence

Examined Falcone commit `ed04fe7269d32f3f3e3cbc434ab5168389153ed6` and the pinned sibling designs listed in [sources](sources.md). Observed code, comments and proposals are distinguished from deployment verification.

| Observed behavior | Replacement implication |
|---|---|
| `vault-secrets.mjs` uses OpenBao KV v2 with Kubernetes authentication and scoped workspace paths | Preserve scoped storage and qualified auth/renewal behavior; replacing an endpoint alone is insufficient |
| Public workspace values are write-only; server-side deployment/provider resolution can read them | Maintain separate metadata/public and value/internal APIs; no new console reveal function |
| Workspace create/replace/delete have strict conflict and not-found semantics | Retain create-only POST, metadata-only PUT/GET, delete-all behavior and role/error precedence |
| Inventory uses platform, tenant, functions, gateway and iam domains, with fields such as `vaultVersion` and `vaultMount` | Preserve those fields through a compatibility mapper; names do not require a Vault backend |
| Rotation records active/grace/expired/revoked versions, grace windows and per-consumer state | Separate secret persistence, provider activation, consumer reload and actual revocation |
| Consumer ACK checks authenticated principal, registered consumer, tenant and version | Retain and test these checks; a caller cannot ACK for another workload |
| Function declarations store value-free names/env aliases; values project to owned Kubernetes Secrets via secretKeyRef | Preserve existing behavior during migration and explicit cleanup of stale/inline revisions |
| LLM/embedding BYOK uses workspace or operator-prefixed references plus endpoint SSRF controls | Keep reference confinement and destination checks together; distinguish fresh key reads from cached exchanged provider tokens |
| Flow execution uses opaque references, run/attempt binding and a protected platform credential table | Preserve lineage and no-secret-history guarantees; reference tokens are sensitive if bearer-like |
| Bootstrap first creates/adopts Kubernetes Secrets; OpenBao is seeded afterward and ESO reconciles them | Preserve first-install recovery and adopt existing credentials; avoid creating self-dependent bootstrap credentials |
| Platform webhook master key and executor-local flow-trigger encryption have separate contracts | Do not assume OpenBao owns every platform key; require independent migration and paired-key backup evidence |
| Secret audit has allowlisted fields, value redaction and tenant routing | New audit must preserve usable evidence without exporting secret material |

The BYOK documentation describes a workflow-worker binding gap; current code and deployed worker configuration must be checked during P0 rather than treating that historical note as current deployment fact. The webhook lifecycle runbook explicitly marks its release/verification status; a new design must not erase those gates.

## Exact public workspace anchor

Base route: `/v1/functions/workspaces/{workspaceId}/secrets`, with `/{secretName}` for individual operations. POST creates (201, duplicate 409); GET/list return metadata only; PUT replaces (200); DELETE removes all versions from live access (204, absent 404). Metadata includes `secretName`, legacy `name`, `tenantId`, `workspaceId`, `resolvedRefCount`, timestamps and optional non-secret description. No value or internal KV version is exposed.

Preserve the observed name pattern `^[a-z][a-z0-9_-]{0,62}$` and nonempty string value limit of 65535 characters; qualify exact Unicode/body-byte limits separately without changing the public contract accidentally. Tenant/workspace come from verified context and ownership, not the body. Existing cross-tenant 404 and own-tenant role-denial 403 ordering must remain covered by fixtures.

## Core and extension scope

Core target: encrypted versioned KV, metadata/inventory, reference resolution, IAM authorization, scoped workload identity, independently recoverable bootstrap, secret/credential rotation, consumer convergence, audit, backups, PostgreSQL lease adapter, scoped S3/event/provider adapters and purpose-bound signing/transit needed by Falcone integrations.

Certificate custody and existing TLS delivery are included. A full certificate authority, SSH CA, arbitrary cloud credential engines, general-purpose plugin ecosystem and every upstream Vault API are optional extensions unless inventory establishes current use. Any in-use engine must be implemented or explicitly retain a bridge; such a bridge postpones complete OpenBao retirement.

Prior corporate constraints carry forward: no assumed new operator/CRDs, cluster-admin, privileged runtime or sandbox support. Rough function/message counts are not secret-operation throughput. All product quota definitions remain in Falcone. Tenant code is untrusted and never runs inside the secret service.
