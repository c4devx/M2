WITH raw_resenas_productos AS (
    SELECT *
    FROM {{ source('public', 'resenasproductos') }}
)

SELECT
    ReseñaID,
    UsuarioID,
    ProductoID,
    Calificacion,
    Comentario,
    Fecha
FROM raw_resenas_productos