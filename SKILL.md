---
name: genpark-personal-agent-cardiac-central-aortic-augmentation-index-pwa-skill
version: 1.0.0
description: Calculates central aortic Augmentation Pressure (AP), Augmentation Index (AIx, AIx@75), Reflection Time (Tr), and Subendocardial Viability Ratio (SEVR).
license: Apache-2.0
compatibility:
  python: ">=3.9"
  openclaw: ">=1.0.0"
  mcp: ">=1.0.0"
---

# Cardiac Central Aortic Augmentation Index (AIx) & Pulse Wave Analysis (PWA) Skill

A zero-dependency personal agent skill for evaluating central aortic wall stiffness, pulse wave reflection kinetics, and left ventricular late-systolic afterload via applanation tonometry pulse wave analysis.

## Features
- **Central Pressure Deconvolution**: Extracts central aortic pulse pressure ($PP$) and augmentation pressure ($AP = P_{\text{systolic}} - P_1$).
- **Augmentation Index (AIx & AIx@75)**: Computes heart-rate normalized augmentation index ($AIx@75 = AIx - 0.56 \times (75 - HR)$).
- **Reflection Transit Time ($T_r$)**: Measures arrival time of peripheral reflected wave to detect accelerated wave velocity.
- **Subendocardial Perfusion Viability**: Calculates the Buckberg Subendocardial Viability Ratio ($SEVR = DTI / STI \times 100\%$).

## MCP Server Integration
Exposes `evaluate_pwa` for autonomous cardiovascular screening and early vascular aging (EVA) monitoring.
