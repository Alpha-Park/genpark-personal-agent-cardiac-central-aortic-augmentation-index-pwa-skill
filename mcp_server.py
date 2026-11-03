"""
MCP Server for Cardiac Central Aortic Augmentation Index (AIx) & Pulse Wave Analysis (PWA).
Exposes tools for arterial stiffness and myocardial workload evaluation.
"""

import json
from typing import Dict, Any, Optional
from client import CentralAorticAugmentationIndexClient


def handle_evaluate_pwa(params: Dict[str, Any]) -> Dict[str, Any]:
    aortic_systolic_bp_mmhg = float(params.get("aortic_systolic_bp_mmhg", 115.0))
    aortic_diastolic_bp_mmhg = float(params.get("aortic_diastolic_bp_mmhg", 75.0))
    inflection_pressure_mmhg = float(params.get("inflection_pressure_mmhg", 105.0))
    reflection_time_tr_ms = float(params.get("reflection_time_tr_ms", 140.0))
    heart_rate_bpm = float(params.get("heart_rate_bpm", 72.0))
    diastolic_time_integral_dti = float(params.get("diastolic_time_integral_dti", 2200.0))
    systolic_time_integral_sti = float(params.get("systolic_time_integral_sti", 1500.0))

    client = CentralAorticAugmentationIndexClient()
    return client.evaluate_pwa(
        aortic_systolic_bp_mmhg=aortic_systolic_bp_mmhg,
        aortic_diastolic_bp_mmhg=aortic_diastolic_bp_mmhg,
        inflection_pressure_mmhg=inflection_pressure_mmhg,
        reflection_time_tr_ms=reflection_time_tr_ms,
        heart_rate_bpm=heart_rate_bpm,
        diastolic_time_integral_dti=diastolic_time_integral_dti,
        systolic_time_integral_sti=systolic_time_integral_sti
    )


TOOLS = {
    "evaluate_pwa": {
        "description": "Calculates central aortic Augmentation Pressure (AP), Augmentation Index (AIx and AIx@75), Reflection Time (Tr), and Subendocardial Viability Ratio (SEVR).",
        "parameters": {
            "type": "object",
            "properties": {
                "aortic_systolic_bp_mmhg": {
                    "type": "number",
                    "description": "Central aortic systolic blood pressure in mmHg (e.g. 115.0)."
                },
                "aortic_diastolic_bp_mmhg": {
                    "type": "number",
                    "description": "Central aortic diastolic blood pressure in mmHg (e.g. 75.0)."
                },
                "inflection_pressure_mmhg": {
                    "type": "number",
                    "description": "Central pressure at first inflection point P1 in mmHg (e.g. 105.0)."
                },
                "reflection_time_tr_ms": {
                    "type": "number",
                    "description": "Pulse wave transit time from foot to inflection point Tr in milliseconds (e.g. 140.0)."
                },
                "heart_rate_bpm": {
                    "type": "number",
                    "description": "Heart rate in beats per minute, default 72.0."
                },
                "diastolic_time_integral_dti": {
                    "type": "number",
                    "description": "Diastolic pressure-time area (DTI), default 2200.0."
                },
                "systolic_time_integral_sti": {
                    "type": "number",
                    "description": "Systolic pressure-time area (STI), default 1500.0."
                }
            },
            "required": ["aortic_systolic_bp_mmhg", "aortic_diastolic_bp_mmhg", "inflection_pressure_mmhg", "reflection_time_tr_ms"]
        },
        "handler": handle_evaluate_pwa
    }
}


def process_request(request_str: str) -> str:
    try:
        req = json.loads(request_str)
        method = req.get("method")
        req_id = req.get("id")

        if method == "tools/list":
            tools_list = [
                {
                    "name": name,
                    "description": spec["description"],
                    "inputSchema": spec["parameters"]
                }
                for name, spec in TOOLS.items()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name not in TOOLS:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                })

            result = TOOLS[tool_name]["handler"](args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            })

        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": f"Unsupported method '{method}'"}
            })

    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        if line.strip():
            print(process_request(line))
            sys.stdout.flush()
