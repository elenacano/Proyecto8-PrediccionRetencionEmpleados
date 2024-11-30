import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Configuración de la página
st.set_page_config(
    page_title="Predicción de precios de casas",
    page_icon="🏡",
    layout="centered",
)

def load_models():
    with open('/Users/Elena/OneDrive/Desktop/Hackio/Modulos/Modulo8/Proyecto7-PrediccionCasas/Modelo1/datos/preprocesamiento/one_hot_encoder.pkl', 'rb') as f:
        one_hot_encoder = pickle.load(f)
    with open('/Users/Elena/OneDrive/Desktop/Hackio/Modulos/Modulo8/Proyecto7-PrediccionCasas/Modelo1/datos/preprocesamiento/target_encoder.pkl', 'rb') as f:
        target_encoder = pickle.load(f)
    with open('/Users/Elena/OneDrive/Desktop/Hackio/Modulos/Modulo8/Proyecto7-PrediccionCasas/Modelo1/datos/preprocesamiento/standar_scaler.pkl', 'rb') as f:
        standar_scaler = pickle.load(f)
    with open('/Users/Elena/OneDrive/Desktop/Hackio/Modulos/Modulo8/Proyecto7-PrediccionCasas/Modelo1/datos/modelos/modelo_prediccion_final.pkl', 'rb') as f:
        model = pickle.load(f)
    return one_hot_encoder, target_encoder, standar_scaler, model

one_hot_encoder, target_encoder, standar_scaler, model = load_models()




