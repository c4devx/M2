{{ config(materialized='table') }}

WITH ordenes_con_productos AS (
    SELECT
        o.OrdenID,
        p.categoria_nombre,
        det.Cantidad
    FROM {{ ref('int_detalle_ordenes_enriquecido') }} det
    JOIN {{ ref('int_productos_enriquecidos') }} p ON det.ProductoID = p.ProductoID
    JOIN {{ source('public', 'ordenes') }} o ON det.OrdenID = o.OrdenID
),

conversiones_por_categoria AS (
    SELECT
        categoria_nombre,
        COUNT(DISTINCT OrdenID) AS CantOrdenes
    FROM ordenes_con_productos
    GROUP BY categoria_nombre
)

SELECT
    categoria_nombre AS Categoria,
    CantOrdenes * 1.0 / NULLIF(SUM(CantOrdenes) OVER (), 0) AS TasaConversion
FROM conversiones_por_categoria
