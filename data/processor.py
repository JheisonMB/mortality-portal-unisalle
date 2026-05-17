"""All data aggregations for the dashboard charts.

Each function returns a DataFrame ready for the corresponding chart.
Results are cached after first call.
"""
from __future__ import annotations

from functools import lru_cache

import pandas as pd

from data.loader import death_codes, divipola, geodiv, mortality

# GRUPO_EDAD1 → label mapping (per DANE spec)
_AGE_LABELS: dict[int, str] = {
    **{k: "Mortalidad neonatal" for k in range(0, 5)},
    **{k: "Mortalidad infantil" for k in range(5, 7)},
    **{k: "Primera infancia" for k in range(7, 9)},
    **{k: "Niñez" for k in range(9, 11)},
    11: "Adolescencia",
    **{k: "Juventud" for k in range(12, 14)},
    **{k: "Adultez temprana" for k in range(14, 17)},
    **{k: "Adultez intermedia" for k in range(17, 20)},
    **{k: "Vejez" for k in range(20, 25)},
    **{k: "Longevidad / Centenarios" for k in range(25, 29)},
    29: "Edad desconocida",
}

_AGE_ORDER = [
    "Mortalidad neonatal", "Mortalidad infantil", "Primera infancia",
    "Niñez", "Adolescencia", "Juventud", "Adultez temprana",
    "Adultez intermedia", "Vejez", "Longevidad / Centenarios",
    "Edad desconocida",
]


def _dept_code_str(code: int | float) -> str:
    """Pad department code to 2-digit string."""
    return str(int(code)).zfill(2)


def _municipality_key(dept: int | float, mun: int | float) -> str:
    """Build 5-digit DANE municipality key."""
    return str(int(dept)).zfill(2) + str(int(mun)).zfill(3)


@lru_cache(maxsize=1)
def deaths_by_department() -> pd.DataFrame:
    """Total deaths per department with padded DPTO key for GeoJSON join.

    Returns: COD_DEPT (str, 2-digit), DEPARTAMENTO, TOTAL
    """
    m = mortality().dropna(subset=["COD_DEPARTAMENTO"])
    g = geodiv()[["CodigoDepartamento", "Departamento"]].drop_duplicates(
        subset="CodigoDepartamento"
    )

    m = m.assign(COD_DEPT=lambda x: x["COD_DEPARTAMENTO"].apply(_dept_code_str))
    df = m.groupby("COD_DEPT", as_index=False).size().rename(columns={"size": "TOTAL"})
    df = df.merge(g, left_on="COD_DEPT", right_on="CodigoDepartamento", how="left")
    df = df.assign(DEPARTAMENTO=lambda x: x["Departamento"].fillna(x["COD_DEPT"]))
    return df[["COD_DEPT", "DEPARTAMENTO", "TOTAL"]].sort_values("TOTAL", ascending=False)


@lru_cache(maxsize=1)
def deaths_by_month() -> pd.DataFrame:
    """Total deaths per month (1–12).

    Returns: MES (int), TOTAL
    """
    m = mortality().dropna(subset=["MES"])
    df = m.groupby("MES", as_index=False).size().rename(columns={"size": "TOTAL"})
    return df.sort_values("MES")


@lru_cache(maxsize=1)
def top5_violent_cities() -> pd.DataFrame:
    """Top 5 cities by homicide with firearm (COD_MUERTE starting with X95).

    Returns: MUNICIPIO, COD_DANE_KEY (str 5-digit), HOMICIDIOS
    """
    m = mortality().dropna(subset=["COD_MUERTE", "COD_DEPARTAMENTO", "COD_MUNICIPIO"])
    g = geodiv()[["CodigoMunicipio", "Municipio"]].drop_duplicates(
        subset="CodigoMunicipio"
    )

    firearm = m[m["COD_MUERTE"].str.startswith("X95", na=False)].assign(
        MUN_KEY=lambda x: x.apply(
            lambda r: _municipality_key(r["COD_DEPARTAMENTO"], r["COD_MUNICIPIO"]), axis=1
        )
    )
    df = (
        firearm.groupby("MUN_KEY", as_index=False)
        .size()
        .rename(columns={"size": "HOMICIDIOS"})
    )
    df = df.merge(g, left_on="MUN_KEY", right_on="CodigoMunicipio", how="left")
    df["MUNICIPIO"] = df["Municipio"].fillna(df["MUN_KEY"])
    return df.nlargest(5, "HOMICIDIOS")[["MUNICIPIO", "MUN_KEY", "HOMICIDIOS"]]


