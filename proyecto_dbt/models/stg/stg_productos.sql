WITH raw_productos AS (
    SELECT *
    FROM {{ source('public', 'productos') }}
)

SELECT
    ProductoID,
    Nombre,
    Descripcion,
    Precio,
    Stock,
    CategoriaID
FROM raw_productos