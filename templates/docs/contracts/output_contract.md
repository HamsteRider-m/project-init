# Output Contract

## Final Output Boundary

Define exactly where accepted output is written and what file types are allowed.

Required final files:

- <!-- file 1 -->
- <!-- file 2 -->

Final output must not contain logs, caches, intermediate JSON, temporary files, credentials, or machine-only artifacts unless this contract explicitly allows them.

## Work Artifact Boundary

Define where engineering artifacts live.

Expected work artifacts:

- <!-- artifact 1 -->
- <!-- artifact 2 -->

## Traceability

Each accepted output must record enough source information to reproduce or audit it:

- source input;
- generation time or version;
- command/tool/script when relevant;
- validation result.

## Rejection Rules

Reject output when:

- required files are missing;
- disallowed file types appear in final output;
- traceability is missing;
- output was produced by a downgraded or non-production path without explicit approval;
- validation evidence is absent or failing.
