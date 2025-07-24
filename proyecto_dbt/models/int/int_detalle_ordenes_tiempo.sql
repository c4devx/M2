WITH detalle_ordenes_resumen AS (
    SELECT
        TO_CHAR(FechaOrden, 'Mon-YY') AS periodo_corto,
        EXTRACT(YEAR FROM FechaOrden) AS anio,
        EXTRACT(MONTH FROM FechaOrden) AS mes,
        OrdenID,
        estado,
        MAX(total_orden) AS total_orden,
        SUM(subtotal) AS total_facturado_por_linea,
        SUM(Cantidad) AS unidades_vendidas
    FROM {{ ref('int_detalle_ordenes_enriquecido') }}
    GROUP BY OrdenID, anio, mes, periodo_corto, estado
)

SELECT
    periodo_corto,
    anio,
    mes,
    estado,
    COUNT(*) AS total_cantidad_ordenes,
    SUM(unidades_vendidas) AS total_unidades_vendidas,
    SUM(total_orden) AS total_facturado_orden,
    SUM(total_facturado_por_linea) AS total_facturado_calculado,
    SUM(total_orden) > SUM(total_facturado_por_linea) AS es_total_orden_mayor
FROM detalle_ordenes_resumen
GROUP BY periodo_corto, anio, mes, estado
ORDER BY anio, mes, estado

