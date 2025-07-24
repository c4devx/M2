import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os


st.set_page_config(page_title="Dashboard E-commerce", layout="wide")


DB = os.getenv("POSTGRES_DB", "EcommerceDB")
USER = os.getenv("POSTGRES_USER", "admin")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin1234")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")

def snake_to_title(s):
    return ' '.join(word.capitalize() for word in s.split('_'))

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

@st.cache_data
def load_data():
    df_compras = pd.read_sql("SELECT * FROM int_detalle_ordenes_enriquecido", engine)
    df_productos = pd.read_sql("SELECT * FROM int_metricas_productos", engine)  
    df_ventas_tiempo = pd.read_sql("SELECT * FROM int_detalle_ordenes_tiempo", engine)
    kpi_ventas = pd.read_sql("SELECT * FROM kpi_valor_total_ventas", engine)
    kpi_ticket = pd.read_sql("SELECT * FROM kpi_ticket_promedio", engine)
    kpi_facturacion_mensual = pd.read_sql("SELECT * FROM kpi_promedio_mensual", engine)
    kpi_porcentaje_ventas_ok = pd.read_sql("SELECT * FROM kpi_porcentaje_ventas_ok", engine)
    kpi_satisfaccion = pd.read_sql("SELECT * FROM kpi_satisfaccion_productos", engine)
    kpi_recompra = pd.read_sql("SELECT * FROM kpi_recompra_clientes", engine)
    return kpi_ventas, kpi_ticket, kpi_facturacion_mensual, kpi_porcentaje_ventas_ok, kpi_satisfaccion, kpi_recompra, df_compras, df_productos, df_ventas_tiempo

kpi_ventas, kpi_ticket, kpi_facturacion_mensual, kpi_porcentaje_ventas_ok, kpi_satisfaccion, kpi_recompra, df_compras, df_productos, df_ventas_tiempo = load_data()

df_compras["fechaorden"] = pd.to_datetime(df_compras["fechaorden"])

tab1, tab2, tab3, tab4 = st.tabs(["KPIs", "Facturación", "Ventas", "Productos"])

