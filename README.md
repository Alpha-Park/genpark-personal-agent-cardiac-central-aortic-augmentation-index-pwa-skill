# Cardiac Central Aortic Augmentation Index (AIx) & Pulse Wave Analysis (PWA) Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](requirements.txt)
[![Status: Production-Ready](https://img.shields.io/badge/status-production--ready-success.svg)](https://github.com/alphaparkinc)

A zero-dependency, mathematically rigorous personal agent skill that evaluates central aortic pulse wave reflections, arterial wall elasticity, and late-systolic cardiac afterload via applanation tonometry pulse wave analysis.

## Architecture

```mermaid
flowchart TD
    A[Radial/Carotid Applanation Tonometry] --> B[Generalized Transfer Function / PWA Waveform]
    B --> C[Identify Forward Peak P1 & Late Systolic Peak P2]
    C --> D[Compute Augmentation Pressure AP = P2 - P1 & AIx]
    D --> E[Normalize to Heart Rate 75 bpm AIx@75 & Measure Tr]
    E --> F[Vascular Aging & Subendocardial Perfusion Index SEVR]
```

## Quick Start

```python
from client import CentralAorticAugmentationIndexClient

client = CentralAorticAugmentationIndexClient()
result = client.evaluate_pwa(
    aortic_systolic_bp_mmhg=115.0,
    aortic_diastolic_bp_mmhg=75.0,
    inflection_pressure_mmhg=105.0,
    reflection_time_tr_ms=140.0,
    heart_rate_bpm=72.0
)
print("Augmentation Index AIx@75 (%):", result["wave_reflection_kinetics"]["aix_normalized_at_75bpm_pct"])
print("SEVR (%):", result["myocardial_perfusion"]["subendocardial_viability_ratio_sevr_pct"])
print("Stiffness Class:", result["vascular_stiffness_assessment"]["stiffness_classification"])
```

## License
Apache-2.0
