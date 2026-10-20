# -*- coding: utf-8 -*-
"""Extrai os extremos das feicoes lineares selecionadas no ArcGIS Pro.

Para cada feicao selecionada, cria dois pontos: INICIO no extremo de maior Y
(Norte) e FIM no extremo de menor Y (Sul). A orientacao considera o sistema
de coordenadas da camada; para dados em que Y nao representa Norte/Sul, reprojete
a camada para um sistema adequado antes de executar.

Execute no Python Window do ArcGIS Pro, com o projeto aberto e a camada
configurada abaixo presente no mapa ativo, com feicoes selecionadas.
"""
from __future__ import print_function

import os
import arcpy


# ---------------------------------------------------------------------------
# CONFIGURACAO: ajuste estes valores para o seu projeto.
# ---------------------------------------------------------------------------
INPUT_FC = r"E:\03_Geodatabase\ShapesOficiais\RedeGasExemplo.shp"
OUTPUT_GDB = r"E:\01_Solicitações\04_Mapa GECOR\2026-09-setembro\Setembro2026.gdb"
OUTPUT_NAME = "CT059_Pontos"

# Campos da camada de entrada que serao copiados para os pontos de saida.
INHERITED_FIELDS = (
    "LOGRADOURO",
    "DATA_CONST",
    "ESTC_INIC",
    "ESTC_FIM",
    "GEO_2D",
    "NOME_EMPREE",
)

LAT_DMS_FIELD = "LAT_DMS"
LONG_DMS_FIELD = "LONG_DMS"


def log(message):
    print(message)
    try:
        arcpy.AddMessage(message)
    except Exception:
        pass


def format_dms(value, degree_width):
    """Formata graus decimais como graus, minutos e segundos."""
    negative = value < 0
    total_hundredths = int(round(abs(float(value)) * 3600.0 * 100.0))
    degrees, remainder = divmod(total_hundredths, 360000)
    minutes, seconds_hundredths = divmod(remainder, 6000)
    seconds = seconds_hundredths / 100.0
    sign = "-" if negative else ""
    return u"{}{:0{}d}° {:02d}' {:05.2f}\"".format(
        sign, degrees, degree_width, minutes, seconds
    )


def normalized_path(path):
    """Normaliza caminhos para comparar a fonte da camada com INPUT_FC."""
    return os.path.normcase(os.path.normpath(path))


def find_input_layer(aprx):
    """Localiza no mapa ativo a camada que aponta para INPUT_FC."""
    active_map = aprx.activeMap
    if active_map is None:
        raise RuntimeError("Nao ha mapa ativo no projeto do ArcGIS Pro.")

    expected_path = normalized_path(INPUT_FC)
    matches = []
    for layer in active_map.listLayers():
        if layer.isGroupLayer or not layer.isFeatureLayer:
            continue
        try:
            if normalized_path(layer.dataSource) == expected_path:
                matches.append(layer)
        except Exception:
            continue

    if len(matches) != 1:
        raise RuntimeError(
            "Esperada exatamente uma camada cuja fonte seja INPUT_FC; "
            "encontradas: {}. Confira o caminho configurado e a camada no mapa ativo.".format(
                len(matches)
            )
        )

    layer = matches[0]
    if not layer.getSelectionSet():
        raise RuntimeError("A camada de entrada nao possui feicoes selecionadas.")
    return layer


def add_inherited_field(output_fc, source_field, output_name):
    """Cria no destino um campo com tipo e tamanho compativeis com a origem."""
    field_types = {
        "String": "TEXT",
        "Date": "DATE",
        "Integer": "LONG",
        "SmallInteger": "SHORT",
        "Double": "DOUBLE",
        "Single": "FLOAT",
        "GUID": "GUID",
        "GlobalID": "GUID",
    }
    field_type = field_types.get(source_field.type)
    if field_type is None:
        raise RuntimeError(
            "Tipo de campo nao suportado para copia: {} ({})".format(
                source_field.name, source_field.type
            )
        )

    kwargs = {}
    if field_type == "TEXT":
        kwargs["field_length"] = max(1, source_field.length)
    if field_type in ("DOUBLE", "FLOAT"):
        kwargs["field_precision"] = source_field.precision
        kwargs["field_scale"] = source_field.scale
    arcpy.management.AddField(output_fc, output_name, field_type, **kwargs)


def resolve_source_fields(input_layer):
    """Resolve nomes de campo e aliases, incluindo NOME_EMPRE truncado."""
    fields = arcpy.ListFields(input_layer)
    lookup = {}
    for field in fields:
        lookup[field.name.upper()] = field
        if field.aliasName:
            lookup[field.aliasName.upper()] = field

    inherited = []
    missing = []
    for requested_name in INHERITED_FIELDS:
        source_field = lookup.get(requested_name.upper())
        # Shapefiles limitam nomes de campos a 10 caracteres.
        if source_field is None and requested_name == "NOME_EMPREE":
            source_field = lookup.get("NOME_EMPRE")
        if source_field is None:
            missing.append(requested_name)
        else:
            inherited.append((requested_name, source_field))

    if missing:
        raise RuntimeError(
            "Campos ausentes na entrada: {}".format(", ".join(missing))
        )
    return inherited


