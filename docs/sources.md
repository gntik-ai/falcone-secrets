# Sources and research evidence

Reviewed 2026-11-01. Primary project sources underpin the survey; proposed objectives, architecture and effort estimates are engineering judgments. Pin actual dependency releases and license files before implementation. No real secret values or deployment credentials were retrieved for this planning exercise.

## Falcone baseline

Source commit: [`ed04fe7269d32f3f3e3cbc434ab5168389153ed6`](https://github.com/gntik-ai/falcone/tree/ed04fe7269d32f3f3e3cbc434ab5168389153ed6).

| Source | Evidence |
|---|---|
| [Secret operations](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/docs-site/operations/secret-management.md) | Bootstrap/adoption, OpenBao/ESO, config.secretRefs and separate webhook-key contract |
| [Workspace-secret contract](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/docs/reference/architecture/workspace-secrets-console.md) | Write-only values, routes/statuses, metadata, role/tenant error ordering and runtime projection |
| [OpenBao client/store](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane/vault-secrets.mjs) | KV v2 path isolation, server-side resolution and Kubernetes-auth token lifecycle |
| [Inventory contract](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/internal-contracts/secrets/secret-inventory-v1.yaml) | Metadata domains, version compatibility fields and value exclusion |
| [Metadata contract](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/internal-contracts/secrets/secret-metadata-v1.yaml) | Existing metadata route and fields |
| [Audit contract](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/internal-contracts/secrets/secret-audit-event-v1.yaml) | Allowlisted audit fields and value/data exclusion |
| [Secret version state](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/provisioning-orchestrator/src/models/secret-version-state.mjs) | Active/grace/expired/revoked states and grace policy |
| [Rotation initiation](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/provisioning-orchestrator/src/actions/secret-rotation-initiate.mjs) | Ownership checks, version updates and backend side-effect boundaries |
| [Consumer acknowledgement](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/provisioning-orchestrator/src/actions/secret-consumer-ack.mjs) | Verified principal, consumer registration, tenant and version checks |
| [Function reference normalization](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane/function-secret-refs.mjs) | Value-free declarations and environment aliases |
| [Function secret remediation](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane/remediate-function-secrets.mjs) | Scope locking, deployment projection and stale revision cleanup |
| [BYOK confinement](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/docs/reference/architecture/byok-provider-secret-confinement.md) | Workspace and env references, endpoint SSRF controls and documented worker gap |
| [Provider credential broker](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane-executor/src/runtime/provider-credential-broker.mjs) | Token exchange and per-connection/version in-process token cache |
| [Workflow credential references](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/internal-contracts/src/flow-execution-credentials.mjs) | Opaque handles, run/attempt binding and platform credential-store ownership |
| [Flow-trigger encryption](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/apps/control-plane-executor/src/runtime/flow-trigger-secret-crypto.mjs) | Separate pre-existing key/ciphertext boundary |
| [Webhook key lifecycle](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/docs-site/operations/webhook-signing-key-lifecycle.md) | Independent custody/recovery, draft release status and qualification gates |
| [Audit sanitizer](https://github.com/gntik-ai/falcone/blob/ed04fe7269d32f3f3e3cbc434ab5168389153ed6/packages/secret-audit-handler/src/sanitizer.mjs) | Schema projection, value redaction and fail-closed validation |

## Sibling design baselines

- [IAM architecture at 7e3ad9f](https://github.com/gntik-ai/falcone-iam/blob/7e3ad9f772494a67d06674a2fea7081417dc7d3d/docs/architecture.md): custom identity/roles/federation, OpenBao/KMS custody proposal, independent integration boundary.
- [Workflow architecture at b26c6e7](https://github.com/gntik-ai/falcone-workflow/blob/b26c6e777211629f41ad3f251bf0059de8003219/docs/architecture.md): decided TypeScript engine, authoritative lineage and credential-reference requirements.
- [Serverless pool identity ADR at 0e41c67](https://github.com/gntik-ai/falcone-serverless/blob/0e41c6768e1eccf3ac85d22dbdd4914bac63760b/docs/adr/0006-pool-identity-and-openbao.md): proposed OpenBao/ESO host delivery, review gates and OCI-shim amendment; not an implemented authentication claim.

These repositories were read as integration references. Their decisions and files were not changed by this bootstrap.

## External primary sources

| Source | Use |
|---|---|
| [OpenBao repository](https://github.com/openbao/openbao), [KV v2](https://openbao.org/docs/secrets/kv/kv-v2/) | License/implementation scope, versioned KV and compare-and-swap behavior |
| [OpenBao seal/unseal](https://openbao.org/docs/concepts/seal/) | Independent root/unlock lifecycle and recovery considerations |
| [OpenBao leases](https://openbao.org/docs/concepts/lease/), [database engines](https://openbao.org/docs/secrets/databases/) | Dynamic credentials, renew/revoke and provider plugins |
| [OpenBao transit](https://openbao.org/docs/secrets/transit/), [audit](https://openbao.org/docs/audit/) | Managed crypto operations, key versions and audit boundaries |
| [Vault source/license](https://github.com/hashicorp/vault/blob/main/LICENSE) | Current source-available license distinction and feature-reference context |
| [Infisical repository/license](https://github.com/Infisical/infisical/blob/main/LICENSE), [secret management](https://infisical.com/platform/secrets-management) | Environment workflows, rotation/dynamic-secret concepts and edition boundaries |
| [Conjur README](https://github.com/cyberark/conjur/blob/master/README.md), [license](https://github.com/cyberark/conjur/blob/master/LICENSE.md) | Machine authorization, PostgreSQL architecture and license intake |
| [Barbican docs](https://docs.openstack.org/barbican/latest/), [backends](https://docs.openstack.org/barbican/latest/install/barbican-backend.html) | Pluggable custody and HSM/secret-store distinction |
| [SOPS docs](https://getsops.io/docs/), [key groups](https://getsops.io/docs/usage/identities/key-groups/) | Encrypted configuration and wrapping patterns |
| [ESO provider docs](https://external-secrets.io/main/provider/webhook/), [repository](https://github.com/external-secrets/external-secrets) | Existing operator delivery and potential provider adapter boundary |
| [Sealed Secrets repository](https://github.com/bitnami/sealed-secrets) | Scoped encrypted GitOps delivery and controller/key prerequisites |
| [step-ca concepts](https://smallstep.com/docs/step-ca/certificate-authority-core-concepts/), [provisioners](https://smallstep.com/docs/step-ca/provisioners/), [source](https://github.com/smallstep/certificates) | Optional certificate/SSH issuer architecture |
| [Confidant repository](https://github.com/lyft/confidant) | Historical envelope/credential model; archived status verified through repository metadata |

Upstream links may evolve. Version pinning and dependency/feature/license verification are explicit backlog requirements; a survey is not authorization to copy every referenced implementation.
