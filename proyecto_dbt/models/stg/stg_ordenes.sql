WITH raw_ordenes AS (
    SELECT *
    FROM {{ source('public', 'ordenes') }}
)

SELECT
    OrdenID,
    UsuarioID,
    FechaOrden,
    Total,
    Estado
FROM raw_ordenes