# Inyectar CSS para cambiar el fondo de la aplicación
st.markdown(
    """
    <style>
    body {
    font-family: 'Roboto', sans-serif;
    }
    .stApp {
        background-color: #ADC2CD; /* Fondo rosa oscuro */
    }
    .prediction-text {
        font-size: 36px;
        text-align: center;
        color: #2d6a4f;
        font-weight: bold;
    }
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título y descripción
st.title("Precios de alquileres en Madrid")
st.write("Averigua donde están los alquileres más baratos!!")

# Imagen
st.image(
    "https://fincaraiz.com.co/blog/wp-content/uploads/2022/08/casas-modernas-1-1920x1130.jpg",
    caption="Tu próxima casa",
    use_container_width=True,
)


col1, col2, col3 = st.columns(3)

with col1:
    # Selección del barrio

    

    property_type = st.selectbox(
        "Tipo de propiedad",
        ["Flat", "Studio", "Duplex", "Other"]
    )
    st.write(f"Tipo de propiedad: {property_type}")

    # Selección del tipo de piso
    floor = st.selectbox(
        "Piso",
        ['3', 'bj', '2', '1', '5', 'en', '4', 'st', '8', '7', '6', '14', 'ss']
    )
    st.write(f"Piso: {floor}")

    municipality = st.selectbox(
        "Municipio",
        [
            'Madrid', 'San Sebastián de los Reyes', 'Villamanrique de Tajo',
            'Rascafría', 'Manzanares el Real', 'Miraflores de la Sierra',
            'Galapagar', 'Arganda', 'San Lorenzo de el Escorial',
            'Aldea del Fresno', 'Aranjuez', 'Villanueva del Pardillo',
            'Las Rozas de Madrid', 'Navalcarnero', 'Alcalá de Henares',
            'El Escorial', 'Leganés', 'Coslada', 'Torrejón de Ardoz',
            'Camarma de Esteruelas', 'Alcorcón', 'Pinto', 'Valdemoro',
            'Collado Villalba', 'Getafe', 'Paracuellos de Jarama', 'El Molar',
            'Parla', 'Tres Cantos', 'Quijorna', 'Valdemorillo', 'Pedrezuela',
            'Daganzo de Arriba', 'Guadarrama', 'Cobeña', 'El Álamo', 'Algete',
            'Rivas-Vaciamadrid', 'Los Santos de la Humosa',
            'San Fernando de Henares', 'Fuenlabrada', 'Mataelpino',
            'Villa del Prado', 'Los Molinos', 'Colmenar Viejo', 'Móstoles',
            'Navalafuente', 'Meco', 'Robledo de Chavela', 'Campo Real',
            'Villaviciosa de Odón', 'Pozuelo de Alarcón', 'Bustarviejo',
            'Collado Mediano', 'Chinchón', 'Colmenarejo', 'Loeches',
            'Sevilla la Nueva', 'Serranillos del Valle', 'Torrelaguna',
            'Villalbilla', 'Alcobendas'
        ]
    )
    st.write(f"Municipio seleccionado: {municipality}")



with col2:
    size = st.number_input(
        "Tamaño (m²)",
        min_value=0.0,  # Valor mínimo
        step=0.1        # Incremento
    )
    st.write(f"Tamaño: {size} m²")

    # Entrada del número de habitaciones
    rooms = st.number_input(
        "Número de habitaciones",
        min_value=1,    # Valor mínimo
        step=1          # Incremento
    )
    st.write(f"Habitaciones: {rooms}")

    # Entrada del número de baños
    bathrooms = st.number_input(
        "Número de baños",
        min_value=1,    # Valor mínimo
        step=1          # Incremento
    )
    st.write(f"Baños: {bathrooms}")

with col3:
    # Entrada de la distancia
    distance = st.number_input(
        "Distancia al centro (metros))",
        min_value=0.0,  # Valor mínimo
        step=0.1        # Incremento
    )
    st.write(f"A {distance} metros del centro")

    exterior = st.selectbox(
        "Exterior",
         ["Sí", "No"]
    )
    st.write(f"Exterior: {exterior}")
    exterior = exterior == "Sí"

    # Selección del tipo de piso
    has_lift = st.selectbox(
        "¿Tiene ascensor?",
         ["Sí", "No"]
    )
    st.write(f"Ascensor: {has_lift}")
    has_lift = has_lift == "Sí" 



dic_pred = {
    'propertyType':property_type.lower(),
    'size': size,
    'exterior': exterior,
    'rooms': rooms,
    'bathrooms' : bathrooms,
    'municipality' : municipality,
    'distance' : distance,
    'floor' : floor,
    'hasLift' : has_lift
}


if st.button("Predecir"):
    df_pred = pd.DataFrame(dic_pred, index=[0])

    # Hacemos el encoding
    diccionario_encoding={"onehot":["rooms", "bathrooms", "propertyType", "exterior"], "target":['municipality', 'floor', 'hasLift']}
    col_one_hot = diccionario_encoding["onehot"]
    col_target = diccionario_encoding["target"]

    df_pred[col_one_hot] = df_pred[col_one_hot].astype(str)
    encoded_matrix = one_hot_encoder.transform(df_pred[col_one_hot])
    df_ohe = pd.DataFrame(
        encoded_matrix.toarray(),  # Convertir matriz dispersa a densa (si es dispersa)
        columns=one_hot_encoder.get_feature_names_out(col_one_hot)  # Obtener nombres de las columnas
    )
    df_encoded = pd.concat([df_pred.reset_index(drop=True), df_ohe.reset_index(drop=True)], axis=1)
    df_encoded.drop(columns=["rooms", "bathrooms", "propertyType", "exterior", "exterior_False"], inplace=True)

    df_encoded = target_encoder.transform(df_encoded)

    # Estandarizamos
    col_num = df_encoded.select_dtypes(include = np.number).columns
    df_encoded_estand = pd.DataFrame(standar_scaler.transform(df_encoded), columns= col_num)

    df_encoded_estand = df_encoded_estand.rename(columns={col: f"{col}_standar" for col in df_encoded_estand.columns})

    
    #Predicción
    prediction = round(model.predict(df_encoded_estand)[0], 2)

     # Mostrar el resultado de la predicción con estilo personalizado
    st.markdown(f'<p class="prediction-text">El precio estimado del alquiler es: {prediction}€</p>', unsafe_allow_html=True)
    st.balloons()

