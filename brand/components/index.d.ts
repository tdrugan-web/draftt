import type * as React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** primary: once per view, the thing the page is for. secondary: default. quiet: low-emphasis, text-like. danger: destructive. */
  variant?: "primary" | "secondary" | "quiet" | "danger";
  /** sm 28px, md 36px, lg 44px (use lg for primary actions on touch). */
  size?: "sm" | "md" | "lg";
}
export declare function Button(props: ButtonProps): React.ReactElement;

export interface TextFieldProps extends React.InputHTMLAttributes<HTMLInputElement & HTMLTextAreaElement> {
  /** Always visible. Never use the placeholder as the label. */
  label: string;
  /** One line under the label, before the input. */
  hint?: string;
  /** Shown under the input with an icon. Sets aria-invalid. */
  error?: string;
  /** Adds "(optional)" after the label. Mark optional fields, not required ones. */
  optional?: boolean;
  multiline?: boolean;
  rows?: number;
}
export declare function TextField(props: TextFieldProps): React.ReactElement;

export interface EvidenceTagProps {
  kind: "evidence" | "assumption" | "synthetic";
  /** Show the word after the letter. Use on first use in a document. */
  spelled?: boolean;
  /** Where the evidence came from, shown after the tag, for example "Interview 3". */
  source?: string;
  className?: string;
}
export declare function EvidenceTag(props: EvidenceTagProps): React.ReactElement;

export interface ArtifactLabelProps {
  label: "ai-generated" | "synthetic" | "assumption-heavy" | "evidence-backed" | "needs-validation";
  className?: string;
}
export declare function ArtifactLabel(props: ArtifactLabelProps): React.ReactElement;

export interface HighlightProps {
  children?: React.ReactNode;
  className?: string;
}
export declare function Highlight(props: HighlightProps): React.ReactElement;

export interface ArtifactCardProps {
  title: string;
  /** Artifact type from docs/ARTIFACT-TYPES.md, shown in mono, for example "prd". */
  type: string;
  /** Team terminology for the type, for example "Product brief". Falls back to type. */
  typeLabel?: string;
  status?: "draft" | "approved";
  labels?: ArtifactLabelProps["label"][];
  confidence?: "high" | "medium" | "low";
  openQuestions?: number;
  /** Producing skill, from the artifact footer. */
  skill?: string;
  version?: number;
  href?: string;
  /** A one or two line excerpt. */
  children?: React.ReactNode;
  className?: string;
}
export declare function ArtifactCard(props: ArtifactCardProps): React.ReactElement;

export interface FlowRailStep {
  id?: string;
  title: string;
  status?: "done" | "current" | "upcoming" | "skipped" | "blocked";
  /** Replaces the default status text, for example "Approved v2". */
  note?: string;
}
export interface FlowRailProps {
  steps: FlowRailStep[];
  /** The flow's title, for example "Idea to PRD". */
  title?: string;
  /** Accessible name for the nav landmark. Default "Flow progress". */
  label?: string;
  className?: string;
}
export declare function FlowRail(props: FlowRailProps): React.ReactElement;

export interface CheckpointBarProps {
  /** review: continue any time. approve: later steps read the approved version. Matches FLOW-SPEC checkpoints. */
  kind?: "review" | "approve";
  title?: string;
  hint?: string;
  continueLabel?: string;
  reviseLabel?: string;
  onContinue?: () => void;
  onRevise?: () => void;
  className?: string;
}
export declare function CheckpointBar(props: CheckpointBarProps): React.ReactElement;

declare global {
  interface Window {
    Draftt: {
      Button: typeof Button;
      TextField: typeof TextField;
      EvidenceTag: typeof EvidenceTag;
      ArtifactLabel: typeof ArtifactLabel;
      Highlight: typeof Highlight;
      ArtifactCard: typeof ArtifactCard;
      FlowRail: typeof FlowRail;
      CheckpointBar: typeof CheckpointBar;
    };
  }
}
