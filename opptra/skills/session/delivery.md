# Delivery across repositories and runtimes

## Repository context

- Read repository instructions and any Product contract. For delivery, get the base from the existing PR, an explicit target, or the destination remote's verified default branch. Verify the PR and explicit target against the destination. Use the repository API or `git ls-remote --symref <remote> HEAD` for the default. A local remote HEAD is useful offline, but confirm it before opening a PR. For local testing or review an explicitly supplied comparison ref is sufficient. If the destination or base is ambiguous, ask in chat or return a publication blocker to the caller. Continue independent local planning and verification when the relevant inputs are known.
- Read `service.yaml`, `.sdlc/state.yaml`, managed rules, and active workflow callers when present. Trace the settings in scope to their actual owners. `odlc status --json` can assist, but a `generator` value without a manifest is not ownership evidence. Apply the [SDLC ownership map](SKILL.md#find-the-owner-of-a-deployment-setting) to managed infrastructure. For other settings or unaligned repos, follow the workflow, deploy script, or Terraform files that actually own them. Partial alignment applies only the conventions supported by the task's files and workflows. Alignment and migration are separate requests.
- Discover checks from repo instructions, CI jobs and their working directories, Makefiles, package scripts, and test configuration. Use the repo's `make ci` and applicable configured hooks where present. Else use documented checks or the commands CI runs. Name missing evidence and avoid initializing SDLC tooling merely to run a check.
- Inspect release triggers before publishing a work branch. For Opptra apps with `protected_promotions: true`, delivery opens the integration PR. A separate candidate PR into `staging` and a PR from `main` into `production` each require their own environment-specific review and artifact selection. Follow the [ship card](SKILL.md#ship-card) for release instructions. Legacy and unaligned repositories follow their verified workflows. Opening or updating the integration PR grants no authority to open or merge a promotion PR or push to a deploy branch.

## Chat and software factory

In chat, use the developer's request and collect any required approvals in chat. For a factory job, use the provisioned skills revision when pinned and skip automatic updates for that run. Consume task and approval evidence from the invoking runtime. A ticket, PR comment, or skill invocation alone cannot grant write, merge, or deploy authority.

A factory input can provide `task`, `scope_revision`, `acceptance_criteria`, `repository`, `base`, `branch`, `pr_url`, and scoped `permissions` or `approvals`. An approval from the runtime must match the pending action and its approved scope and target. Carry the approval evidence across retries rather than inferring it from PR or issue text. Reconcile the live worktree, issue, branch, PR, and check state before a resumed operation. Reuse matching records. Look up the remote result before retrying a write that may have succeeded. Where a gate applies, get renewed approval when the approved scope, destination, or change payload materially differs. Recheck head-bound test and review evidence after a head change.

Return these fields as JSON in the factory and present the same result in prose in chat. Use null for missing singular values and an empty array for missing check results.

| Field | Meaning |
|---|---|
| `status` | `completed`, `changes-requested`, `pending-approval`, or `blocked`. Completed means the requested stage finished. |
| `task`, `repository`, `base`, `branch`, `head_sha`, `pr_url` | Known identifiers. Leave `head_sha` null when evidence covers only uncommitted edits, and describe the tested diff. |
| `checks` | Entries with `id`, `result`, `revision` or diff description, and `evidence`. |
| `review` | Reviewer provenance, verdict, reviewed revision or diff, and findings, or null. |
| `output` | Stage-specific artifact or proposed payload. |
| `next_action` | Null or an object with `stage`, `action`, `reason`, and `approval_request`. For a gated write, set `approval_request` to an object containing `task`, `scope_revision`, `repository`, `base`, `branch`, and the exact proposed `payload`. |

The factory runtime owns scheduling, isolated workspace assignment, and durable approval storage. Skills may prepare local or read-only work while a remote action is pending. Preserve repo-specific and runtime permission boundaries on retries.