def main():
    if not arcpy.Exists(INPUT_FC):
        raise RuntimeError("Camada de entrada nao encontrada. Ajuste INPUT_FC no script.")
    if not arcpy.Exists(OUTPUT_GDB):
        raise RuntimeError(
            "Geodatabase de saida nao encontrada. Ajuste OUTPUT_GDB no script."
        )

    aprx = arcpy.mp.ArcGISProject("CURRENT")
    input_layer = find_input_layer(aprx)
    inherited = resolve_source_fields(input_layer)

    desc = arcpy.Describe(input_layer)
    spatial_reference = desc.spatialReference
    if spatial_reference is None or spatial_reference.name == "Unknown":
        raise RuntimeError("A camada de entrada nao possui referencia espacial conhecida.")

    geographic_reference = (
        spatial_reference
        if spatial_reference.type == "Geographic"
        else spatial_reference.GCS
    )
    if geographic_reference is None or geographic_reference.name == "Unknown":
        raise RuntimeError("A referencia espacial nao possui sistema geografico conhecido.")

    output_fc = os.path.join(OUTPUT_GDB, OUTPUT_NAME)
    if arcpy.Exists(output_fc):
        arcpy.management.Delete(output_fc)

    arcpy.management.CreateFeatureclass(
        OUTPUT_GDB,
        OUTPUT_NAME,
        "POINT",
        spatial_reference=spatial_reference,
    )
    arcpy.management.AddField(output_fc, "PONTOS", "TEXT", field_length=50)
    arcpy.management.AddField(output_fc, "X_COORD", "DOUBLE")
    arcpy.management.AddField(output_fc, "Y_COORD", "DOUBLE")

    # Campo proprio e editavel: recebe um identificador sequencial para cada
    # ponto de saida. Nao e o OID original da feicao de entrada.
    arcpy.management.AddField(output_fc, "ORIG_OID", "LONG")
    arcpy.management.AddField(output_fc, LAT_DMS_FIELD, "TEXT", field_length=32)
    arcpy.management.AddField(output_fc, LONG_DMS_FIELD, "TEXT", field_length=32)

    for output_name, source_field in inherited:
        add_inherited_field(output_fc, source_field, output_name)

    output_fields = [
        "SHAPE@", "PONTOS", "X_COORD", "Y_COORD", "ORIG_OID",
        LAT_DMS_FIELD, LONG_DMS_FIELD,
    ] + [output_name for output_name, _ in inherited]
    input_fields = ["OID@", "SHAPE@"] + [
        field.name for _, field in inherited
    ]

    # Mantem a orientacao Norte-Sul por feicao e ordena os trechos por Y,
    # usando X e o OID da origem apenas para desempatar.
    trechos = []
    with arcpy.da.SearchCursor(input_layer, input_fields) as cursor:
        for row in cursor:
            shape = row[1]
            first_point = shape.firstPoint
            last_point = shape.lastPoint
            if first_point is None or last_point is None:
                log("Geometria sem vertices ignorada (OID {}).".format(row[0]))
                continue

            if first_point.Y >= last_point.Y:
                start_point, end_point = first_point, last_point
            else:
                start_point, end_point = last_point, first_point

            trechos.append((
                start_point.Y,
                start_point.X,
                row[0],
                start_point,
                end_point,
                list(row[2:]),
            ))

    if not trechos:
        raise RuntimeError("Nenhuma feicao selecionada valida foi encontrada.")

    trechos.sort(key=lambda item: (-item[0], item[1], item[2]))

    trecho_count = 0
    point_id = 1
    inserted = 0
    with arcpy.da.InsertCursor(output_fc, output_fields) as cursor:
        for _, _, _, start_point, end_point, attributes in trechos:
            for point, suffix in (
                (start_point, "INICIO"),
                (end_point, "FIM"),
            ):
                point_geometry = arcpy.PointGeometry(
                    arcpy.Point(point.X, point.Y, point.Z, point.M),
                    spatial_reference,
                )
                geographic_point = (
                    point_geometry
                    if spatial_reference.type == "Geographic"
                    else point_geometry.projectAs(geographic_reference)
                ).firstPoint

                row_out = [
                    point_geometry,
                    "{} - {}".format(trecho_count, suffix),
                    point.X,
                    point.Y,
                    point_id,
                    format_dms(geographic_point.Y, 2),
                    format_dms(geographic_point.X, 3),
                ] + attributes
                cursor.insertRow(row_out)
                point_id += 1
                inserted += 1
            trecho_count += 1

    log("Feicoes processadas: {}".format(trecho_count))
    log("Pontos criados em {}: {}".format(output_fc, inserted))
    log("Orientacao por feicao: Norte (INICIO) para Sul (FIM).")
    log("Ordenacao: Norte para Sul; X e OID desempataram valores de Y.")
    log("ORIG_OID e um identificador sequencial editavel dos pontos de saida.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        try:
            arcpy.AddError(str(exc))
        except Exception:
            pass
        raise
