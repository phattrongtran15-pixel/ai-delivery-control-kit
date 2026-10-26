# Browser Intelligence Behavioral Specification (PROPOSED, not deployed)
## Purpose
Nine user-mandated capabilities. Source-linked to SPEC.md C1–C9 and LikeC4 candidate elements. These scenarios define target behavior; passing a synthetic fixture is not full production acceptance.
## Requirements
### Requirement: R1 Multi-agent browser monitoring
The system SHALL expose independently observed status for each authorized browser actor without claiming synthetic clients are model-backed agents.

#### Scenario: 48-context monitor
- **GIVEN** 48 identifiable simulated actors complete synthetic browser actions
- **WHEN** a monitor is rendered
- **THEN** 48 distinct rows and real-outcome references are shown; users can distinguish synthetic from model-backed

### Requirement: R2 Isolated MCP sessions
The system SHALL keep session cookies and storage isolated across independent MCP clients even when they execute overlapping tasks.

#### Scenario: Cookie isolation
- **GIVEN** two or more MCP clients use distinct session identities
- **WHEN** clients navigate and inspect their sessions
- **THEN** no client observes another client's cookie; storage bleed causes a FAIL

### Requirement: R3 Learn verified browser procedures
The system SHALL store a newly successful browser method as a non-executable candidate until independent verification and authorized acceptance.

#### Scenario: Unapproved skill blocked
- **GIVEN** an observer has proposed a working action
- **WHEN** another actor searches for it before reviewer approval
- **THEN** the candidate cannot be executed as an approved skill

### Requirement: R4 Capture replay and verify actions
The system SHALL record a trace and verify the actual downstream outcome rather than accepting a browser-agent self-reported success.

#### Scenario: False success denied
- **GIVEN** an agent reports a successful click but independent state did not change
- **WHEN** the verifier reads server-side state
- **THEN** the skill is marked FAILED or UNKNOWN, never VERIFIED

### Requirement: R5 Safe fast action caching
The system SHALL reuse approved browser procedures from a fingerprint-keyed cache and reject stale or unauthorized matches.

#### Scenario: UI drift invalidates cache
- **GIVEN** an approved cached selector exists
- **WHEN** the page fingerprint, tenant or actor role changes
- **THEN** the cached action is not executed and cache metadata is invalidated

### Requirement: R6 Cross-agent searchable skill memory
The system SHALL allow separately authorized AI actors to find an approved skill by task while preserving version and source evidence.

#### Scenario: Cross-process search
- **GIVEN** an approved skill exists for a known task and site
- **WHEN** a different authorized process queries the catalog
- **THEN** the exact versioned skill is returned and unauthorized callers receive no executable procedure

### Requirement: R7 Checkpointed browser automation
The system SHALL produce retryable, evidence-backed workflow outcomes without unapproved side effects or duplicate protected actions.

#### Scenario: Crash-safe resume
- **GIVEN** a scoped automation job loses its worker midway
- **WHEN** a new authorized runner checks the checkpoint
- **THEN** it avoids duplicate protected writes and records a fresh completion receipt

### Requirement: R8 Share memory across AI hosts
The system SHALL distribute approved skill metadata across authorized Local and Cloud clients without transferring login cookies or token material.

#### Scenario: Cloud-local handoff
- **GIVEN** a local actor has an independently accepted skill
- **WHEN** a cloud actor retrieves it with verified identity and permissions
- **THEN** the same skill version is discoverable while session cookies remain private

### Requirement: R9 Versioned capability growth tree
The system SHALL expose the versioned ancestry, tests, and acceptance status of newly learned capabilities.

#### Scenario: Growth provenance
- **GIVEN** a previously accepted skill is improved and reviewed
- **WHEN** the capability graph is regenerated
- **THEN** parent/child version links and evidence distinguish CANDIDATE from ACCEPTED
