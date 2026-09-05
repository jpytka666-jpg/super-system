<!-- super-system-header-v1 -->
<!-- AUTHOR: M. SZUL -->
<!-- CREATED: 2026-09-05 Europe/London -->
<!-- PURPOSE: Research foundation for Warlock/Kali authorized security testing lab. -->

# Warlock / Kali research foundation

## Mission

Warlock/Kali is an **authorized adversarial testing subsystem** for software owned by or explicitly placed under test by the operator. It should behave aggressively *inside a declared lab scope*, while the control plane remains deterministic, auditable and unable to expand scope by itself.

The design goal is not a general-purpose intrusion bot. The goal is a high-throughput vulnerability discovery and exploitability-validation laboratory for newly developed applications, libraries, services and protocol implementations.

## Research conclusions

### 1. Fuzzing core: LibAFL

Current LibAFL 0.16.x is a strong match because it is Rust-first, composable and supports multiple instrumentation backends. Relevant capabilities include SanitizerCoverage, Frida, QEMU user/system modes and multi-core/multi-machine scaling through LLMP.

Use LibAFL as the long-term engine abstraction rather than hard-coding one fuzzer.

Reference:
- https://docs.rs/libafl/latest/libafl/
- https://docs.rs/libafl_qemu/latest/libafl_qemu/

### 2. Application-security test taxonomy: OWASP ASVS + WSTG

Use OWASP ASVS 5.0.0 as the verification requirements catalogue and WSTG as the dynamic testing taxonomy. They provide a stable way to label findings and coverage without tying the system to a single scanner.

References:
- https://owasp.org/www-project-application-security-verification-standard/
- https://owasp.org/www-project-web-security-testing-guide/latest/

### 3. Isolation boundary: Firecracker-class microVMs

The execution environment must assume test workloads can be hostile. Firecracker explicitly treats guest execution as potentially malicious and combines KVM isolation with seccomp, namespaces, cgroups and privilege dropping through its jailer.

For Warlock/Kali this implies:
- disposable microVM per campaign or target class;
- no host filesystem mount by default;
- no ambient credentials;
- explicit egress policy;
- resource ceilings;
- immutable base image + ephemeral writable layer;
- evidence copied out through a narrow channel only.

Reference:
- https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md

## Threat model

Assume all of the following can be hostile:
- target process;
- test corpus;
- crash artifact;
- malformed protocol response;
- generated input;
- debugger output;
- dynamically loaded target component.

Therefore no discovery worker is trusted with policy decisions.

## Trust split

```text
Operator
   |
   v
Scope Manifest --------------+
   |                          |
   v                          v
Warlock Control         Audit Journal
   |
   +--> Policy Gate
   |      |
   |      +--> deny / allow / approval-required
   |
   v
Kali Worker Controller
   |
   v
Disposable Isolation Boundary
   |
   +--> fuzz target
   +--> sanitizer/instrumentation
   +--> protocol tester
   +--> crash reproducer
   +--> exploitability triage
   |
   v
Evidence Bundle
```

## Non-negotiable invariants

1. Every run has an immutable `scope_id` and `run_id`.
2. A target must be declared before execution.
3. Workers cannot add targets to their own scope.
4. Network egress is deny-by-default.
5. Credentials are never inherited from the host shell.
6. Exploitability analysis is performed only against the declared lab target.
7. Findings preserve provenance: target build, commit, harness, corpus, seed, environment and crash hash.
8. Destructive actions require an explicit lab capability and disposable target.
9. A worker result is evidence, not authorization for the next action.
10. The operator can stop a campaign centrally and the worker must fail closed.

## Initial capability families

Safe foundation capabilities to implement first:
- source-aware fuzz campaign orchestration;
- binary fuzzing through an adapter boundary;
- sanitizer crash ingestion;
- deterministic crash deduplication;
- reproducibility scoring;
- protocol grammar mutation;
- HTTP/API negative testing;
- ASVS/WSTG coverage tagging;
- SBOM/dependency inventory ingestion;
- static-analysis result normalization;
- exploitability triage inside the lab;
- evidence packaging and audit.

## Deferred capabilities

Do not implement in the foundation stage:
- public-network target discovery;
- autonomous lateral movement;
- credential harvesting;
- persistence mechanisms;
- stealth/evasion mechanisms;
- self-propagation;
- unrestricted shell execution outside the lab boundary.

These are intentionally outside the architecture because they do not improve authorized application testing and destroy the containment model.
