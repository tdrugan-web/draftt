# TextField

A labeled text input or text area, with an optional hint and error, for the few things a flow truly needs to ask.

- The label is always visible and says what to type in plain language. The placeholder is an example, never the label.
- Use `hint` for format or "how much is enough" ("A sentence or two is enough"). Draftt asks for as little as possible, so most fields should be `optional`, and say so.
- Errors say what went wrong and how to fix it, in one sentence, and appear after the person leaves the field or submits, never on each keystroke. The field gets a 2px `error` border and `aria-invalid`; the message is tied to the input with `aria-describedby`.
- Use `multiline` for ideas, notes, and revision requests. Let it grow; don't cap length unless a skill needs it.
- API keys: `type="password"`, never echo the key back after saving. Show only its last four characters.

The consumer provides value, onChange, and validation.
