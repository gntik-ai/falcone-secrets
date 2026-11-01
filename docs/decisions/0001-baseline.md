# ADR 0001 — Falcone-native secret custody and lifecycle

Date: 2026-11-01. Status: **proposed**. The owner requested a custom Falcone replacement and authorized the planning/backlog publication; technical profiles and production rollout still require qualification.

## Decision

Implement a Falcone-owned service for versioned encrypted values, scoped resolution, key operations, leases, rotation and consumer convergence. Preserve existing Falcone contracts. Use maintained crypto/identity libraries, PostgreSQL transactions, existing Kafka-compatible eventing and independently recoverable root custody. Initial language recommendation is TypeScript/Node.js for compatibility with current Falcone and IAM/workflow designs.

Keep user/machine identity, SAML/OIDC/LDAP/AD/SCIM and role policy in `falcone-iam`. Secrets is an enforcement and custody service, with a narrowly defined independent IAM bootstrap signing path. No synchronous dependency on workflow/serverless is allowed for unlock, signing, core resolution or emergency revocation.

## Rationale

Existing Falcone already supplies workspace APIs, reference contracts, rotation state, audit schemas and consumer protections. A generic replacement IAM or secret-console hierarchy would duplicate that product model. PostgreSQL can atomically persist encrypted values, state, audit acceptance and outbox intent; external providers still require reconciliation. Restricting baseline deployment to ordinary namespaced workloads respects the corporate OpenShift constraint.

The principal costs are security maintenance, root-key recovery, provider-specific revocation, rollout correctness and independent qualification. Lower external-service count does not eliminate those responsibilities.

## Alternatives and extensions

| Path | Scalability / ergonomics | Operational cost | Falcone compatibility and decision |
|---|---|---|---|
| Custom modular service with library crypto and independent key provider | Reuse JS contracts; replicate API/workers; benchmark audit and KMS limits | Own schema, crypto configuration, recovery and lifecycle correctness | Proposed target; protocol and custody qualification first |
| Custom Go core | Potentially simpler binary/concurrency and crypto-worker isolation; requires cross-language fixtures | Different contributor/tooling skills; memory still requires careful handling | Viable if team/runtime requirements justify it; not assumed inherently secure or faster |
| Falcone facade over OpenBao during migration | Fastest contract/consumer validation | Retains existing service, seal and upgrade work | Useful transitional phase; not the final requested dependency replacement |
| Embed or fork an OpenBao component | Could reuse mature behavior but internal APIs and MPL obligations need review | Large upstream merge/patch surface and possible retained complexity | Evaluate only for a concrete component; do not treat a renamed fork as a smaller architecture |
| External KMS/HSM root custody | Mature independent trust; network latency/rate limits matter | Additional provider availability, cost and custodian obligations | Preferred if available; cloud-neutral adapter and offline recovery evidence required |
| Offline operator unlock | Fewer external online dependencies | Manual restart/recovery, software-key exposure and custody burden | Alternative requiring explicit operator acceptance; no new secret-sharing scheme |
| Optional shared cache | Can lower repeated key/metadata work | Staleness, secret exposure and invalidation complexity | Add only after measurement with bounded freshness; no authoritative plaintext cache |
| Existing ESO / optional SOPS or Sealed Secrets | Fits established deployment/GitOps workflows | Controllers, CRDs or offline tooling and key recovery | Optional compatibility/delivery paths; native baseline cannot require new operators |
| Full PKI/SSH/cloud engines | Broader user value | Issuer trust, provider-specific APIs, expiry/revocation and recovery | Add only for required current usage or an explicit later epic; certificate custody is already included |
| Per-tenant database/key partitions | Stronger failure and access boundaries | More connections, providers and restore operations | Optional isolation tier when actual risk/capacity justifies it |

## Guarantees not inferred

No blanket Vault API/plugin compatibility, instant distributed revocation, exactly-once provider effects, perfect memory erasure or universal credential portability. No replacement of Falcone IAM or product quotas. No automatic adoption of enterprise-only/source-available code. These boundaries keep the custom service's behavior testable.
