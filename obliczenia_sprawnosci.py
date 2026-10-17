#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ocena wpływu zawartości O2 w spalinach na sprawność kotła na pellet.
Metoda 1: wzór Siegerta (empiryczny, używany przez analizatory spalin)
Metoda 2: bilans cieplny spalin (model stechiometryczny pelletu)

Użycie:
  python3 obliczenia_sprawnosci.py
  python3 obliczenia_sprawnosci.py --o2-przed 18 --tg-przed 180 --o2-po 11 --tg-po 180 --ta 20
"""

import argparse


# ---------- Metoda 1: Siegert ----------
def siegert(O2: float, tg: float, ta: float, A1: float = 0.65, B: float = 0.0) -> float:
    """Zwraca stratę kominową qA [%] wg wzoru Siegerta (wariant tlenowy)."""
    return (tg - ta) * (A1 / (21.0 - O2) + B)


def lam(O2: float) -> float:
    """Współczynnik nadmiaru powietrza lambda."""
    return 21.0 / (21.0 - O2)


# ---------- Metoda 2: bilans cieplny ----------
# 1 kg pelletu: wilgotność 8%, popiół 0,5%, skład części palnej, wartość opałowa 17,0 MJ/kg
C, H, O, N, W, A = 0.4575, 0.0549, 0.398, 0.00275, 0.08, 0.005  # kg/kg paliwa
Wu = 17.0e3   # kJ/kg
Vm = 22.414   # nm3/kmol

nC = C / 12.011
nH = H / 1.008
nO = O / 15.999
O2_st = nC + nH / 4 - nO / 2  # kmol O2 / kg
V_O2_st = O2_st * Vm
V_air_st = V_O2_st / 0.21
V_CO2 = nC * Vm
V_H2O = (nH / 2 + W / 18.015) * Vm

# cp [kJ/(nm3 K)] w przedziale ok. 20-180 C
cp_dry, cp_H2O = 1.32, 1.494
hum = 0.008  # kg wody/kg suchego powietrza


def bilans_cieplny(O2: float, tg: float, ta: float):
    """Zwraca (lambda, V_dry [nm3/kg], strata [kJ/kg], qA [%], eta [%])."""
    L = lam(O2)
    V_dry = V_CO2 + 0.79 * V_air_st * L + 0.21 * V_air_st * (L - 1)
    V_w = V_H2O + hum * (V_air_st * L * 1.293) * 1.244
    q = (V_dry * cp_dry + V_w * cp_H2O) * (tg - ta)
    qA_pct = 100.0 * q / Wu
    return L, V_dry, q, qA_pct, 100.0 - qA_pct


def drukuj_tabele_domyslne(ta: float = 20.0, A1: float = 0.65, B: float = 0.0):
    print(f"=== Metoda 1: wzór Siegerta (A1={A1:.2f}; B={B:.3f} - pellet/drewno) ===")
    print("O2[%]  lambda  ", "  ".join(f"tg={tg}" for tg in (120, 150, 180, 210)))
    for O2 in (18.0, 11.0, 9.0, 6.0):
        row = [f"{100 - siegert(O2, tg, ta, A1, B):5.1f}%" for tg in (120, 150, 180, 210)]
        print(f"{O2:4.1f}   {lam(O2):4.2f}   " + "  ".join(row))
    print(f"(wartości = sprawność spalania netto 100-qA, temperatura powietrza {ta:.0f} °C)")
    print()
    print(
        "Delta sprawności 11% vs 18% O2:  ",
        [round(siegert(18, tg, ta, A1, B) - siegert(11, tg, ta, A1, B), 1) for tg in (120, 150, 180, 210)],
    )

    print("\n=== Metoda 2: bilans cieplny (tg=180 °C) ===")
    print(f"powietrze stechiometryczne: {V_air_st:.2f} nm3/kg ({V_air_st * 1.293:.2f} kg/kg)")
    print(f"CO2max (spaliny suche): {100 * V_CO2 / (V_CO2 + 0.79 * V_air_st):.1f} %")
    print("\nO2[%]  lam    spaliny suche  straty[kJ/kg]  qA[%]   eta_netto[%]")
    for O2 in (18.0, 11.0, 9.0, 6.0):
        L, V_dry, q, qA_pct, eta = bilans_cieplny(O2, 180.0, ta)
        print(f"{O2:4.1f}   {L:4.2f}   {V_dry:6.2f} nm3/kg   {q:7.0f}      {qA_pct:5.1f}    {eta:5.1f}")


def drukuj_porownanie(o2_a: float, tg_a: float, o2_b: float, tg_b: float, ta: float, a1: float, b: float):
    qa_a = siegert(o2_a, tg_a, ta, a1, b)
    qa_b = siegert(o2_b, tg_b, ta, a1, b)
    eta_a = 100.0 - qa_a
    eta_b = 100.0 - qa_b
    d_eta = eta_b - eta_a
    oszcz = (d_eta / eta_b * 100.0) if eta_b > 0 else 0.0

    print("\n=== Porównanie dwóch pomiarów (wzór Siegerta) ===")
    print(f"Przed: O2 = {o2_a:.1f} %, tg = {tg_a:.1f} °C -> lambda = {lam(o2_a):.2f}, qA = {qa_a:.1f} %, eta = {eta_a:.1f} %")
    print(f"Po:    O2 = {o2_b:.1f} %, tg = {tg_b:.1f} °C -> lambda = {lam(o2_b):.2f}, qA = {qa_b:.1f} %, eta = {eta_b:.1f} %")
    print(f"Zysk sprawności spalania: {d_eta:+.1f} p.p.")
    print(f"Szacunkowa oszczędność paliwa: {oszcz:.1f} %")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kalkulator strat kominowych i sprawności spalania kotła na pellet.")
    parser.add_argument("--o2-przed", type=float, default=None, help="O2 przed regulacją [%%]")
    parser.add_argument("--tg-przed", type=float, default=180.0, help="Temperatura spalin przed regulacją [°C]")
    parser.add_argument("--o2-po", type=float, default=None, help="O2 po regulacji [%%]")
    parser.add_argument("--tg-po", type=float, default=180.0, help="Temperatura spalin po regulacji [°C]")
    parser.add_argument("--ta", type=float, default=20.0, help="Temperatura powietrza do spalania [°C]")
    parser.add_argument("--a1", type=float, default=0.65, help="Współczynnik Siegerta A1 (domyślnie 0.65)")
    parser.add_argument("--b", type=float, default=0.0, help="Współczynnik Siegerta B (domyślnie 0.0)")
    args = parser.parse_args()

    drukuj_tabele_domyslne(ta=args.ta, A1=args.a1, B=args.b)
    if args.o2_przed is not None and args.o2_po is not None:
        drukuj_porownanie(args.o2_przed, args.tg_przed, args.o2_po, args.tg_po, args.ta, args.a1, args.b)
