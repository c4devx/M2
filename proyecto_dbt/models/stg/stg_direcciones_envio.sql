WITH raw_direcciones_envio AS (
    SELECT *
    FROM {{ source('public', 'direccionesenvio') }}
)

SELECT
    DireccionID,
    UsuarioID,
    Calle,
    Ciudad,
    Departamento,
    Provincia,
    Distrito,
    Estado,
    CodigoPostal,
    Pais
FROM raw_direcciones_envio