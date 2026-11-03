"""
Cardiac Central Aortic Augmentation Index (AIx) & Pulse Wave Analysis (PWA) Client.
Zero-mock pure Python standard library implementation.
Calculates Augmentation Pressure (AP), Augmentation Index (AIx), Heart-Rate Corrected AIx@75,
Reflection Time (Tr), and Subendocardial Viability Ratio (SEVR / Buckberg Index).
"""

import math
from typing import Dict, Any, Optional


class CentralAorticAugmentationIndexClient:
    """
    Evaluates central aortic stiffness and late-systolic ventricular afterload via Pulse Wave Analysis:
    - AP (mmHg) = P_peak - P_inflection
    - AIx (%) = (AP / PP) * 100
    - AIx@75 (%) = AIx - 0.56 * (75 - HR)
    - Tr (ms): wave reflection transit time (foot to inflection point)
    - SEVR / Buckberg index (%): (DTI / STI) * 100
    """

    def __init__(self):
        pass

    def evaluate_pwa(
        self,
        aortic_systolic_bp_mmhg: float,
        aortic_diastolic_bp_mmhg: float,
        inflection_pressure_mmhg: float,
        reflection_time_tr_ms: float,
        heart_rate_bpm: Optional[float] = 72.0,
        diastolic_time_integral_dti: Optional[float] = 2200.0,
        systolic_time_integral_sti: Optional[float] = 1500.0
    ) -> Dict[str, Any]:
        """
        Calculates central hemodynamic pulse wave metrics.
        aortic_systolic_bp_mmhg: central aortic systolic pressure (e.g. 115 mmHg).
        aortic_diastolic_bp_mmhg: central aortic diastolic pressure (e.g. 75 mmHg).
        inflection_pressure_mmhg: pressure at the inflection point P1 (e.g. 105 mmHg).
        reflection_time_tr_ms: transit time to inflection point in ms (e.g. 140 ms).
        heart_rate_bpm: cardiac frequency in beats per minute (e.g. 72 bpm).
        """
        if aortic_systolic_bp_mmhg <= aortic_diastolic_bp_mmhg:
            raise ValueError("Aortic systolic pressure must exceed diastolic pressure.")
        if reflection_time_tr_ms <= 0:
            raise ValueError("Reflection time must be positive.")

        # Central pulse pressure (PP in mmHg)
        pp = aortic_systolic_bp_mmhg - aortic_diastolic_bp_mmhg

        # Augmentation pressure (AP in mmHg)
        ap = aortic_systolic_bp_mmhg - inflection_pressure_mmhg

        # Augmentation Index (AIx in %)
        aix_pct = (ap / pp) * 100.0

        # Heart-rate normalized AIx (AIx@75 in %)
        aix_at_75 = aix_pct - 0.56 * (75.0 - heart_rate_bpm)

        # Subendocardial Viability Ratio (SEVR %)
        sevr_pct = None
        if diastolic_time_integral_dti and systolic_time_integral_sti and systolic_time_integral_sti > 0:
            sevr_pct = round((diastolic_time_integral_dti / systolic_time_integral_sti) * 100.0, 1)

        # Clinical arterial elasticity classification (ESH/ESC Guidelines):
        # AIx@75 normal reference (age-dependent, < 25% in healthy adults < 50yo)
        # Elevated AIx@75 (> 30%): premature wave reflection, high arterial stiffness
        # Tr shortened (< 130 ms): high PWV, wave reflects early during systole
        if aix_at_75 > 32.0 or reflection_time_tr_ms < 125.0:
            stiffness_class = "Markedly Elevated Wave Reflection & Central Arterial Stiffness"
            clinical_risk = "Premature wave reflection augments central systolic afterload, increasing left ventricular myocardial oxygen demand and hypertrophy risk."
        elif aix_at_75 > 22.0 or reflection_time_tr_ms < 140.0:
            stiffness_class = "Mildly Accelerated Pulse Wave Reflection"
            clinical_risk = "Early vascular aging (EVA); subclinical increase in central pulse pressure."
        else:
            stiffness_class = "Preserved Central Elastic Compliance / Optimal Cushioning"
            clinical_risk = "Delayed wave reflection returns during diastole, enhancing coronary perfusion without elevating peak LV systolic workload."

        return {
            "status": "success",
            "central_pressures_mmhg": {
                "aortic_systolic_mmhg": round(aortic_systolic_bp_mmhg, 1),
                "aortic_diastolic_mmhg": round(aortic_diastolic_bp_mmhg, 1),
                "central_pulse_pressure_mmhg": round(pp, 1),
                "inflection_pressure_p1_mmhg": round(inflection_pressure_mmhg, 1),
                "augmentation_pressure_ap_mmhg": round(ap, 1)
            },
            "wave_reflection_kinetics": {
                "augmentation_index_aix_pct": round(aix_pct, 1),
                "aix_normalized_at_75bpm_pct": round(aix_at_75, 1),
                "reflection_time_tr_ms": round(reflection_time_tr_ms, 1),
                "heart_rate_bpm": heart_rate_bpm
            },
            "myocardial_perfusion": {
                "subendocardial_viability_ratio_sevr_pct": sevr_pct,
                "sevr_status": "Adequate Subendocardial Perfusion (> 130%)" if (sevr_pct and sevr_pct >= 130.0) else "Borderline / Compromised Subendocardial Supply"
            },
            "vascular_stiffness_assessment": {
                "stiffness_classification": stiffness_class,
                "pathophysiology": clinical_risk
            }
        }
