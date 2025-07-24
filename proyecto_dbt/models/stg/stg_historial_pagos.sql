WITH raw_historial_pagos AS (
    SELECT *
    FROM {{ source('public', 'historialpagos') }}
)

SELECT
    PagoID,
    OrdenID,
    MetodoPagoID,
    Monto,
    FechaPago,
    EstadoPago
FROM raw_historial_pagos