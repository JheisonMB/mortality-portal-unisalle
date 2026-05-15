"""Raw data loading — reads CSVs once and exposes clean DataFrames."""
from __future__ import annotations

import os
from functools import lru_cache

import pandas as pd

_RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

_MORTALITY_FILE = os.path.join(_RAW, "Anexo1.NoFetal2019_CE_15-03-23.csv")
_CODES_FILE = os.path.join(_RAW, "Anexo2.CodigosDeMuerte_CE_15-03-23.csv")
_DIVIPOLA_FILE = os.path.join(_RAW, "Divipola_CE_Hoja1.csv")
_GEODIV_FILE = os.path.join(_RAW, "Divipola_CE_Hoja3.csv")
_GEOJSON_FILE = os.path.join(_RAW, "Colombia.geo.json")


@lru_cache(maxsize=1)
def mortality() -> pd.DataFrame:
    df = pd.read_csv(_MORTALITY_FILE, dtype=str, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    # Strip BOM from first column name if present
    df.rename(columns={df.columns[0]: "COD_DANE"}, inplace=True)
    int_cols = ["COD_DEPARTAMENTO", "COD_MUNICIPIO", "AÑO", "MES",
                "HORA", "MINUTOS", "SEXO", "GRUPO_EDAD1"]
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@lru_cache(maxsize=1)
def death_codes() -> pd.DataFrame:
    # File has inconsistent trailing commas; parse manually and truncate to 6 fields
    import csv as _csv
    rows = []
    with open(_CODES_FILE, encoding="utf-8-sig", newline="") as fh:
        reader = _csv.reader(fh)
        header = next(reader)[:6]
        for row in reader:
            rows.append(row[:6])
    df = pd.DataFrame(rows, columns=[c.strip() for c in header])
    df.rename(columns={
        "Código de la CIE-10 cuatro caracteres": "COD_MUERTE",
        "Descripcion  de códigos mortalidad a cuatro caracteres": "NOMBRE_MUERTE",
        "Código de la CIE-10 tres caracteres": "COD3",
        "Descripción  de códigos mortalidad a tres caracteres": "NOMBRE3",
    }, inplace=True)
    return df


@lru_cache(maxsize=1)
def divipola() -> pd.DataFrame:
    """Municipality → department mapping with DANE codes."""
    df = pd.read_csv(_DIVIPOLA_FILE, dtype=str, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: "COD_DANE"}, inplace=True)
    return df


@lru_cache(maxsize=1)
def geodiv() -> pd.DataFrame:
    """Municipality geo data with lat/lon."""
    df = pd.read_csv(_GEODIV_FILE, dtype=str, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: "CodigoDepartamento"}, inplace=True)
    return df


def geojson_path() -> str:
    return _GEOJSON_FILE
