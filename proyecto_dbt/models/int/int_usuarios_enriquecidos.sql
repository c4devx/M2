-- models/intermediate/int_usuarios_enriquecidos.sql
WITH usuarios_base AS (
    SELECT *
    FROM {{ ref('stg_usuarios') }}
),

usuarios_actividad AS (
    SELECT
        u.*,
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, u.FechaRegistro)) AS años_como_usuario,
        EXTRACT(DAY FROM AGE(CURRENT_DATE, u.FechaRegistro)) AS dias_como_usuario,
        CASE 
            WHEN EXTRACT(DAY FROM AGE(CURRENT_DATE, u.FechaRegistro)) <= 30 THEN 'Nuevo'
            WHEN EXTRACT(DAY FROM AGE(CURRENT_DATE, u.FechaRegistro)) <= 365 THEN 'Activo'
            ELSE 'Veterano'
        END AS segmento_antiguedad
    FROM usuarios_base u
)

SELECT
    UsuarioID,
    Nombre,
    Apellido,
    CONCAT(Nombre, ' ', Apellido) AS nombre_completo,
    Email,
    LOWER(Email) AS email_normalizado,
    FechaRegistro,
    años_como_usuario,
    dias_como_usuario,
    segmento_antiguedad
FROM usuarios_actividad