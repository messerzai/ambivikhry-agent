# Ambivikhry personalization / biosignal design — 2026-10-04

## Status

DESIGN-ONLY / EXPERIMENTAL / NOT PROMOTED.

This document proposes a future personalization layer. It does not grant new permissions, enable sensors, collect biometric data, modify Policy Gate, or change human-approval requirements.

## Research basis

Recent public work suggests a promising architecture for personalized wearable agents: perception, personalization, and reasoning can be separated; physiological evidence can be combined with context and user history; structured memory can adapt without per-user model retraining. See Affective Agent (arXiv:2609.12322, September 2026). Recent wearable-intelligence surveys also emphasize lifelong personalized memory, proactive assistance, multimodal sensing, resource constraints, and user regulation. Privacy research argues that personalization privacy must be evaluated at the whole-system level, including information flows, indirect leakage, interaction trajectories, and privacy/utility trade-offs.

## Proposed architecture

`Sensors -> local signal quality -> feature extraction -> state hypotheses -> personalized memory -> reasoning -> intervention policy -> user feedback`

Candidate input classes:

- heart rate / HRV and pulse-derived features;
- sleep/activity/context signals;
- optional respiration and other wearable signals;
- optional EEG-derived features when a compatible device and explicit consent exist;
- conversation, interaction, task history, preferences and corrections.

Raw biosignals should remain local by default. The personalization layer should preferentially consume derived features plus provenance, confidence, timestamp and signal-quality metadata. Raw streams should only leave the device after an explicit, purpose-specific authorization.

## Personalization model

Do not create a single permanent "psychological profile". Maintain a versioned personal state with separate layers:

1. stable preferences;
2. learned interaction preferences;
3. temporary context/state;
4. physiological baselines;
5. current uncertainty;
6. user-confirmed facts;
7. hypotheses awaiting confirmation.

Every inferred state must carry `source`, `confidence`, `time_window`, `signal_quality`, and `expiry/revalidation` metadata.

## Resonance / impulse layer

The future agent may choose among intervention modes rather than always producing information:

- information;
- question;
- short reflection;
- breathing/pause prompt;
- task prioritization;
- motivational impulse;
- silence/no intervention.

Interventions should be evaluated for usefulness and annoyance, with user-adjustable intensity. Physiological signals must never be treated as direct proof of emotion, intent, diagnosis, truthfulness, or personality. A signal can be evidence for a hypothesis, not a verdict.

## EEG-specific rule

EEG should be treated as a high-sensitivity input. The design must separate signal processing from interpretation. No automatic claim such as "the EEG shows that you feel X" is allowed. The system should report uncertainty and distinguish measured signal features from downstream hypotheses. Medical or diagnostic use is out of scope for this evolution branch unless a separately approved, human-reviewed project explicitly establishes that scope.

## Privacy / authority gates

The personalization layer must be fail-closed:

- no sensor activation without explicit user consent and a visible purpose;
- no silent background collection;
- per-sensor permissions;
- per-purpose permissions;
- revocation and deletion controls;
- local-first processing where feasible;
- provenance on every sensitive feature;
- no sharing with tools or external services outside the authorized purpose;
- no inference of sensitive characteristics from biometrics;
- no autonomous changes to Policy Gate or tool permissions;
- no human-approval bypass.

These requirements are aligned with the broader principle that personalization must not override higher-level safety/privacy constraints and that sensitive tool calls require explicit scope and provenance.

## Evaluation plan

Before any implementation is promoted, evaluate:

1. personalization gain over a non-personalized baseline;
2. calibration of physiological-state hypotheses;
3. false-positive / false-intervention rate;
4. intervention usefulness;
5. intervention annoyance / interruption cost;
6. cross-session retention;
7. robustness to missing/noisy sensors;
8. sensor-distribution shift;
9. privacy leakage / unauthorized inference;
10. consent and revocation compliance;
11. adversarial prompt attempts to exfiltrate biosignals;
12. holdout-user generalization without exposing holdout data to optimization.

A candidate must not be promoted merely because it predicts a physiological or affective label better. The target is better *user outcomes and calibration under constraints*.

## Candidate research experiments

A. Compare conversation-only personalization vs conversation + wearable features.

B. Compare raw-signal access vs derived-feature-only access; prefer the minimum-data condition if utility is statistically comparable.

C. Test whether explicit user corrections improve personalization more reliably than passive inference.

D. Test intervention timing: proactive vs user-triggered vs silence.

E. Test whether physiological features improve information selection rather than merely emotional labeling.

F. Test graceful degradation when sensors disappear, become noisy, or are deliberately spoofed.

## Rejected for now

- always-on biometric collection;
- unrestricted raw EEG upload;
- hidden emotion/personality inference;
- autonomous medical interpretation;
- biometric-based persuasion or manipulation;
- using physiology to override explicit user instructions;
- creating or expanding tool permissions to reach sensors;
- changing Policy Gate to enable personalization;
- automatic promotion based on biometric classification accuracy alone.

## Lineage

Parent: `d2f4d45440e2f3ae27a1831c9da97a371a2d3654`
Branch: `experiment/ambivikhry-personalization-biometrics-2026-10-04`
Main remains untouched.

## Decision

KEEP AS RESEARCH HYPOTHESIS. No production integration until an independently evaluated prototype demonstrates measurable personalization benefit while preserving consent, provenance, privacy, calibration and authority boundaries.
