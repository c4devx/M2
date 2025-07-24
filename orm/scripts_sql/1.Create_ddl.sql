-- Crear tabla: Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    UsuarioID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    DNI VARCHAR(20) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Contraseña VARCHAR(255) NOT NULL,
    FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla: Categorías
CREATE TABLE IF NOT EXISTS Categorias (
    CategoriaID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(255)
);

-- Crear tabla: Productos
CREATE TABLE IF NOT EXISTS Productos (
    ProductoID SERIAL PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Precio DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL,
    CategoriaID INT REFERENCES Categorias(CategoriaID)
);

-- Crear tabla: Órdenes
CREATE TABLE IF NOT EXISTS Ordenes (
    OrdenID SERIAL PRIMARY KEY,
    UsuarioID INT REFERENCES Usuarios(UsuarioID),
    FechaOrden TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Total DECIMAL(10,2) NOT NULL,
    Estado VARCHAR(50) DEFAULT 'Pendiente'
);

-- Crear tabla: Detalle de Órdenes
CREATE TABLE IF NOT EXISTS DetalleOrdenes (
    DetalleID SERIAL PRIMARY KEY,
    OrdenID INT REFERENCES Ordenes(OrdenID),
    ProductoID INT REFERENCES Productos(ProductoID),
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL
);

-- Crear tabla: Direcciones de Envío
CREATE TABLE IF NOT EXISTS DireccionesEnvio (
    DireccionID SERIAL PRIMARY KEY,
    UsuarioID INT REFERENCES Usuarios(UsuarioID),
    Calle VARCHAR(255) NOT NULL,
    Ciudad VARCHAR(100) NOT NULL,
    Departamento VARCHAR(100),
    Provincia VARCHAR(100),
    Distrito VARCHAR(100),
    Estado VARCHAR(100),
    CodigoPostal VARCHAR(20),
    Pais VARCHAR(100) NOT NULL
);

-- Crear tabla: Carrito de Compras
CREATE TABLE IF NOT EXISTS Carrito (
    CarritoID SERIAL PRIMARY KEY,
    UsuarioID INT REFERENCES Usuarios(UsuarioID),
    ProductoID INT REFERENCES Productos(ProductoID),
    Cantidad INT NOT NULL,
    FechaAgregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla: Métodos de Pago
CREATE TABLE IF NOT EXISTS MetodosPago (
    MetodoPagoID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(255)
);

-- Crear tabla: Ordenes Métodos de Pago
CREATE TABLE IF NOT EXISTS OrdenesMetodosPago (
    OrdenMetodoID SERIAL PRIMARY KEY,
    OrdenID INT REFERENCES Ordenes(OrdenID),
    MetodoPagoID INT REFERENCES MetodosPago(MetodoPagoID),
    MontoPagado DECIMAL(10,2) NOT NULL
);

-- Crear tabla: Reseñas de Productos
CREATE TABLE IF NOT EXISTS ResenasProductos (
    ReseñaID SERIAL PRIMARY KEY,
    UsuarioID INT REFERENCES Usuarios(UsuarioID),
    ProductoID INT REFERENCES Productos(ProductoID),
    Calificacion INT CHECK (Calificacion >= 1 AND Calificacion <= 5),
    Comentario TEXT,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla: Historial de Pagos
CREATE TABLE IF NOT EXISTS HistorialPagos (
    PagoID SERIAL PRIMARY KEY,
    OrdenID INT REFERENCES Ordenes(OrdenID),
    MetodoPagoID INT REFERENCES MetodosPago(MetodoPagoID),
    Monto DECIMAL(10,2) NOT NULL,
    FechaPago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    EstadoPago VARCHAR(50) DEFAULT 'Procesando'
);

