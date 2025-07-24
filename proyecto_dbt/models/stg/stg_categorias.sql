WITH raw_categorias AS (
    SELECT *
    FROM {{ source('public', 'categorias') }}
)

SELECT
    CategoriaID,
    Nombre,
    Descripcion
FROM raw_categorias