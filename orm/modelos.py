
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from db_conector import Base 

class Usuario(Base):
    __tablename__ = 'usuarios'

    usuarioid = Column('usuarioid', Integer, primary_key=True)
    nombre = Column('nombre', String(100), nullable=False)
    apellido = Column('apellido', String(100), nullable=False)
    dni = Column('dni', String(20), unique=True, nullable=False)
    email = Column('email', String(255), unique=True, nullable=False)
    contraseña = Column('contraseña', String(255), nullable=False)
    fecharegistro = Column('fecharegistro', DateTime, server_default=func.now())
    ordenes = relationship("Orden", back_populates="usuario")
    direcciones = relationship("DireccionEnvio", back_populates="usuario")
    carrito_items = relationship("Carrito", back_populates="usuario")
    reseñas = relationship("ReseñaProducto", back_populates="usuario")

class Categoria(Base):
    __tablename__ = 'categorias'

    categoriaid = Column('categoriaid', Integer, primary_key=True)
    nombre = Column('nombre', String(100), nullable=False, unique=True)
    descripcion = Column('descripcion', String(255))

    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = 'productos'

    productoid = Column('productoid', Integer, primary_key=True)
    nombre = Column('nombre', String(255), nullable=False)
    descripcion = Column('descripcion', Text)
    precio = Column(Numeric(10,2), nullable=False)
    stock = Column('stock', Integer, nullable=False)
    categoriaid = Column('categoriaid', Integer, ForeignKey('categorias.categoriaid'))

    categoria = relationship("Categoria", back_populates="productos")
    detalles = relationship("DetalleOrden", back_populates="producto")
    reseñas = relationship("ReseñaProducto", back_populates="producto")
    carrito_items = relationship("Carrito", back_populates="producto")

class Orden(Base):
    __tablename__ = 'ordenes'

    ordenid = Column('ordenid', Integer, primary_key=True)
    usuarioid = Column('usuarioid', Integer, ForeignKey('usuarios.usuarioid'))
    fecha_orden = Column('fechaorden', DateTime, server_default=func.now())
    total = Column('total', Numeric(10,2), nullable=False)
    estado = Column('estado', String(50), server_default='Pendiente')

    usuario = relationship("Usuario", back_populates="ordenes")
    detalles = relationship("DetalleOrden", back_populates="orden")
    metodos_pago = relationship("OrdenMetodoPago", back_populates="orden")
    historial_pagos = relationship("HistorialPago", back_populates="orden")

class DetalleOrden(Base):
    __tablename__ = 'detalleordenes'

    detalleid = Column('detalleid', Integer, primary_key=True)
    ordenid = Column('ordenid', Integer, ForeignKey('ordenes.ordenid'))
    productoid = Column('productoid', Integer, ForeignKey('productos.productoid'))
    cantidad = Column('cantidad', Integer, nullable=False)
    precio_unitario = Column('precio_unitario', Numeric(10,2), nullable=False)

    orden = relationship("Orden", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")

class DireccionEnvio(Base):
    __tablename__ = 'direccionesenvio'

    direccion_id = Column('direccion_id', Integer, primary_key=True)
    usuarioid = Column('usuarioid', Integer, ForeignKey('usuarios.usuarioid'))
    calle = Column('calle', String(255), nullable=False)
    ciudad = Column('ciudad', String(100), nullable=False)
    departamento = Column('departamento', String(100))
    provincia = Column(String(100))
    distrito = Column(String(100))
    estado = Column(String(100))
    codigo_postal = Column(String(20))
    pais = Column(String(100), nullable=False)

    usuario = relationship("Usuario", back_populates="direcciones")

class Carrito(Base):
    __tablename__ = 'carrito'

    carritoid = Column('carritoid', Integer, primary_key=True)
    usuarioid = Column('usuarioid', Integer, ForeignKey('usuarios.usuarioid'))
    productoid = Column('productoid', Integer, ForeignKey('productos.productoid'))
    cantidad = Column('cantidad', Integer, nullable=False)
    fecha_agregado = Column('fecha_agregado', DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="carrito_items")
    producto = relationship("Producto", back_populates="carrito_items")

class MetodoPago(Base):
    __tablename__ = 'metodospago'

    metodopagoid = Column('metodopagoid', Integer, primary_key=True)
    nombre = Column('nombre', String(100), nullable=False)
    descripcion = Column('descripcion', String(255))

    ordenes_pago = relationship("OrdenMetodoPago", back_populates="metodo_pago")
    historial_pagos = relationship("HistorialPago", back_populates="metodo_pago")

class OrdenMetodoPago(Base):
    __tablename__ = 'ordenesmetodospago'

    orden_metodo_id = Column('orden_metodo_id', Integer, primary_key=True)
    ordenid = Column('ordenid', Integer, ForeignKey('ordenes.ordenid'))
    metodopagoid = Column('metodopagoid', Integer, ForeignKey('metodospago.metodopagoid'))
    monto_pagado = Column('monto_pagado', Numeric(10,2), nullable=False)

    orden = relationship("Orden", back_populates="metodos_pago")
    metodo_pago = relationship("MetodoPago", back_populates="ordenes_pago")

class ReseñaProducto(Base):
    __tablename__ = 'reseñasproductos'

    reseña_id = Column('reseña_id', Integer, primary_key=True)
    usuarioid = Column('usuarioid', Integer, ForeignKey('usuarios.usuarioid'))
    productoid = Column('productoid', Integer, ForeignKey('productos.productoid'))
    calificacion = Column('calificacion', Integer, CheckConstraint('calificacion >= 1 AND calificacion <= 5'))
    comentario = Column('comentario', Text)
    fecha = Column(DateTime, server_default=func.now())

    usuario = relationship("Usuario", back_populates="reseñas")
    producto = relationship("Producto", back_populates="reseñas")

class HistorialPago(Base):
    __tablename__ = 'historialpagos'

    pagoid = Column('pagoid', Integer, primary_key=True)
    ordenid = Column('ordenid', Integer, ForeignKey('ordenes.ordenid'))
    metodopagoid = Column('metodopagoid', Integer, ForeignKey('metodospago.metodopagoid'))
    monto = Column('monto', Numeric(10,2), nullable=False)
    fecha_pago = Column('fechapago', DateTime, server_default=func.now())
    estado_pago = Column('estadopago', String(50), server_default='Procesando')

    orden = relationship("Orden", back_populates="historial_pagos")
    metodo_pago = relationship("MetodoPago", back_populates="historial_pagos")