@lru_cache(maxsize=1)
def bottom10_mortality_cities() -> pd.DataFrame:
    """10 municipalities with the lowest total mortality (excl. zero deaths).

    Returns: MUNICIPIO, MUN_KEY, TOTAL
    """
    m = mortality().dropna(subset=["COD_DEPARTAMENTO", "COD_MUNICIPIO"])
    g = geodiv()[["CodigoMunicipio", "Municipio"]].drop_duplicates(
        subset="CodigoMunicipio"
    )

    m = m.assign(
        MUN_KEY=lambda x: x.apply(
            lambda r: _municipality_key(r["COD_DEPARTAMENTO"], r["COD_MUNICIPIO"]), axis=1
        )
    )
    df = m.groupby("MUN_KEY", as_index=False).size().rename(columns={"size": "TOTAL"})
    df = df[df["TOTAL"] > 0]
    df = df.merge(g, left_on="MUN_KEY", right_on="CodigoMunicipio", how="left")
    df["MUNICIPIO"] = df["Municipio"].fillna(df["MUN_KEY"])
    return df.nsmallest(10, "TOTAL")[["MUNICIPIO", "MUN_KEY", "TOTAL"]]


@lru_cache(maxsize=1)
def top10_causes() -> pd.DataFrame:
    """Top 10 causes of death with code, name and total.

    Returns: COD_MUERTE, NOMBRE_MUERTE, TOTAL
    """
    m = mortality().dropna(subset=["COD_MUERTE"])
    dc = death_codes()[["COD_MUERTE", "NOMBRE_MUERTE"]].drop_duplicates(
        subset="COD_MUERTE"
    )

    df = m.groupby("COD_MUERTE", as_index=False).size().rename(columns={"size": "TOTAL"})
    df = df.merge(dc, on="COD_MUERTE", how="left")
    df["NOMBRE_MUERTE"] = df["NOMBRE_MUERTE"].fillna(df["COD_MUERTE"])
    return df.nlargest(10, "TOTAL")[["COD_MUERTE", "NOMBRE_MUERTE", "TOTAL"]]


@lru_cache(maxsize=1)
def deaths_by_sex_department() -> pd.DataFrame:
    """Deaths by sex for each department.

    Returns: COD_DEPT, DEPARTAMENTO, SEXO_LABEL, TOTAL
    SEXO_LABEL: 'Masculino' | 'Femenino' | 'Indeterminado'
    """
    m = mortality().dropna(subset=["COD_DEPARTAMENTO", "SEXO"])
    g = geodiv()[["CodigoDepartamento", "Departamento"]].drop_duplicates(
        subset="CodigoDepartamento"
    )

    m = (
        m[m["SEXO"].isin([1, 2, 3])]
        .assign(
            COD_DEPT=lambda x: x["COD_DEPARTAMENTO"].apply(_dept_code_str),
            SEXO_LABEL=lambda x: x["SEXO"].map(
                {1: "Masculino", 2: "Femenino", 3: "Indeterminado"}
            ),
        )
    )
    df = (
        m.groupby(["COD_DEPT", "SEXO_LABEL"], as_index=False)
        .size()
        .rename(columns={"size": "TOTAL"})
    )
    df = df.merge(g, left_on="COD_DEPT", right_on="CodigoDepartamento", how="left")
    df = df.assign(DEPARTAMENTO=lambda x: x["Departamento"].fillna(x["COD_DEPT"]))
    return df[["COD_DEPT", "DEPARTAMENTO", "SEXO_LABEL", "TOTAL"]]


@lru_cache(maxsize=1)
def deaths_by_age_group() -> pd.DataFrame:
    """Deaths grouped by DANE age categories.

    Returns: CATEGORIA, TOTAL
    """
    m = mortality().dropna(subset=["GRUPO_EDAD1"])
    m = (
        m[m["GRUPO_EDAD1"].notna()]
        .assign(GRUPO_EDAD1=lambda x: x["GRUPO_EDAD1"].astype(int))
        .assign(
            CATEGORIA=lambda x: x["GRUPO_EDAD1"].map(_AGE_LABELS).fillna("Edad desconocida")
        )
    )
    df = m.groupby("CATEGORIA", as_index=False).size().rename(columns={"size": "TOTAL"})
    df = df.assign(
        ORDER=lambda x: x["CATEGORIA"].map(
            {v: i for i, v in enumerate(_AGE_ORDER)}
        ).fillna(len(_AGE_ORDER))
    )
    return df.sort_values("ORDER")[["CATEGORIA", "TOTAL"]]
