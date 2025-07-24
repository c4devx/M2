-- models/intermediate/int_metricas_productos.sql
WITH productos AS (
    SELECT *
    FROM {{ ref('int_productos_enriquecidos') }}
),

detalle_ordenes AS (
    SELECT *
    FROM {{ ref('int_detalle_ordenes_enriquecido') }}
),

resenas AS (
    SELECT *
    FROM {{ ref('int_resenas_agregadas') }}
),

metricas_ventas AS (
    SELECT
        ProductoID,
        COUNT(DISTINCT OrdenID) AS total_ordenes,
        SUM(Cantidad) AS total_vendido,
        AVG(Cantidad) AS promedio_cantidad_por_orden,
        SUM(subtotal) AS ingresos_totales,
        AVG(subtotal) AS ingreso_promedio_por_orden,
        MIN(FechaOrden) AS primera_venta,
        MAX(FechaOrden) AS ultima_venta
    FROM detalle_ordenes
    GROUP BY ProductoID
),

metricas_resenas AS (
    SELECT
        ProductoID,
        COUNT(*) AS total_resenas,
        AVG(Calificacion) AS calificacion_promedio,
        COUNT(CASE WHEN sentimiento_calificacion = 'Positiva' THEN 1 END) AS resenas_positivas,
        COUNT(CASE WHEN sentimiento_calificacion = 'Negativa' THEN 1 END) AS resenas_negativas
    FROM resenas
    GROUP BY ProductoID
),

productos_con_metricas AS (
    SELECT
        p.*,
        COALESCE(v.total_ordenes, 0) AS total_ordenes,
        COALESCE(v.total_vendido, 0) AS total_vendido,
        COALESCE(v.promedio_cantidad_por_orden, 0) AS promedio_cantidad_por_orden,
        COALESCE(v.ingresos_totales, 0) AS ingresos_totales,
        COALESCE(v.ingreso_promedio_por_orden, 0) AS ingreso_promedio_por_orden,
        v.primera_venta,
        v.ultima_venta,
        COALESCE(r.total_resenas, 0) AS total_resenas,
        COALESCE(r.calificacion_promedio, 0) AS calificacion_promedio,
        COALESCE(r.resenas_positivas, 0) AS resenas_positivas,
        COALESCE(r.resenas_negativas, 0) AS resenas_negativas,
        CASE 
            WHEN COALESCE(v.total_vendido, 0) = 0 THEN 'sin ventas'
            WHEN v.total_vendido <= 50 THEN 'pocas'
            WHEN v.total_vendido <= 150 THEN 'moderadas'
            ELSE 'altas'
        END AS categoria_ventas,
        CASE 
            WHEN COALESCE(r.calificacion_promedio, 0) = 0 THEN 'sin calificar'
            WHEN r.calificacion_promedio >= 4 THEN 'muy bueno'
            WHEN r.calificacion_promedio >= 3 THEN 'bueno'
            ELSE 'a mejorar'
        END AS categoria_calificacion
    FROM productos p
    LEFT JOIN metricas_ventas v ON p.ProductoID = v.ProductoID
    LEFT JOIN metricas_resenas r ON p.ProductoID = r.ProductoID
)

SELECT *
FROM productos_con_metricas