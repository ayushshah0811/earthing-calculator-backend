import math
from app.constants import PI, MATERIAL_CONSTANTS, STANDARD


def calculate_earthing(data):
    ρ = data.earth_resistivity
    ISC = data.fault_current
    T = data.fault_clearing_time
    NP = data.number_of_pits

    WS = data.strip_width_mm / 1000
    TS = data.strip_thickness_mm / 1000
    LS = data.strip_length_m
    NS = data.number_of_strips

    material = data.strip_material.upper()
    K = MATERIAL_CONSTANTS[material]

    earthing_type = data.earthing_type

    # ======================================================
    # PART A: Heat Dissipation
    # ======================================================

    I_perm = (7.57 * 1000) / math.sqrt(ρ * T)
    required_area = ISC / I_perm

    # ---------- Electrode Area ----------
    if earthing_type == "pipe":
        r = data.rod_radius_m
        h = data.rod_length_m

        electrode_area = 2 * math.pi * r * (h + r) * NP

    elif earthing_type == "plate":
        Lp = data.plate_length_mm / 1000
        Wp = data.plate_width_mm / 1000
        Tp = data.plate_thickness_mm / 1000

        long_side_area = 2 * (Lp * Wp)
        thin_side_area = 4 * (Lp * Tp)
        plate_area_each = long_side_area + thin_side_area

        electrode_area = plate_area_each * NP

    else:
        raise ValueError("Invalid earthing type")

    # ---------- Strip Area ----------
    strip_area = (2 * (WS + TS) * LS) * NS
    net_area = electrode_area + strip_area

    heat_status = "Acceptable" if net_area > required_area else "Not Acceptable"

    # ======================================================
    # PART B: Strip Cross Section
    # ======================================================

    min_strip_area = (ISC * math.sqrt(T)) / K
    selected_strip_area = (data.strip_width_mm * data.strip_thickness_mm) * NS

    strip_status = (
        "Acceptable"
        if selected_strip_area > min_strip_area
        else "Not Acceptable"
    )

    # ======================================================
    # PART C: Earthing Resistance
    # ======================================================

    # ---------- Electrode Resistance ----------
    if earthing_type == "pipe":
        h = data.rod_length_m
        L_cm = h * 100
        D_cm = data.rod_diameter_mm / 10

        R_electrode_each = (
            (100 * ρ / (2 * PI * L_cm))
            * math.log((2 * L_cm) / D_cm)
        )

    elif earthing_type == "plate":
        Lp = data.plate_length_mm / 1000
        Wp = data.plate_width_mm / 1000

        plate_area = Lp * Wp
        R_electrode_each = (ρ / 4) * math.sqrt(PI / plate_area)

    R_electrode_parallel = R_electrode_each / NP

    # ---------- Strip Resistance ----------
    Ls_cm = LS * 100
    d_cm = data.strip_width_mm / 10

    R_strip_each = (
        (100 * ρ / (2 * PI * Ls_cm))
        * math.log((4 * Ls_cm) / d_cm)
    )
    R_strip_parallel = R_strip_each / NS

    # ---------- Net Resistance ----------
    net_resistance = (
        R_electrode_parallel * R_strip_parallel
    ) / (
        R_electrode_parallel + R_strip_parallel
    )

    resistance_status = (
        "Acceptable" if net_resistance < 4 else "Not Acceptable"
    )

    # ======================================================
    # OVERALL RESULT
    # ======================================================

    overall = (
        "PASS"
        if heat_status == strip_status == resistance_status == "Acceptable"
        else "FAIL"
    )

    return {
        "standard": STANDARD,
        "earthing_type": earthing_type.capitalize(),
        "summary": [
            {
                "description": "Net Heat Dissipation Area Available",
                "result": round(net_area, 2),
                "unit": "Sqmt",
                "condition": "Must be higher than required heat dissipation area",
                "remarks": heat_status,
            },
            {
                "description": "Minimum Cross Sectional Area Required for Strip",
                "result": round(min_strip_area, 2),
                "unit": "Sqmm",
                "condition": "Must be lower than selected earth strip",
                "remarks": strip_status,
            },
            {
                "description": "Net Earthing Resistance",
                "result": round(net_resistance, 2),
                "unit": "Ohm",
                "condition": "Preferably lower than 4 Ohm",
                "remarks": resistance_status,
            },
        ],
        "overall_status": overall,
    }