with tab1:
    st.header("KPIs principales")

    df_kpis = pd.DataFrame([
    {
        "kpi_nombre": kpi_ventas.iloc[0]["kpi_nombre"],
        "valor": kpi_ventas.iloc[0]["valor"],
        "descripcion": kpi_ventas.iloc[0]["descripcion"],
        "unidad": kpi_ventas.iloc[0]["unidad"],
    },
    {
        "kpi_nombre": kpi_ticket.iloc[0]["kpi_nombre"],
        "valor": kpi_ticket.iloc[0]["valor"],
        "descripcion": kpi_ticket.iloc[0]["descripcion"],
        "unidad": kpi_ticket.iloc[0]["unidad"],
    },
    {
        "kpi_nombre": kpi_facturacion_mensual.iloc[0]["kpi_nombre"],
        "valor": kpi_facturacion_mensual.iloc[0]["valor"],
        "descripcion": kpi_facturacion_mensual.iloc[0]["descripcion"],
        "unidad": kpi_facturacion_mensual.iloc[0]["unidad"],
    },
    {
        "kpi_nombre": kpi_porcentaje_ventas_ok.iloc[0]["kpi_nombre"],
        "valor": kpi_porcentaje_ventas_ok.iloc[0]["valor"],
        "descripcion": kpi_porcentaje_ventas_ok.iloc[0]["descripcion"],
        "unidad": kpi_porcentaje_ventas_ok.iloc[0]["unidad"],
    },
    {
        "kpi_nombre": kpi_satisfaccion.iloc[0]["kpi_nombre"],
        "valor": kpi_satisfaccion.iloc[0]["valor"],
        "descripcion": kpi_satisfaccion.iloc[0]["descripcion"],
        "unidad": kpi_satisfaccion.iloc[0]["unidad"],
    },
    {
        "kpi_nombre": kpi_recompra.iloc[0]["kpi_nombre"],
        "valor": kpi_recompra.iloc[0]["valor"],
        "descripcion": kpi_recompra.iloc[0]["descripcion"],
        "unidad": kpi_recompra.iloc[0]["unidad"],
    },
    ])
    cols = st.columns(3)  
    for i in range(0, len(df_kpis), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(df_kpis):
                kpi = df_kpis.iloc[i + j]
                with col:
                    st.markdown(f"""
                    <style>
                    .kpi-card {{
                        border-top: 2px solid transparent;
                        border-image: linear-gradient(to right, #ffa07a, #ff6347);
                        border-image-slice: 1;
                        border-right: 1px solid rgba(255, 99, 71, 0.2);
                        border-radius: 16px;
                        padding: 20px;
                        background-color: #fffaf9;
                        text-align: center;
                        width: 100%;
                        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
                        margin-bottom: 30px;
                    }}
                    .kpi-title {{
                        font-size: 15px;
                        font-weight: 600;
                        color: #333;
                        margin-bottom: 8px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        gap: 6px;
                    }}
                    .tooltip-icon {{
                        position: relative;
                        background-color: #ccc;
                        color: white;
                        border-radius: 50%;
                        width: 18px;
                        height: 18px;
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 12px;
                        font-weight: bold;
                        cursor: default;
                    }}
                    .tooltip-icon::after {{
                        content: attr(data-tooltip);
                        position: absolute;
                        bottom: 125%;
                        left: 50%;
                        transform: translateX(-50%);
                        background-color: #333;
                        color: #fff;
                        padding: 6px 10px;
                        border-radius: 5px;
                        font-size: 12px;
                        white-space: nowrap;
                        opacity: 0;
                        pointer-events: none;
                        transition: opacity 0.2s ease;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                        z-index: 100;
                    }}
                    .tooltip-icon:hover::after {{
                        opacity: 1;
                    }}
                    .kpi-value {{
                        font-size: 24px;
                        font-weight: 700;
                        color: #FF4B4B;
                    }}
                    </style>
                    <div class="kpi-card">
                        <div class="kpi-title">
                            {snake_to_title(kpi['kpi_nombre'])}
                            <span class="tooltip-icon" data-tooltip="{kpi['descripcion']}">?</span>
                        </div>
                        <div class="kpi-value">{kpi['valor']:,.2f} <span style="margin-left: 4px; font-size: 0.9em; color: #555;">{kpi['unidad']}</span></div>
                    </div>
                """, unsafe_allow_html=True)

with tab2:
    st.header("Análisis de facturación")

    col7, col8 = st.columns(2)

    with col7:
        st.subheader("Facturación mensual")

        df_resumen = df_ventas_tiempo.copy()
        df_resumen["anio"] = df_resumen["anio"].astype(int)
        df_resumen["mes"] = df_resumen["mes"].astype(int)
        df_resumen["fecha"] = pd.to_datetime(df_resumen["anio"].astype(str) + "-" + df_resumen["mes"].astype(str) + "-01")
        
        ultimos_fechas = (
            df_resumen[["periodo_corto", "fecha"]]
            .drop_duplicates()
            .sort_values("fecha")
            .tail(12)
        )
        
        ultimos_12m = df_resumen[df_resumen["fecha"].isin(ultimos_fechas["fecha"])]
        
        facturado_mensual = (
            ultimos_12m
            .groupby(["periodo_corto", "fecha", "anio"])["total_facturado_calculado"]
            .sum()
            .reset_index()
            .sort_values("fecha")
        )
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            data=facturado_mensual,
            x="periodo_corto",
            y="total_facturado_calculado",
            palette="crest",
            ax=ax
        )
        
        media_2024 = facturado_mensual.loc[facturado_mensual['anio'] == 2024, 'total_facturado_calculado'].mean()
        media_2025 = facturado_mensual.loc[facturado_mensual['anio'] == 2025, 'total_facturado_calculado'].mean()
        
        media_2024_line = [
            media_2024 if anio == 2024 else None
            for anio in facturado_mensual["anio"]
        ]
        
        media_2025_line = [
            media_2025 if anio == 2025 else None
            for anio in facturado_mensual["anio"]
        ]
        
        ax.plot(facturado_mensual["periodo_corto"], media_2024_line, color='red', linestyle='--', label=f'Media 2024: {media_2024:.2f}')
        ax.plot(facturado_mensual["periodo_corto"], media_2025_line, color='blue', linestyle='--', label=f'Media 2025: {media_2025:.2f}')
        
        ax.legend(
            loc='upper right',
            fontsize=12,
            frameon=True,
            framealpha=0.9,
            facecolor='white',
            edgecolor='black'
        )
        
        ax.set_title("Facturación vs. Mes (últimos 12 meses)", fontsize=18, pad=15)
        ax.set_xlabel("Mes", fontsize=14, labelpad=10)
        ax.set_ylabel("Facturación calculada", fontsize=14, labelpad=10)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        st.pyplot(fig)

    with col8:       
        st.subheader("Facturación mensual (estado: Completado)")

        df_resumen = df_ventas_tiempo[df_ventas_tiempo['estado'] == 'Completado'].copy()
        df_resumen["anio"] = df_resumen["anio"].astype(int)
        df_resumen["mes"] = df_resumen["mes"].astype(int)
        df_resumen["fecha"] = pd.to_datetime(df_resumen["anio"].astype(str) + "-" + df_resumen["mes"].astype(str) + "-01")

        # Obtener últimos 12 meses
        ultimos_fechas = (
            df_resumen[["periodo_corto", "fecha"]]
            .drop_duplicates()
            .sort_values("fecha")
            .tail(12)
        )
        ultimos_12m = df_resumen[df_resumen["fecha"].isin(ultimos_fechas["fecha"])]

        ordenes_mensuales = (
            ultimos_12m
            .groupby(["periodo_corto", "fecha"])["total_facturado_calculado"]
            .sum()
            .reset_index()
            .sort_values("fecha")
        )

        fig, ax = plt.subplots(figsize=(8, 6))

        # Barras
        sns.barplot(
            data=ordenes_mensuales,
            x="periodo_corto",
            y="total_facturado_calculado",
            palette="crest",
            ax=ax
        )

        # Crear eje numérico para x (0 a 11)
        x = np.arange(len(ordenes_mensuales))
        y = ordenes_mensuales["total_facturado_calculado"].values

        # Ajuste polinomial grado 3 para suavizar
        coef = np.polyfit(x, y, 3)
        polinomio = np.poly1d(coef)
        y_ajustado = polinomio(x)

        # Graficar curva tendencia
        ax.plot(ordenes_mensuales["periodo_corto"], y_ajustado, color='red', linestyle='--', linewidth=2, label='Tendencia')

        # Leyenda
        ax.legend()

        ax.set_title("Facturación efectiva vs. Mes", fontsize=18, pad=15)
        ax.set_xlabel("Mes", fontsize=14, labelpad=15)
        ax.set_ylabel("Facturación calculada", fontsize=14, labelpad=15)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

        plt.tight_layout()
        st.pyplot(fig)

    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Volumen ventas por categoría")
        fig9, ax9 = plt.subplots(figsize=(8, 6))

        categoria_ventas = df_productos.groupby("categoria_nombre")["total_vendido"].sum().reset_index()
        categoria_ventas = categoria_ventas.sort_values(by="total_vendido", ascending=False)

        sns.barplot(
            data=categoria_ventas,
            x="categoria_nombre",
            y="total_vendido",
            palette="viridis",
            ax=ax9
        )

        ax9.set_xticklabels(ax9.get_xticklabels(), rotation=30, ha='right')

        ax9.set_title("Volumen ventas vs. categoría", fontsize=16, pad=15)
        ax9.set_xlabel("Categoría", fontsize=14, labelpad=10)
        ax9.set_ylabel("Volumen total vendido", fontsize=14, labelpad=10)

        plt.tight_layout()
        st.pyplot(fig9)
    
    with col4:
        st.subheader("Facturación por categoría")
        fig10, ax10 = plt.subplots(figsize=(8, 6))

        categoria_ingresos = df_productos.groupby("categoria_nombre")["ingresos_totales"].sum().reset_index()
        categoria_ingresos = categoria_ingresos.sort_values(by="ingresos_totales", ascending=False)

        sns.barplot(
            data=categoria_ingresos,
            x="categoria_nombre",
            y="ingresos_totales",
            palette="viridis",
            ax=ax10
        )

        ax10.set_xticklabels(ax10.get_xticklabels(), rotation=30, ha='right')

        ax10.set_title("Facturación vs. categoría", fontsize=16, pad=15)
        ax10.set_xlabel("Categoría", fontsize=14, labelpad=10)
        ax10.set_ylabel("Ingreso", fontsize=14, labelpad=10)

        plt.tight_layout()
        st.pyplot(fig10)

