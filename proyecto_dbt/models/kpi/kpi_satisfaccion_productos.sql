{{ config(
    materialized='view',
    description='KPI. Promedio calificación productos.'
) }}

SELECT 
    'calificación_promedio_productos' AS kpi_nombre,
    ROUND(AVG(Calificacion), 2) AS valor,
    'puntos' AS unidad,
    'Calificación promedio de los productos' AS descripcion
FROM {{ ref('int_resenas_agregadas') }}
