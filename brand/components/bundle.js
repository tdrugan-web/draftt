/* @ds-bundle: {"format":4,"namespace":"Draftt","components":[{"name":"Button"},{"name":"TextField"},{"name":"EvidenceTag"},{"name":"ArtifactLabel"},{"name":"Highlight"},{"name":"ArtifactCard"},{"name":"FlowRail"},{"name":"CheckpointBar"}]} */
(function () {
  var React = window.React;
  var h = React.createElement;

  function cx() {
    var out = [];
    for (var i = 0; i < arguments.length; i++) if (arguments[i]) out.push(arguments[i]);
    return out.join(" ");
  }

  function omit(obj, keys) {
    var out = {};
    for (var k in obj) if (Object.prototype.hasOwnProperty.call(obj, k) && keys.indexOf(k) === -1) out[k] = obj[k];
    return out;
  }

  var uid = 0;
  function useId(prefix) {
    var ref = React.useRef(null);
    if (ref.current === null) ref.current = prefix + "-" + (++uid);
    return ref.current;
  }

  /* Button: primary (one per view), secondary, quiet, danger. */
  function Button(props) {
    var variant = props.variant || "secondary";
    var size = props.size || "md";
    var rest = omit(props, ["variant", "size", "className", "children", "type"]);
    return h("button", Object.assign({ type: props.type || "button" }, rest, {
      className: cx("dt-btn", "dt-btn-" + variant, "dt-btn-" + size, props.className)
    }), props.children);
  }

  /* TextField: label always visible, optional hint and error, single or multi-line. */
  function TextField(props) {
    var generatedId = useId("dt-field");
    var id = props.id || generatedId;
    var hintId = props.hint ? id + "-hint" : null;
    var errId = props.error ? id + "-error" : null;
    var describedBy = [hintId, errId].filter(Boolean).join(" ") || undefined;
    var rest = omit(props, ["label", "hint", "error", "multiline", "rows", "className", "id", "optional"]);
    var control = h(props.multiline ? "textarea" : "input", Object.assign({}, rest, {
      id: id,
      rows: props.multiline ? (props.rows || 4) : undefined,
      className: cx("dt-input", props.multiline && "dt-input-multi", props.error && "dt-input-invalid"),
      "aria-describedby": describedBy,
      "aria-invalid": props.error ? true : undefined
    }));
    return h("div", { className: cx("dt-field", props.className) },
      h("label", { className: "dt-field-label", htmlFor: id }, props.label,
        props.optional ? h("span", { className: "dt-field-optional" }, " (optional)") : null),
      props.hint ? h("p", { className: "dt-field-hint", id: hintId }, props.hint) : null,
      control,
      props.error ? h("p", { className: "dt-field-error", id: errId },
        h("span", { "aria-hidden": "true", className: "dt-field-error-icon" }, "!"), props.error) : null
    );
  }

  /* EvidenceTag: [E] evidence, [A] assumption, [S] synthetic. The letter is always shown. */
  var TAGS = {
    evidence: { letter: "E", word: "Evidence" },
    assumption: { letter: "A", word: "Assumption" },
    synthetic: { letter: "S", word: "Synthetic" }
  };
  function EvidenceTag(props) {
    var kind = TAGS[props.kind] ? props.kind : "assumption";
    var t = TAGS[kind];
    return h("span", { className: cx("dt-tag", "dt-tag-" + kind, props.className), title: props.source || t.word },
      h("span", { className: "dt-tag-letter", "aria-hidden": "true" }, "[" + t.letter + "]"),
      props.spelled ? h("span", { className: "dt-tag-word" }, t.word) : h("span", { className: "dt-sr" }, t.word),
      props.source ? h("span", { className: "dt-tag-source" }, props.source) : null
    );
  }

  /* ArtifactLabel: the labels from the artifact footer, shown on cards and headers. */
  var LABELS = {
    "ai-generated": "Drafted by Draftt",
    "synthetic": "Synthetic, not real users",
    "assumption-heavy": "Mostly assumptions",
    "evidence-backed": "Evidence-backed",
    "needs-validation": "Needs validation"
  };
  function ArtifactLabel(props) {
    var label = props.label;
    return h("span", { className: cx("dt-label", "dt-label-" + label, props.className) }, LABELS[label] || label);
  }

  /* Highlight: the highlighter. One per view. */
  function Highlight(props) {
    return h("mark", { className: cx("dt-hl", props.className) }, props.children);
  }

  /* ArtifactCard: a workspace artifact with its footer data surfaced. */
  var CONFIDENCE = { high: "High confidence", medium: "Medium confidence", low: "Low confidence" };
  function ArtifactCard(props) {
    var labels = props.labels || [];
    var status = props.status || "draft";
    var titleId = useId("dt-card");
    var Title = props.href ? "a" : "span";
    return h("article", { className: cx("dt-card", "dt-card-" + status, props.className), "aria-labelledby": titleId },
      h("header", { className: "dt-card-head" },
        h("span", { className: "dt-card-type" }, props.typeLabel || props.type),
        h("span", { className: cx("dt-card-status", "dt-card-status-" + status) }, status === "approved" ? "Approved" : "Draft")
      ),
      h("h3", { className: "dt-card-title", id: titleId },
        h(Title, props.href ? { href: props.href, className: "dt-card-link" } : {}, props.title)),
      props.children ? h("div", { className: "dt-card-body" }, props.children) : null,
      labels.length ? h("div", { className: "dt-card-labels" }, labels.map(function (l) { return h(ArtifactLabel, { key: l, label: l }); })) : null,
      h("footer", { className: "dt-card-foot" },
        h("span", { className: cx("dt-conf", "dt-conf-" + (props.confidence || "low")) },
          h("span", { className: "dt-conf-bars", "aria-hidden": "true" },
            h("i", null), h("i", null), h("i", null)),
          CONFIDENCE[props.confidence] || CONFIDENCE.low),
        typeof props.openQuestions === "number" ? h("span", { className: "dt-card-meta" },
          props.openQuestions === 1 ? "1 open question" : props.openQuestions + " open questions") : null,
        props.skill ? h("code", { className: "dt-card-skill" }, props.skill + (props.version ? " v" + props.version : "")) : null
      )
    );
  }

  /* FlowRail: progress through a flow. Ordered list, current step marked with aria-current. */
  var STEP_TEXT = { done: "Done", current: "Current step", upcoming: "Not started", skipped: "Skipped", blocked: "Waiting for approval" };
  function FlowRail(props) {
    var steps = props.steps || [];
    return h("nav", { className: cx("dt-rail", props.className), "aria-label": props.label || "Flow progress" },
      props.title ? h("p", { className: "dt-rail-title" }, props.title) : null,
      h("ol", { className: "dt-rail-list" }, steps.map(function (s, i) {
        var status = s.status || "upcoming";
        return h("li", { key: s.id || i, className: cx("dt-rail-step", "dt-rail-" + status), "aria-current": status === "current" ? "step" : undefined },
          h("span", { className: "dt-rail-dot", "aria-hidden": "true" }, status === "done" ? "✓" : String(i + 1)),
          h("span", { className: "dt-rail-text" },
            h("span", { className: "dt-rail-name" }, s.title),
            h("span", { className: "dt-rail-state" }, s.note || STEP_TEXT[status]))
        );
      }))
    );
  }

  /* CheckpointBar: the review or approve moment at the end of a flow step. */
  function CheckpointBar(props) {
    var kind = props.kind || "review";
    var approve = kind === "approve";
    return h("section", { className: cx("dt-check", "dt-check-" + kind, props.className), "aria-label": approve ? "Approval checkpoint" : "Review checkpoint" },
      h("div", { className: "dt-check-text" },
        h("p", { className: "dt-check-title" }, props.title || (approve ? "Approve to continue" : "Review before moving on")),
        h("p", { className: "dt-check-hint" }, props.hint || (approve
          ? "Later steps build on the approved version. You can still edit it after."
          : "Edit anything, or continue. Nothing later is locked to this version."))
      ),
      h("div", { className: "dt-check-actions" },
        h(Button, { variant: "quiet", onClick: props.onRevise }, props.reviseLabel || "Request changes"),
        h(Button, { variant: "primary", onClick: props.onContinue }, props.continueLabel || (approve ? "Approve and continue" : "Continue"))
      )
    );
  }

  window.Draftt = Object.assign(window.Draftt || {}, {
    Button: Button,
    TextField: TextField,
    EvidenceTag: EvidenceTag,
    ArtifactLabel: ArtifactLabel,
    Highlight: Highlight,
    ArtifactCard: ArtifactCard,
    FlowRail: FlowRail,
    CheckpointBar: CheckpointBar
  });
})();