with tab3:
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Cantidad de órdenes")

        df_resumen = df_ventas_tiempo.copy()
        df_resumen["anio"] = df_resumen["anio"].astype(int)
        df_resumen["mes"] = df_resumen["mes"].astype(int)
        df_resumen["fecha"] = pd.to_datetime(df_resumen["anio"].astype(str) + "-" + df_resumen["mes"].astype(str) + "-01")

        ultimos_fechas = (
            df_resumen[["periodo_corto", "fecha"]]
            .drop_duplicates()
            .sort_values("fecha")
            .tail(12)
        )
        ultimos_12m = df_resumen[df_resumen["fecha"].isin(ultimos_fechas["fecha"])]
        ordenes_mensuales = (
            ultimos_12m
            .groupby(["periodo_corto", "fecha", "anio"])["total_cantidad_ordenes"]
            .sum()
            .reset_index()
            .sort_values("fecha")
        )

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            data=ordenes_mensuales,
            x="periodo_corto",
            y="total_cantidad_ordenes",
            palette="crest",
            ax=ax
        )

        media_2024 = ordenes_mensuales.loc[ordenes_mensuales['anio'] == 2024, 'total_cantidad_ordenes'].mean()
        media_2025 = ordenes_mensuales.loc[ordenes_mensuales['anio'] == 2025, 'total_cantidad_ordenes'].mean()

        media_2024_line = [
            media_2024 if anio == 2024 else None
            for anio in ordenes_mensuales["anio"]
        ]

        media_2025_line = [
            media_2025 if anio == 2025 else None
            for anio in ordenes_mensuales["anio"]
        ]

        ax.plot(ordenes_mensuales["periodo_corto"], media_2024_line, color='red', linestyle='--', label=f'Media 2024: {media_2024:.1f}')
        ax.plot(ordenes_mensuales["periodo_corto"], media_2025_line, color='blue', linestyle='--', label=f'Media 2025: {media_2025:.1f}')

        ax.legend(
            loc='upper right',
            fontsize=12,
            frameon=True,             
            framealpha=0.9,            
            facecolor='white',          
            edgecolor='black'         
        )
        ax.set_title("Órdenes mensuales (últimos 12 meses)", fontsize=18, pad=15)
        ax.set_xlabel("Mes", fontsize=14, labelpad=10)
        ax.set_ylabel("Cantidad de órdenes", fontsize=14, labelpad=10)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

    with col6:
        st.subheader("Total unidades vendidas")

        df_resumen = df_ventas_tiempo.copy()
        df_resumen["anio"] = df_resumen["anio"].astype(int)
        df_resumen["mes"] = df_resumen["mes"].astype(int)
        df_resumen["fecha"] = pd.to_datetime(df_resumen["anio"].astype(str) + "-" + df_resumen["mes"].astype(str) + "-01")

        ultimos_fechas = (
            df_resumen[["periodo_corto", "fecha"]]
            .drop_duplicates()
            .sort_values("fecha")
            .tail(12)
        )
        ultimos_12m = df_resumen[df_resumen["fecha"].isin(ultimos_fechas["fecha"])]

        unidades_mensuales = (
            ultimos_12m
            .groupby(["periodo_corto", "fecha", "anio"])["total_unidades_vendidas"]
            .sum()
            .reset_index()
            .sort_values("fecha")
        )

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            data=unidades_mensuales,
            x="periodo_corto",
            y="total_unidades_vendidas",
            palette="crest",
            ax=ax
        )

        media_2024 = unidades_mensuales.loc[unidades_mensuales['anio'] == 2024, 'total_unidades_vendidas'].mean()
        media_2025 = unidades_mensuales.loc[unidades_mensuales['anio'] == 2025, 'total_unidades_vendidas'].mean()

        media_2024_line = [
            media_2024 if anio == 2024 else None
            for anio in unidades_mensuales["anio"]
        ]

        media_2025_line = [
            media_2025 if anio == 2025 else None
            for anio in unidades_mensuales["anio"]
        ]

        ax.plot(unidades_mensuales["periodo_corto"], media_2024_line, color='red', linestyle='--', label=f'Media 2024: {media_2024:.1f}')
        ax.plot(unidades_mensuales["periodo_corto"], media_2025_line, color='blue', linestyle='--', label=f'Media 2025: {media_2025:.1f}')

        ax.legend(
            loc='upper right',
            fontsize=12,
            frameon=True,
            framealpha=0.9,
            facecolor='white',
            edgecolor='black'
        )

        ax.set_title("Unidades vendidas mensuales (últimos 12 meses)", fontsize=18, pad=15)
        ax.set_xlabel("Mes", fontsize=14, labelpad=10)
        ax.set_ylabel("Total unidades vendidas", fontsize=14, labelpad=10)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

        plt.tight_layout()
        st.pyplot(fig)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ventas por categoría")

        fig1, ax1 = plt.subplots(figsize=(8, 6))  # tamaño similar a tu otro gráfico

        # Agrupar y ordenar de forma descendente para que se vea mejor (opcional)
        ventas_categoria = df_compras.groupby("categoria_nombre")["subtotal"].sum().sort_values(ascending=True)

        # Gráfico de barras horizontales con paleta viridis usando seaborn para homogeneidad
        sns.barplot(x=ventas_categoria.values, y=ventas_categoria.index, ax=ax1, palette="viridis")

        # Etiquetas y título con tamaño y padding para mejor presentación
        ax1.set_xlabel("Subtotal acumulado", fontsize=14, labelpad=15)
        ax1.set_ylabel("Categoría", fontsize=14, labelpad=15)
        ax1.set_title("Ventas por categoría", fontsize=18, pad=15)

        plt.tight_layout()
        st.pyplot(fig1)
        #st.subheader("Ventas por categoría")
        #fig1, ax1 = plt.subplots()
        #df_compras.groupby("categoria_nombre")["subtotal"].sum().sort_values().plot(kind="barh", ax=ax1)
        #ax1.set_xlabel("Subtotal acumulado")
        #st.pyplot(fig1)

    with col2:
        st.subheader("Cantidad vendida por producto")
        fig2, ax2 = plt.subplots(figsize=(8, 6))

        vendidos = df_compras.groupby("producto_nombre")["cantidad"].sum().sort_values(ascending=False).head(15)

        # Usamos seaborn para el barplot con paleta viridis para consistencia
        sns.barplot(x=vendidos.index, y=vendidos.values, ax=ax2, palette="viridis")

        # Etiquetas y título con tamaño y pad
        ax2.set_ylabel("Cantidad vendida", fontsize=14, labelpad=15)
        ax2.set_xlabel("Producto", fontsize=14, labelpad=15)
        ax2.set_title("Top productos por unidades vendidas", fontsize=18, pad=15)

        # Mejorar etiquetas del eje x para que no se monten
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=10)

        plt.tight_layout()
        st.pyplot(fig2)
      #  st.subheader("Cantidad vendida por producto")
       # fig2, ax2 = plt.subplots(figsize=(10, 5))
       # vendidos = df_compras.groupby("producto_nombre")["cantidad"].sum().sort_values(ascending=False).head(15)
       # vendidos.plot(kind="bar", ax=ax2)
       # ax2.set_ylabel("Cantidad vendida")
       # ax2.set_title("Top productos por unidades vendidas")
       # plt.xticks(rotation=45, ha='right')
       # st.pyplot(fig2)

    st.subheader("Tabla de ventas")

    column_map = {
    "detalleid":"DetalleID",   
    "ordenid": "OrdenID",
    "estado":"Estado",
    "cantidad": "Cantidad",
    "productoid":"ProductoID",
    "producto_nombre": "Producto Nombre",
    "preciounitario": "Precio Unitario",
    "subtotal": "Subtotal",
    "categoria_nombre": "Categoría Nombre",
    "segmento_precio": "Segmento Precio",
    "fechaorden": "Fecha Orden",
    "usuarioid": "UsuarioID",
    "total_orden": "Total Orden",
    "porcentaje_del_total": "Porcentaje" 
    }

    df_para_mostrar = df_compras.rename(columns=column_map)
    st.dataframe(df_para_mostrar)

