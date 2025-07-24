{{ config(
    materialized='table',
    description='Tabla base con órdenes completadas para optimizar consultas de KPIs'
) }}

SELECT 
    OrdenID,
    UsuarioID,
    Total,
    FechaOrden,
    Estado
FROM {{ source('public', 'ordenes') }}
WHERE Estado = 'Completado'