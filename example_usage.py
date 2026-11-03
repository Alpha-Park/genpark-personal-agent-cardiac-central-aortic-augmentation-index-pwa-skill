"""
Example usage of Cardiac Central Aortic Augmentation Index (AIx) & Pulse Wave Analysis (PWA).
Demonstrates youthful compliant aorta vs accelerated vascular aging with premature wave reflection.
"""

from client import CentralAorticAugmentationIndexClient

def main():
    client = CentralAorticAugmentationIndexClient()

    print("=== Case 1: Healthy Elastic Aorta (Young Adult) ===")
    young_case = client.evaluate_pwa(
        aortic_systolic_bp_mmhg=110.0,
        aortic_diastolic_bp_mmhg=70.0,
        inflection_pressure_mmhg=104.0,
        reflection_time_tr_ms=145.0,
        heart_rate_bpm=68.0,
        diastolic_time_integral_dti=2400.0,
        systolic_time_integral_sti=1400.0
    )
    print("Hemodynamics:")
    print(f"  Pulse Pressure:    {young_case['central_pressures_mmhg']['central_pulse_pressure_mmhg']} mmHg")
    print(f"  Augmentation Pres: {young_case['central_pressures_mmhg']['augmentation_pressure_ap_mmhg']} mmHg")
    print(f"  AIx@75:            {young_case['wave_reflection_kinetics']['aix_normalized_at_75bpm_pct']} %")
    print(f"  SEVR (Buckberg):   {young_case['myocardial_perfusion']['subendocardial_viability_ratio_sevr_pct']} %")
    print(f"  Stiffness Class:   {young_case['vascular_stiffness_assessment']['stiffness_classification']}")

    print("\n=== Case 2: Early Vascular Aging / Arterial Stiffness ===")
    stiff_case = client.evaluate_pwa(
        aortic_systolic_bp_mmhg=142.0,
        aortic_diastolic_bp_mmhg=82.0,
        inflection_pressure_mmhg=118.0,
        reflection_time_tr_ms=115.0,
        heart_rate_bpm=78.0,
        diastolic_time_integral_dti=1800.0,
        systolic_time_integral_sti=1750.0
    )
    print("Hemodynamics:")
    print(f"  Pulse Pressure:    {stiff_case['central_pressures_mmhg']['central_pulse_pressure_mmhg']} mmHg")
    print(f"  Augmentation Pres: {stiff_case['central_pressures_mmhg']['augmentation_pressure_ap_mmhg']} mmHg")
    print(f"  AIx@75:            {stiff_case['wave_reflection_kinetics']['aix_normalized_at_75bpm_pct']} %")
    print(f"  SEVR (Buckberg):   {stiff_case['myocardial_perfusion']['subendocardial_viability_ratio_sevr_pct']} %")
    print(f"  Stiffness Class:   {stiff_case['vascular_stiffness_assessment']['stiffness_classification']}")
    print(f"  Pathophysiology:   {stiff_case['vascular_stiffness_assessment']['pathophysiology']}")

if __name__ == "__main__":
    main()