with tab4:
    st.header("Análisis de productos")

    col1, col3 = st.columns(2)

    with col1:
        st.subheader("Productos más vendidos")
        fig6, ax6 = plt.subplots(figsize=(8, 6))

        productos_con_ventas = df_productos[df_productos["total_vendido"] > 0]
        top_productos = productos_con_ventas.nlargest(10, "total_vendido")
        
        sns.barplot(data=top_productos, y="nombre", x="total_vendido", ax=ax6, palette="viridis")
        ax6.set_title("Top 10",fontsize=18, pad=15)
        ax6.set_ylabel("Producto", fontsize=14, labelpad=15)
        ax6.set_xlabel("Volumen total vendido", fontsize=14, labelpad=15)
        ax6.set_yticklabels(ax6.get_yticklabels())  
        plt.tight_layout()
        st.pyplot(fig6)
    with col3:
        st.subheader("Cantidad de stock por producto")
        fig3, ax3 = plt.subplots(figsize=(8, 6))  # Aumentamos un poco la altura para las etiquetas

        stock = df_productos.set_index("nombre")["stock"].sort_values(ascending=False).head(15)

        sns.barplot(x=stock.index, y=stock.values, ax=ax3, palette="viridis")

        ax3.set_ylabel("Stock disponible", fontsize=14, labelpad=15)
        ax3.set_xlabel("Producto", fontsize=14, labelpad=15)
        ax3.set_title("Productos con más stock", fontsize=18, pad=15)

        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right', fontsize=10)

        plt.tight_layout()
        st.pyplot(fig3)
   
    col2, col4 = st.columns(2)

    with col2:
        st.subheader("Calificaciones - Distribución del promedio")
        fig7, ax7 = plt.subplots(figsize=(8, 6))

        productos_calificados = df_productos[df_productos["calificacion_promedio"] > 0]

        media = productos_calificados["calificacion_promedio"].mean()
        desviacion = productos_calificados["calificacion_promedio"].std()

        sns.histplot(productos_calificados["calificacion_promedio"], bins=16, ax=ax7)
        sns.kdeplot(productos_calificados["calificacion_promedio"], ax=ax7, color="darkblue", linestyle="--", linewidth=2)

        ax7.set_title("Calificaciones (promedio)", fontsize=18, pad=15)
        ax7.set_ylabel("Cantidad", fontsize=14, labelpad=15)
        ax7.set_xlabel("Calificación promedio", fontsize=14, labelpad=15)
        ax7.text( 0.98, 0.95,
            f"Media: {media:.2f}\nDesv. Est.: {desviacion:.2f}",
            transform=ax7.transAxes,
            fontsize=12,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray", alpha=0.7)
        )
        plt.tight_layout()
        st.pyplot(fig7)

    st.subheader("Calificación y Precio")

    with col4:
        st.subheader("Total de órdenes por producto")
        fig4, ax4 = plt.subplots(figsize=(8, 6))  # Un poco más alto para las etiquetas

        ordenes = df_compras.groupby("producto_nombre")["ordenid"].nunique().sort_values(ascending=False).head(15)

        sns.barplot(x=ordenes.index, y=ordenes.values, ax=ax4, palette="viridis")

        ax4.set_ylabel("Cantidad de órdenes", fontsize=14, labelpad=10)
        ax4.set_xlabel("Producto", fontsize=14, labelpad=10)
        ax4.set_title("Productos con más órdenes únicas", fontsize=18, pad=15)

        ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha='right', fontsize=10)

        plt.tight_layout()
        st.pyplot(fig4)
     
    # Crear figura y eje
    fig8, ax8 = plt.subplots(figsize=(10, 6))  # Más ancho para dar espacio a la leyenda

    # Filtrar productos válidos
    productos_scatter = df_productos[df_productos["calificacion_promedio"] > 0]

    # Dibujar scatterplot
    sns.scatterplot(
        data=productos_scatter,
        x="precio",
        y="calificacion_promedio",
        hue="categoria_nombre",
        palette="viridis",
        ax=ax8
    )

    # Títulos y etiquetas
    ax8.set_title("Precio vs Calificación Promedio", fontsize=14, pad=15)
    ax8.set_xlabel("Precio", fontsize=12, labelpad=10)
    ax8.set_ylabel("Calificación Promedio", fontsize=12, labelpad=10)
    ax8.grid(True, linestyle=':')
    ax8.set_facecolor('#f5f5f5')  # Gris muy claro, por ejemplo

    # Leyenda a la izquierda del gráfico, fuera del área de datos
    ax8.legend(
        bbox_to_anchor=(-0.4, 0.5),  # -0.4 a la izquierda del eje y 0.5 (centro vertical)
        loc="center left",
        borderaxespad=0.
    )

    # Aumentar espacio a la izquierda para la leyenda
    fig8.subplots_adjust(left=0.1)

    # Mostrar en Streamlit
    st.pyplot(fig8)

    st.subheader("Tabla - Métricas productos")

    columnas_importantes = ['nombre', 'categoria_nombre', 'precio', 'stock', 'total_vendido', 
                          'ingresos_totales', 'calificacion_promedio', 'total_reseñas', 
                          'categoria_ventas', 'categoria_calificacion']
    renombrar_cols = {
    'nombre': 'Nombre',
    'categoria_nombre': 'Categoría',
    'precio': 'Precio',
    'stock': 'Stock',
    'total_vendido': 'Total Ventas',
    'ingresos_totales': 'Total Ingresos',
    'calificacion_promedio': 'Calificación Promedio',
    'total_reseñas': 'Total Reseñas',
    'categoria_ventas': 'Categoría Ventas',
    'categoria_calificacion': 'Categoría Calificación'
}

    df_mostrar = df_productos[columnas_importantes].rename(columns=renombrar_cols)
    num_filas = df_productos.shape[0]
    print("Número de filas:", num_filas)

    st.dataframe(df_mostrar)