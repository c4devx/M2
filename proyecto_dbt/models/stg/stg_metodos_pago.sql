WITH raw_metodos_pago AS (
    SELECT *
    FROM {{ source('public', 'metodospago') }}
)

SELECT
    MetodoPagoID,
    Nombre,
    Descripcion
FROM raw_metodos_pago