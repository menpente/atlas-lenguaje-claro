"""Calcula el índice PLDI (0-100) y genera la matriz semáforo país x pilar.

Regla central (ver metodologia.qmd, P7): una celda con `insufficient_evidence`
se trata como dato ausente (NaN), no como cero. En el estado actual de la
recolección (P2/P3 solo cubrieron una fracción de las fuentes posibles),
todo cero en `pldi_coding.csv` significa "no se ha buscado todavía", nunca
"se buscó y no se encontró" — tratarlo como ausencia real, no como un cero
sustantivo, es la única lectura honesta con los datos disponibles hoy.

Paleta: paleta de estado validada (verde/ámbar/rojo + gris neutro para
"sin datos"), nunca solo color — cada celda lleva también una etiqueta de
texto, por la regla de "color nunca solo" del sistema de diseño.
"""

from __future__ import annotations

import pandas as pd

from atlas.config import COUNTRY_UNIVERSE, DATA_CODING, DATA_PROCESSED, PILLARS

STATUS_COLORS = {
    "verde": "#0ca30c",
    "ambar": "#fab219",
    "rojo": "#d03b3b",
    "sin_datos": "#9a9a95",
}
STATUS_LABELS = {"verde": "V", "ambar": "Á", "rojo": "R", "sin_datos": "–"}


def _semaforo_bucket(score: float) -> str:
    if pd.isna(score):
        return "sin_datos"
    if score >= 3:
        return "verde"
    if score >= 2:
        return "ambar"
    return "rojo"


def load_coding() -> pd.DataFrame:
    df = pd.read_csv(DATA_CODING / "pldi_coding.csv")
    df["score_or_nan"] = df["score"].where(~df["insufficient_evidence"], other=float("nan"))
    return df


def pillar_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Media por país x pilar de los 3 indicadores, ignorando NaN (sin_datos)."""
    pivot = df.pivot_table(
        index="iso3", columns="pillar", values="score_or_nan", aggfunc="mean"
    )
    return pivot.reindex(columns=list(PILLARS), index=list(COUNTRY_UNIVERSE))


def country_index(pillars_df: pd.DataFrame) -> pd.Series:
    """Índice 0-100 = media de las puntuaciones de pilar disponibles / 4 * 100."""
    return pillars_df.mean(axis=1, skipna=True) / 4 * 100


def coverage(df: pd.DataFrame) -> pd.Series:
    """Fracción de los 24 indicadores (8 pilares x 3) con evidencia real por país."""
    covered = df.assign(has_evidence=~df["insufficient_evidence"])
    return covered.groupby("iso3")["has_evidence"].mean().reindex(list(COUNTRY_UNIVERSE))


def drop_one_pillar_sensitivity(pillars_df: pd.DataFrame) -> pd.DataFrame:
    """Correlación de rango (Spearman) entre el índice completo y el índice
    recalculado omitiendo cada pilar, uno a la vez — criterio de aceptación
    de P7."""
    full_index = pillars_df.mean(axis=1, skipna=True)
    rows = []
    for pillar in pillars_df.columns:
        dropped = pillars_df.drop(columns=[pillar]).mean(axis=1, skipna=True)
        both = pd.concat([full_index, dropped], axis=1).dropna()
        # Spearman = Pearson sobre los rangos; se evita la dependencia de scipy.
        if len(both) > 1:
            corr = both.iloc[:, 0].rank().corr(both.iloc[:, 1].rank())
        else:
            corr = float("nan")
        rows.append(
            {"pilar_omitido": pillar, "spearman_rho": corr, "n_paises_comparados": len(both)}
        )
    return pd.DataFrame(rows)


def build_pldi_table() -> pd.DataFrame:
    df = load_coding()
    pillars_df = pillar_scores(df)
    out = pillars_df.copy()
    out["indice"] = country_index(pillars_df)
    out["cobertura"] = coverage(df)
    out.insert(0, "nombre", [COUNTRY_UNIVERSE[iso3] for iso3 in out.index])
    return out.reset_index().rename(columns={"index": "iso3"})


def render_semaforo_html(pillars_df: pd.DataFrame) -> str:
    pillar_labels = {key: spec["label"] for key, spec in PILLARS.items()}
    rows_html = []
    for iso3 in pillars_df.index:
        cells = []
        for pillar in pillars_df.columns:
            score = pillars_df.loc[iso3, pillar]
            bucket = _semaforo_bucket(score)
            color = STATUS_COLORS[bucket]
            label = STATUS_LABELS[bucket]
            title = f"{pillar_labels[pillar]}: {'sin datos' if pd.isna(score) else round(score, 1)}"
            cells.append(
                f'<td class="semaforo-cell" style="background:{color}" title="{title}">'
                f'<span class="visually-hidden">{title}</span>{label}</td>'
            )
        nombre = COUNTRY_UNIVERSE[iso3]
        rows_html.append(f"<tr><th scope=\"row\">{nombre}</th>{''.join(cells)}</tr>")

    header_cells = "".join(
        f'<th scope="col">{PILLARS[p]["label"]}</th>' for p in pillars_df.columns
    )

    return f"""<!-- Generado por atlas.viz.semaforo — no editar a mano -->
<style>
.semaforo-table {{ border-collapse: collapse; font: 14px/1.4 system-ui, sans-serif; }}
.semaforo-table th, .semaforo-table td {{ padding: 6px 10px; text-align: center; }}
.semaforo-table th[scope="row"] {{ text-align: left; }}
.semaforo-cell {{ color: #0b0b0b; font-weight: 600; border: 2px solid var(--surface-1, #fcfcfb); }}
.visually-hidden {{
    position: absolute; width: 1px; height: 1px; overflow: hidden;
    clip: rect(0 0 0 0); white-space: nowrap;
}}
</style>
<table class="semaforo-table">
  <thead><tr><th scope="col">País</th>{header_cells}</tr></thead>
  <tbody>
    {"".join(rows_html)}
  </tbody>
</table>
<p><strong>Leyenda:</strong>
  <span class="semaforo-cell" style="background:{STATUS_COLORS['verde']}">V</span> verde (3-4) ·
  <span class="semaforo-cell" style="background:{STATUS_COLORS['ambar']}">Á</span> ámbar (2) ·
  <span class="semaforo-cell" style="background:{STATUS_COLORS['rojo']}">R</span> rojo (0-1) ·
  <span class="semaforo-cell" style="background:{STATUS_COLORS['sin_datos']}">–</span> sin datos
  (no confundir con cero: significa que no se ha recolectado evidencia todavía).
</p>
"""


def main() -> None:
    df = load_coding()
    pillars_df = pillar_scores(df)

    pldi_table = build_pldi_table()
    (DATA_PROCESSED / "pldi.parquet").parent.mkdir(parents=True, exist_ok=True)
    pldi_table.to_parquet(DATA_PROCESSED / "pldi.parquet", index=False)

    sensitivity = drop_one_pillar_sensitivity(pillars_df)
    sensitivity.to_csv(DATA_PROCESSED / "sensitivity_drop_one_pillar.csv", index=False)

    html = render_semaforo_html(pillars_df)
    (DATA_PROCESSED / "semaforo.html").write_text(html, encoding="utf-8")

    print(pldi_table[["nombre", "indice", "cobertura"]].sort_values("indice", ascending=False))
    print()
    print("Sensibilidad (drop-one-pillar Spearman rho):")
    print(sensitivity)


if __name__ == "__main__":
    main()
