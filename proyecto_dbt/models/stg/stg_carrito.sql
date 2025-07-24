WITH raw_carrito AS (
    SELECT *
    FROM {{ source('public', 'carrito') }}
)

SELECT
    CarritoID,
    UsuarioID,
    ProductoID,
    Cantidad,
    FechaAgregado
FROM raw_carrito