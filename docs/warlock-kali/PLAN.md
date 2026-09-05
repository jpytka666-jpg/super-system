<!-- super-system-header-v1 -->
<!-- AUTHOR: M. SZUL -->
<!-- CREATED: 2026-09-05 Europe/London -->
<!-- PURPOSE: Implementation plan for Warlock/Kali isolated red-team subsystem. -->

# Warlock / Kali implementation plan

## Objective

Build a Rust-first, auditable red-team laboratory that can aggressively test operator-owned applications while remaining mechanically constrained to declared targets and disposable environments.

## Phase 0 — foundation

Status: STARTED on branch `feat/warlock-kali-lab-foundation`.

Deliverables:
- typed Scope Manifest;
- target allowlist and capability model;
- execution decision engine;
- audit/event envelope;
- worker request/response contracts;
- zero exploit logic in the control plane;
- tests proving fail-closed behavior.

Exit gate:
- an undeclared target cannot produce an executable worker request;
- network access defaults to denied;
- destructive capability defaults to denied;
- every allowed request contains scope/run/target provenance.

## Phase 1 — isolated campaign runner

Build a local worker launcher behind a trait boundary.

Preferred runtime path:
1. Linux/KVM host.
2. Firecracker microVM per campaign.
3. Jailer enabled.
4. No host credentials or writable host mounts.
5. Explicit CPU, memory, process and wall-clock limits.
6. Evidence-only output channel.

Initial worker types:
- source fuzz worker;
- binary fuzz worker;
- sanitizer crash collector;
- deterministic reproducer.

## Phase 2 — LibAFL integration

Add LibAFL as an adapter, not as policy.

Capabilities:
- seed corpus ingestion;
- mutation strategy selection;
- coverage feedback;
- crash/hang objective collection;
- multi-core scaling;
- optional QEMU adapter for binary-only targets.

Every fuzzer process receives a pre-authorized immutable WorkerRequest. It cannot ask the control plane to widen scope.

## Phase 3 — application test adapters

Adapters should translate an application boundary into fuzzable inputs:
- HTTP request structures;
- JSON/API schemas;
- file formats;
- IPC messages;
- parsers and codecs;
- CLI argument/input streams;
- protocol state machines.

Tag findings against OWASP ASVS/WSTG where appropriate.

## Phase 4 — finding pipeline

For each candidate failure:
1. hash and deduplicate;
2. reproduce in a fresh disposable environment;
3. capture stack/sanitizer evidence;
4. minimize input;
5. classify reliability;
6. classify security impact conservatively;
7. attach source/build/commit provenance;
8. emit a human-reviewable evidence bundle.

No candidate automatically becomes an authorization to perform a broader action.

## Phase 5 — Darkstar integration

Target architecture:

```text
AIONS / Darkstar
  -> Capability Gate
  -> Policy
  -> Orchestrator
  -> Warlock Provider
  -> Kali Lab Worker
  -> Evidence
  -> Event + Audit + Memory
```

Darkstar remains the authority. Warlock plans and coordinates adversarial test campaigns. Kali workers execute only the narrow pre-authorized test job.

## Phase 6 — advanced vulnerability research

Only after the containment and evidence pipeline are proven:
- coverage-guided structured fuzzing;
- differential testing;
- state-machine fuzzing;
- parser confusion testing;
- concurrency/race stress harnesses;
- fault injection;
- memory-safety exploitability triage inside the disposable target;
- regression corpus generation.

## Explicitly out of scope

- scanning arbitrary Internet targets;
- autonomous intrusion against third parties;
- persistence on external systems;
- credential theft;
- covert exfiltration;
- self-propagating payloads;
- automated weaponization for use outside the declared lab.

## First coding milestone

Create crate `warlock-kali-core` with:
- `ScopeManifest`;
- `TargetSpec`;
- `Capability`;
- `ExecutionRequest`;
- `Decision`;
- deterministic `PolicyEngine`;
- unit tests for fail-closed behavior.
