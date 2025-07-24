WITH productos_base AS (
    SELECT *
    FROM {{ ref('stg_productos') }}
),

categorias_base AS (
    SELECT *
    FROM {{ ref('stg_categorias') }}
),

productos_con_categoria AS (
    SELECT
        pb.*,
        cb.Nombre AS categoria_nombre,
        cb.Descripcion AS categoria_descripcion
    FROM productos_base pb
    LEFT JOIN categorias_base cb ON pb.CategoriaID = cb.CategoriaID
),

productos_enriquecidos AS (
    SELECT
        *,
        CASE 
            WHEN Stock = 0 THEN 'sin stock'
            WHEN Stock <= 10 THEN 'stock bajo'
            WHEN Stock <= 50 THEN 'stock normal'
            ELSE 'stock alto'
        END AS estado_stock,
        CASE 
            WHEN Precio <= 250 THEN 'eco'
            WHEN Precio <= 750 THEN 'medium'
            WHEN Precio <= 1250 THEN 'premium'
            ELSE 'deluxe'
        END AS segmento_precio
    FROM productos_con_categoria
)

SELECT
    ProductoID,
    Nombre,
    Descripcion,
    Precio,
    Stock,
    CategoriaID,
    categoria_nombre,
    categoria_descripcion,
    estado_stock,
    segmento_precio
FROM productos_enriquecidos