# Button

Buttons start or commit an action; one primary button per view, for the thing the page is for.

- **primary** (`action` fill, `on-action` text): the next step in a flow, "Approve and continue", "Write the PRD". Never two on one screen.
- **secondary** (default, `raised` with a `line-strong` border): everything else that does something.
- **quiet** (`action` text, no border): low-emphasis actions next to a primary, like "Request changes" or "Skip".
- **danger** (`error` border and text): destructive actions. Always confirm deleting a workspace, and say what will be lost.

Labels are verbs, sentence case, and say what happens: "Export as Docx", not "Export" when there are several formats, and never "Submit" or "OK".

Sizes: `md` (36px) by default, `lg` (44px) for the primary action on touch, `sm` (28px) only in dense tables. The focus ring is a 2px `action` outline with a 2px gap. Disabled buttons stay readable (`ink-muted` on `sunk`), but explain nearby why the action is unavailable.

The consumer provides the click handler and any loading state. While a skill runs, keep the button disabled and say what's happening in a live region elsewhere, not inside the button.
