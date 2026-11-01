# ADR 0002 — Owner acceptance of all open-point proposals

Date: 2026-11-01. Status: **accepted**. Decision authority: Falcone project owner, in the project conversation.

## Decision

The owner stated: “about falcone secrets open points i accept all the proposal without any change”. All nineteen working proposals in [the original open-points table](../open-questions.md) are accepted as written, including their conditions and qualification gates. ADR 0001 is the accepted architectural baseline. No feature, threshold or acceptance criterion is changed by this record.

This accepts TypeScript/Node.js alignment subject to component benchmarking, Falcone-owned policy and interfaces, scoped host-mediated delivery where specified, independent root custody as the preferred profile, the proposed 30-second new-resolution freshness bound, single-region HA initially, configurable retention, measured sizing, and fenced migration with consumer verification. Optional alternatives are not simultaneous implementation commitments.

## Consequences

Implementers can proceed with the SEC backlog without requesting acceptance of these proposals again. Implementation issues remain open until their acceptance criteria have evidence. This decision is not a production deployment or OpenBao-retirement approval.

Some original proposals deliberately specify an investigation or defer an external fact: deployed versions/engines, available KMS/HSM, actual workload volumes, exact cluster builds, named on-call/custody owners and license selection. Those tasks remain part of the accepted plan. No license, provider, certification, retention duration or person is invented by this acceptance. The operator-unlock fallback retains its original condition of separate operator acceptance if it becomes necessary.

The accepted secrets boundary also applies to Falcone S3 integration: secrets owns recoverable provider credentials and key operations; S3 owns objects and storage bindings; IAM owns identities and policy. Root-custody recovery must remain independent of storage that requires those same keys to unlock.

## Backlog traceability

SEC-CON tracks contract/component qualification; SEC-BOOT tracks root trust and bootstrap. All other SEC epics inherit this accepted baseline, with their existing requirements, dependencies and completion criteria unchanged.
