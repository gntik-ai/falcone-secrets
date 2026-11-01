# Comparative reference survey

Research date: 2026-11-01. This is a representative set of secret servers and complementary tools, not an exhaustive inventory. Architectural scaling models are not benchmark results. Features in commercial editions are not automatically available in the referenced OSS artifact.

## Platforms and complementary projects

| Reference | Features and extensibility | Scaling/operating model | What Falcone should take; limitations |
|---|---|---|---|
| [OpenBao](https://openbao.org/docs/) — current baseline | Versioned KV/CAS, auth/policies, leases, dynamic database credentials, transit, PKI, audit and engine plugins | HA service with configured durable storage, seal custody and coordinated lifecycle work | Principal behavior reference: key lifecycle, bounded leases and separate engines. Current Falcone uses a subset; exact deployed engines require inventory |
| [Vault](https://github.com/hashicorp/vault) | Similar engine/auth boundaries, response wrapping, credential lifecycle and cryptographic services; broad integrations | HA control/storage and external trust dependencies; edition affects topology/features | Valuable behavioral reference. Current code is BSL source-available, not assumed open source or freely embeddable; older releases have release-specific terms |
| [Infisical](https://github.com/Infisical/infisical) | Project/environment secrets, developer tooling, sync, rotations and dynamic-secret capabilities across editions | API/control services, database and background work; edition/configuration matters | Adopt usable environment workflows, rotation visibility and scoped machines. Map to Falcone tenant/workspace rather than create a second project hierarchy; verify exact OSS feature locations |
| [Conjur OSS](https://github.com/cyberark/conjur) | Machine identity, policy-based access, secret storage, authenticators and integration points | Application service backed by PostgreSQL; deployment/replica features require version qualification | Adopt explicit machine/resource authorization. Falcone IAM already owns identities/roles, so avoid duplicating that authority |
| [OpenStack Barbican](https://docs.openstack.org/barbican/latest/) | Secret/key/certificate management, API and pluggable secret-store/crypto backends including HSM integration | API/workers plus storage, integrated with OpenStack identity/operations | Adopt custody-provider abstraction and certificate boundaries. Running a complete OpenStack-oriented control plane would be excessive for Falcone |
| [SOPS](https://getsops.io/docs/) | Encrypted structured files, KMS/age-backed wrapping and key groups | Offline/CLI workflow; no online secret-service control plane | Optional encrypted configuration/import artifact pattern. It does not provide online authorization, dynamic leases or consumer revocation |
| [External Secrets Operator](https://external-secrets.io/main/provider/webhook/) | Provider adapters and reconciliation into Kubernetes Secrets; configurable refresh/delivery | Kubernetes controller with CRDs and provider credentials | Preserve compatibility where already approved. It is a delivery mechanism, not the encryption authority; cannot be a mandatory new install in restricted OpenShift |
| [Sealed Secrets](https://github.com/bitnami/sealed-secrets) | Public-key sealing for namespace/name-scoped Kubernetes delivery; controller decrypts | Cluster controller/key lifecycle and CRDs | Optional GitOps pattern. It adds controller prerequisites and Kubernetes plaintext Secret exposure; does not replace online leases or provider rotation |
| [step-ca](https://smallstep.com/docs/step-ca/certificate-authority-core-concepts/) | X.509/SSH certificate authority, provisioners, lifecycle and integration interfaces | Network CA with persistent state and key-provider dependencies | Reference for optional PKI/SSH engines. Certificate issuance is a separate trust and operational commitment, not a default consequence of storing TLS keys |
| [Confidant](https://github.com/lyft/confidant) — historical | Application identity, encrypted credential storage and KMS-backed envelope design | Service plus external cloud custody/data dependencies | Useful envelope/reference pattern only. Repository is archived at review time; do not choose it as a maintained new runtime dependency |

## License and maintenance intake

Checked upstream repository metadata/license files: OpenBao and SOPS use MPL-2.0; Barbican, ESO, Sealed Secrets and step-ca report Apache-2.0; Conjur's LICENSE.md specifies LGPL-3.0. Infisical's root license distinguishes MIT-covered code from `ee/` content. Current Vault LICENSE specifies BSL terms and a version-dependent future change license. Confidant reports Apache-2.0 and is archived. Pin exact release/license files before reuse; this is an inventory, not a legal compatibility opinion or the Falcone repository's license choice.

## Feature selection

| Pattern | References | Falcone implementation direction | Epics |
|---|---|---|---|
| Versioning, CAS and distinct deletion semantics | OpenBao | Internal immutable versions with strict existing public write-only contracts | KV |
| Custody separated from encrypted data | OpenBao, Barbican, historical Confidant | Envelope encryption and independent root provider; explicit recovery profiles | KEY, BOOT |
| Machine authorization | Conjur, OpenBao, Infisical | Falcone IAM decisions and per-attempt workload context | AUTH, DEL |
| Dynamic leases and backend revocation | OpenBao, Vault, Infisical | Durable lease state, capability declarations and orphan reconciliation | DYN, ROT |
| Secret propagation visibility | Infisical, ESO | Authenticated loaded/validated ACKs beyond mere delivery | ROT, DEL |
| Encryption/signing as scoped operations | OpenBao, Vault | Purpose-bound signing and context-bound transit, qualified with IAM | SIG |
| Encrypted configuration delivery | SOPS, Sealed Secrets | Optional tools; baseline stays operator-free and namespaced | DEL, OPS |
| Certificate issuance | Barbican, step-ca | Store/deliver existing certificates now; optional issuer adapter after qualification | SIG |

A custom Falcone service offers precise product contracts and less duplicated identity/configuration. It also transfers responsibility for key recovery, authorization, provider side effects, audit durability, patching and incident response to Falcone maintainers. The [ADR](decisions/0001-baseline.md) compares implementation alternatives.
