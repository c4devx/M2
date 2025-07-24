{{ config(materialized='table') }}

WITH ventas_por_producto AS (
    SELECT
        p.ProductoID,
        p.Nombre,
        SUM(det.Cantidad) AS TotalVentas
    FROM {{ ref('int_detalle_ordenes_enriquecido') }} det
    JOIN {{ ref('int_productos_enriquecidos') }} p
        ON det.ProductoID = p.ProductoID
    GROUP BY p.ProductoID, p.Nombre
)


SELECT *
FROM ventas_por_producto
ORDER BY TotalVentas DESC
