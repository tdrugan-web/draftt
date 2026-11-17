# FlowRail

The progress rail for a flow: every step in order, with done, current, upcoming, skipped, and waiting-for-approval states.

- One rail per flow, on the left on wide screens and collapsed into a "Step 3 of 4" header on narrow ones.
- Step titles come from the flow YAML and start with a verb ("Frame the problem").
- Each state has words as well as a dot style, so the rail works without color and in a screen reader. The current step is marked with `aria-current="step"`.
- `blocked` means the step is waiting for an approval checkpoint above it. Say what it's waiting for in `note`.
- Branch steps show only the option that ran. Parallel steps show as one step with the parallel step's title.
- Past steps are links back to their artifacts; future steps are not clickable.
