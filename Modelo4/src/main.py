from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# Configuración para mostrar todas las columnas
pd.set_option('display.max_columns', None)

# cargamos los transformadores y el modelo entrenado
with open('../datos/modelos/modelo_prediccion_final.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../datos/preprocesamiento/robust_scaler.pkl', 'rb') as f:
    robust_scaler = pickle.load(f)

with open('../datos/preprocesamiento/target_encoder.pkl', 'rb') as f:
    target_encoder = pickle.load(f)

with open('../datos/preprocesamiento/one_hot_encoder.pkl', 'rb') as f:
    one_hot_encoder = pickle.load(f)


# Diccionario para el encoding
diccionario_encoding={"onehot":["Gender", 'JobRole'], "target":['EnvironmentSatisfaction', 'JobSatisfaction', 'WorkLifeBalance', 'BusinessTravel', 'Department', 'EducationField',  'MaritalStatus']}

col_one_hot = diccionario_encoding["onehot"]
col_target = diccionario_encoding["target"]


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()
        df_pred = pd.DataFrame(data, index=[0])

        # --------------------- Primero hacemos el one hot encoder ----------------------
        encoded_matrix = one_hot_encoder.transform(df_pred[col_one_hot])

        df_ohe = pd.DataFrame(
            encoded_matrix.toarray(),  # Convertir matriz dispersa a densa (si es dispersa)
            columns=one_hot_encoder.get_feature_names_out(col_one_hot)  # Obtener nombres de las columnas
        )

        df_encoded = pd.concat([df_pred.reset_index(drop=True), df_ohe.reset_index(drop=True)], axis=1)
        df_encoded.drop(columns=col_one_hot, inplace=True)

        # ------------------------- Después hacemos el target encoder ----------------------
        df_encoded = target_encoder.transform(df_encoded)

        # ----------------------------- Ahora estandarizamos -------------------------------
        col_num = df_encoded.select_dtypes(include = np.number).columns
        df_encoded_estand = pd.DataFrame(robust_scaler.transform(df_encoded), columns= col_num)

        # --------------------------Finalmente hacemos la prediccion ----------------------
        print("________________________PREDICCION___________________________")
        prediccion = model.predict(df_encoded_estand)[0]
        probabilidad = round(model.predict_proba(df_encoded_estand)[0][prediccion]*100, 2)
        attrition = "no" if prediccion==0 else "si"
        print(f"El empleado {attrition.upper()} se va de la empresa con una probabilidad del {probabilidad}%")

        return jsonify({"prediccion":attrition.upper(), "probabilidad":probabilidad})

    except:
        return jsonify({"respuesta":"Ha habido un problema en el envío de los datos"})
    
    
if __name__=="__main__":
    app.run(debug = True)

