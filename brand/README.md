# Draftt

Draftt is an operating system for product and UX teams: Claude skills that take a product from idea to market, used inside Claude or on draftt.com. The brand is a well-kept draft. Paper, ink, a highlighter for what matters, and a visible trail of what's evidence and what's a guess. It should feel like a sharp colleague's working notes, not a dashboard.

## Principles

1. **Work in progress, shown honestly.** Drafts, revisions, and open questions are the product. Show versions and what changed instead of hiding them.
2. **Evidence is visible.** Every claim about users or markets carries its tag: [E] evidence, [A] assumption, [S] synthetic. The tags are the most distinctive thing in the interface. Treat them that way.
3. **One highlight per view.** The `highlight` marks the single thing a reader must not miss. Two highlights means neither matters.
4. **Paper, not plastic.** Hairlines, not shadows. Near-square corners. Flat fills.
5. **Plain language over framework jargon.** "What problem are we solving?" beats "Define your opportunity space."

## Voice and content

- Plain, specific, and short. Write like a senior PM explaining something to a smart colleague.
- Verbs first on buttons and steps, sentence case everywhere: "Frame the problem", "Approve PRD".
- No em dashes. Use commas, periods, colons, or parentheses.
- No hype words: powerful, seamless, effortless, revolutionary, supercharge, leverage.
- Name AI work for what it is. "Drafted by Draftt" on generated artifacts, "Synthetic" on anything from roleplay. Never call a synthetic persona "research".
- The product name is always lowercase in the wordmark (draftt) and title case in prose (Draftt). Two t's, always.

| Do | Don't |
|----|-------|
| Approve problem frame | Submit |
| 3 open questions | Some questions may need attention |
| Synthetic gut check (not real users) | AI user insights |
| Low confidence: mostly assumptions | Insights generated |

## Color

A neutral paper-and-ink system with one action color, one highlighter, and three evidence colors.

- **Ground:** `paper` for pages, `raised` for cards and editors (outlined in `line-strong`), `sunk` for rails, wells, and the artifact footer.
- **Text:** `ink` for primary text, `ink-muted` for secondary. Both pass 4.5:1 on every ground.
- **Action:** `action` for links, the primary button, and focus rings. Text on it is `on-action`. One primary button per view.
- **Highlight:** `highlight` sits behind `ink` text like a highlighter stroke, flush with the line, `radius-sm`. Never use it for buttons, banners, or backgrounds larger than a line.
- **Evidence tags:** `evidence`, `assumption`, and `synthetic` are close in lightness, so they are never the only signal. Every tag shows its letter ([E], [A], [S]) in `mono`, and the first use in a document spells the word out.
- **Error:** `error` with an icon and words. Draftt has no warning yellow, because yellow belongs to the highlighter.

Dark theme is not designed yet. Don't invent dark values in product code.

## Type

- **Newsreader** (display family) for page titles, artifact titles, and the wordmark. It gives artifacts the feel of a document, not an app. Use only the `display` and `title` styles.
- **IBM Plex Sans** (sans family) for everything in the interface and for artifact body text: `heading`, `body`, `body-sm`, `label`.
- **IBM Plex Mono** (mono family) for evidence tags, the artifact footer, skill names, and code.
- All three are free Google Fonts. Load weights 400, 500, and 600 for Plex Sans, 500 for Newsreader, 400 for Plex Mono.

## Space and shape

- A 4px base. Use `space-1` through `space-16`, nothing in between.
- `radius-sm` for tags, inputs, and the highlighter. `radius-md` for buttons, cards, and panels. `radius-full` only for progress dots and avatars.
- Separate surfaces with a 1px `line-strong` hairline. No drop shadows.

## Logo

The mark is two t's sharing one crossbar, like a typesetter's tt ligature. The second t is the revision. Use `draftt-mark.svg` (single ink, set with CSS `color`) almost everywhere, and `draftt-mark-color.svg` (ink plus `action`) on paper for the hero and favicon. The wordmark is a live-text placeholder until it's drawn as outlines. See `logos/README.md`.

## Iconography

Not designed yet. Until it is, use a 24px outline icon set with a 1.5px stroke and square line caps, drawn in `ink` or `ink-muted`. Icons never carry meaning alone.

## Accessibility

WCAG 2.2 AA is the floor. Every text token's usage note lists the grounds it passes on. Focus rings are a 2px `action` outline with a 2px `paper` gap. Targets are at least 24 by 24px, 44 by 44px for primary actions on touch.

## Components

Eight components cover the first website flows. They are React 18 components on `window.Draftt`, styled by `components/bundle.css` (guidelines in `components/<Name>.md`) with token variables only.

| Component | For |
|-----------|-----|
| Button | Actions. One primary per view |
| TextField | The few inputs a flow needs. Label always visible |
| EvidenceTag | [E], [A], [S] after every claim about users or markets |
| ArtifactLabel | Footer labels on cards and artifact headers. "Drafted by Draftt" always shows |
| Highlight | The one thing a reader must not miss |
| ArtifactCard | One artifact in a workspace, with status, labels, confidence, and open questions |
| FlowRail | Progress through a flow |
| CheckpointBar | The review or approve moment at the end of a step |

## Not built yet

Dark theme, icons, an outlined wordmark, and the workspace-level components (artifact view, revision diff, export menu, upload drop zone).
