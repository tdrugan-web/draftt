# CheckpointBar

The bar at the end of a flow step where the person reviews an artifact and either continues, approves, or asks for changes, matching the `review` and `approve` checkpoints in FLOW-SPEC.

- **approve**: a 2px `action` top rule. The primary button is "Approve and continue". Say what depends on the approval.
- **review**: a hairline top rule. The primary button is "Continue". Make clear nothing is locked.
- "Request changes" opens a revision request (a multiline TextField). It never discards the current version.
- Sticky at the bottom of the artifact view, never a modal. The person must be able to scroll and edit the artifact while the bar is visible.
- `none` checkpoints don't show a bar.
