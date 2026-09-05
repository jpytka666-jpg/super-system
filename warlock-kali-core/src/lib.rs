// super-system-header-v1
// AUTHOR: M. SZUL
// CREATED: 2026-09-05 Europe/London
// PURPOSE: Deterministic scope and policy boundary for the Warlock/Kali authorized security lab.

use serde::{Deserialize, Serialize};
use std::collections::BTreeSet;
use uuid::Uuid;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum Capability {
    ReadTarget,
    Fuzz,
    CrashReproduce,
    ProtocolNegativeTest,
    StaticAnalysis,
    ExploitabilityTriage,
    DestructiveLabTest,
    NetworkEgress,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum TargetKind {
    LocalProcess,
    LocalService,
    DisposableVm,
    Container,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct TargetSpec {
    pub target_id: String,
    pub kind: TargetKind,
    pub locator: String,
    pub disposable: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScopeManifest {
    pub scope_id: Uuid,
    pub owner: String,
    pub targets: Vec<TargetSpec>,
    pub allowed_capabilities: BTreeSet<Capability>,
}

impl ScopeManifest {
    pub fn target(&self, target_id: &str) -> Option<&TargetSpec> {
        self.targets.iter().find(|target| target.target_id == target_id)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionRequest {
    pub run_id: Uuid,
    pub scope_id: Uuid,
    pub target_id: String,
    pub capability: Capability,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Decision {
    Allow,
    Deny(DenyReason),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum DenyReason {
    ScopeMismatch,
    TargetNotDeclared,
    CapabilityNotAllowed,
    DestructiveRequiresDisposableTarget,
    NetworkEgressRequiresExplicitCapability,
}

#[derive(Debug, Default)]
pub struct PolicyEngine;

impl PolicyEngine {
    pub fn evaluate(&self, scope: &ScopeManifest, request: &ExecutionRequest) -> Decision {
        if request.scope_id != scope.scope_id {
            return Decision::Deny(DenyReason::ScopeMismatch);
        }

        let Some(target) = scope.target(&request.target_id) else {
            return Decision::Deny(DenyReason::TargetNotDeclared);
        };

        if !scope.allowed_capabilities.contains(&request.capability) {
            return Decision::Deny(DenyReason::CapabilityNotAllowed);
        }

        if request.capability == Capability::DestructiveLabTest && !target.disposable {
            return Decision::Deny(DenyReason::DestructiveRequiresDisposableTarget);
        }

        if request.capability == Capability::NetworkEgress
            && !scope.allowed_capabilities.contains(&Capability::NetworkEgress)
        {
            return Decision::Deny(DenyReason::NetworkEgressRequiresExplicitCapability);
        }

        Decision::Allow
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn scope() -> ScopeManifest {
        ScopeManifest {
            scope_id: Uuid::new_v4(),
            owner: "operator".into(),
            targets: vec![TargetSpec {
                target_id: "app-under-test".into(),
                kind: TargetKind::DisposableVm,
                locator: "lab://app-under-test".into(),
                disposable: true,
            }],
            allowed_capabilities: BTreeSet::from([
                Capability::ReadTarget,
                Capability::Fuzz,
                Capability::CrashReproduce,
                Capability::ExploitabilityTriage,
            ]),
        }
    }

    #[test]
    fn declared_target_and_capability_are_allowed() {
        let scope = scope();
        let request = ExecutionRequest {
            run_id: Uuid::new_v4(),
            scope_id: scope.scope_id,
            target_id: "app-under-test".into(),
            capability: Capability::Fuzz,
        };

        assert_eq!(PolicyEngine.evaluate(&scope, &request), Decision::Allow);
    }

    #[test]
    fn undeclared_target_fails_closed() {
        let scope = scope();
        let request = ExecutionRequest {
            run_id: Uuid::new_v4(),
            scope_id: scope.scope_id,
            target_id: "something-else".into(),
            capability: Capability::Fuzz,
        };

        assert_eq!(
            PolicyEngine.evaluate(&scope, &request),
            Decision::Deny(DenyReason::TargetNotDeclared)
        );
    }

    #[test]
    fn ungranted_capability_fails_closed() {
        let scope = scope();
        let request = ExecutionRequest {
            run_id: Uuid::new_v4(),
            scope_id: scope.scope_id,
            target_id: "app-under-test".into(),
            capability: Capability::NetworkEgress,
        };

        assert_eq!(
            PolicyEngine.evaluate(&scope, &request),
            Decision::Deny(DenyReason::CapabilityNotAllowed)
        );
    }

    #[test]
    fn destructive_test_requires_disposable_target() {
        let mut scope = scope();
        scope
            .allowed_capabilities
            .insert(Capability::DestructiveLabTest);
        scope.targets[0].disposable = false;

        let request = ExecutionRequest {
            run_id: Uuid::new_v4(),
            scope_id: scope.scope_id,
            target_id: "app-under-test".into(),
            capability: Capability::DestructiveLabTest,
        };

        assert_eq!(
            PolicyEngine.evaluate(&scope, &request),
            Decision::Deny(DenyReason::DestructiveRequiresDisposableTarget)
        );
    }
}
