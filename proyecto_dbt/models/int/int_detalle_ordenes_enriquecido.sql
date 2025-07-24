WITH detalle_basico AS (
    SELECT *
    FROM {{ ref('stg_detalle_ordenes') }}
),

ordenes_basico AS (
    SELECT *
    FROM {{ ref('stg_ordenes') }}
),

productos_enriquecidos AS (
    SELECT *
    FROM {{ ref('int_productos_enriquecidos') }}
),

detalle_enriquecido AS (
    SELECT
        db.DetalleID,
        db.OrdenID,
        db.ProductoID,
        db.Cantidad,
        db.PrecioUnitario,
        db.Cantidad * db.PrecioUnitario AS subtotal,
        ob.FechaOrden,
        ob.UsuarioID,
        ob.Total AS total_orden,
        ob.Estado,
        pe.Nombre AS producto_nombre,
        pe.categoria_nombre,
        pe.segmento_precio,
        ROUND(
            (db.Cantidad * db.PrecioUnitario) * 100.0 / NULLIF(ob.Total, 0), 2
        ) AS porcentaje_del_total
    FROM detalle_basico db
    LEFT JOIN productos_enriquecidos pe ON db.ProductoID = pe.ProductoID
    LEFT JOIN ordenes_basico ob ON db.OrdenID = ob.OrdenID
)

SELECT
    DetalleID,
    OrdenID,
    Estado,
    ProductoID,
    Cantidad,
    PrecioUnitario,
    subtotal,
    producto_nombre,
    categoria_nombre,
    segmento_precio,
    FechaOrden,
    UsuarioID,
    total_orden,
    porcentaje_del_total
FROM detalle_enriquecido