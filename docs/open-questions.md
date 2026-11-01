# Accepted proposals and remaining qualification evidence

On 2026-11-01, the project owner accepted every proposal below without changes. These are now the approved working decisions. See [ADR 0002](decisions/0002-owner-acceptance.md). The original proposals are preserved verbatim in the table; conditional alternatives remain conditional. Environment inventories, measurements, provider availability and named operational owners still require evidence at their existing gates; acceptance does not invent those facts.

| Original question / evidence to collect | Accepted proposal | Qualification gate |
|---|---|---|
| Is TypeScript/Node.js preferred, or must the service be Go? | Align with current Falcone and IAM/workflow contracts; benchmark before commitment | P0 component ADR |
| Which open-source license should this repository use? | No project license selected; no upstream runtime source copied in this bootstrap | Before code distribution |
| Which OpenBao versions, mounts, auth methods, engines and direct clients are actually deployed? | Source inventory is a starting point; every in-use consumer gets a tested mapping | P0 compatibility |
| Are transit, PKI, SSH or cloud dynamic engines currently used? | Core includes needed signing/transit and credential adapters; full PKI/SSH/cloud breadth depends on inventory | Replacement scope |
| What independent KMS/HSM or root-custody service is available in corporate OpenShift? | Prefer existing independent provider; operator unlock is a separately approved alternative | **Before encryption/bootstrap implementation** |
| What bootstrap database access, TLS identity and recovery credentials can be supplied independently? | Narrow pre-enrolled workload/operator trust, no dependence on IAM-issued session or secrets-only storage | Bootstrap gate |
| Can the selected IAM implementation perform remote signing, or does it need protected private-key export? | Qualify actual library adapter; record memory/export exposure explicitly | IAM integration |
| Is ESO already installed and permitted in every target environment? | Preserve approved existing ESO, offer native namespaced resolution/projector path without a new operator | Deployment/delivery |
| What exact Kubernetes/OpenShift builds and workload permissions are approved? | Non-root arbitrary UID, no cluster-admin, privileged workload, mlock prerequisite or new CRDs | Deployment qualification |
| How many secret objects/versions, resolve requests, key operations, leases and rotations are expected? | Do not extrapolate from function/event throughput; measure each operation class | Sizing/SLO |
| May any tenant/runtime receive plaintext, or should operations always be host-mediated? | Preserve existing approved function behavior; native execution follows scoped host/shim design and narrow grants | Delivery/security |
| Which consumers can reload live, and which require restart or credential-session termination? | Track delivered/loaded/validated separately and define backend-specific revocation | Rotation qualification |
| What freshness and revocation delays are acceptable for each backend? | Proposed new-resolve bound 30 seconds; external providers and copied credentials have distinct limits | SLO/security |
| Must high availability span regions, and what key residency/FIPS/HSM constraints apply? | Single-region HA initially, qualified cryptographic module/custody profile | Architecture/security |
| What audit/backup retention, legal hold and destruction policy applies? | Configurable scope and retention; no claim that live delete erases historical copies | Production privacy/custody |
| How should the non-OpenBao webhook/flow-trigger key lifecycles move? | Dedicated adapters and paired-key recovery; preserve current runbook gates | Key migration |
| Which exact sibling-service revisions are target integration contracts? | Pinned designs in sources.md; reviewed handoffs required before deployment | Cross-repository rollout |
| Who owns runtime patches, root custody, on-call and independent review? | Roles in operations.md; actual people/rotations not assumed | Production readiness |
| What canary scope, write-freeze window and rollback retention are acceptable? | Fenced per-scope cutover and post-cutover reconciliation | P3 rollout |

The accepted root-custody preference is an existing independent KMS/HSM or custody provider. Its actual availability and integration must still be qualified before implementation. Operator unlock remains the separately approved alternative described in the original proposal; acceptance does not select it in place of the preferred path. Record implementation evidence against the affected SEC story IDs. No further confirmation of the proposals in this table is needed.
