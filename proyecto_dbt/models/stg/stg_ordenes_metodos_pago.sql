WITH raw_ordenes_metodos_pago AS (
    SELECT *
    FROM {{ source('public', 'ordenesmetodospago') }}
)

SELECT
    OrdenMetodoID,
    OrdenID,
    MetodoPagoID,
    MontoPagado
FROM raw_ordenes_metodos_pago