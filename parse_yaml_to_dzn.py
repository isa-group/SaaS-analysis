from scripts.PricingsLoader import PricingsLoader
import google.generativeai as genai
from google.generativeai import GenerationConfig
from tqdm import tqdm
import os
import time

dataset = PricingsLoader('./pricings/yaml')
        
def _make_request(prompt:str) -> str:
    
    genai.configure(api_key=os.getenv('GOOGLE_AI_STUDIO'))
    model = 'gemini-1.5-flash'
    config = GenerationConfig(temperature=0.0)
    response = genai.GenerativeModel(model, generation_config=config).generate_content(contents=[prompt])
    
    return response.text
    

def _generate_prompt(pricing: str):
    return f"""
    Quiero que te conviertas en una herramienta de transformación entre la sintaxis Pricing2Yaml y los archivos .dzn que modelan un pricing para operar con el en un solver CSP como MiniZinc. A continuación, voy a darte las indicaciones de cómo realizar la transformación.

    Los mensajes que recibirás tendrán como parte de su contenido un archivo YAML con una estructura similar a la siguiente:

    ```
    saasName: Test
    version: "2.0"
    createdAt: 2024-01-15
    currency: EUR
    hasAnnualPayment: false
    features:
    feature1:
        description: Feature 1 description
        valueType: BOOLEAN
        defaultValue: true
        type: DOMAIN
    feature2:
        description: Feature 2 description
        valueType: BOOLEAN
        defaultValue: false
        type: DOMAIN
    feature3:
        description: Feature 3 description
        valueType: BOOLEAN
        defaultValue: false
        type: DOMAIN
    feature4:
        description: Feature 4 description
        valueType: BOOLEAN
        defaultValue: false
        type: DOMAIN
    usageLimits:
    limitOfFeature1:
        description: ''
        valueType: NUMERIC
        defaultValue: 2
        unit: use/month
        type: RENEWABLE
        linkedFeatures:
        - feature1
    limitOfFeature4:
        description: ''
        valueType: NUMERIC
        defaultValue: 0
        unit: use/month
        type: RENEWABLE
        linkedFeatures:
        - feature4
    plans:
    BASIC:
        description: Basic plan
        price: 0.0
        unit: user/month
        features: null
        usageLimits: null
    PRO:
        description: Advanced plan
        price: 35.0
        unit: user/month
        features:
        feature2:
            value: true
        usageLimits:
        limitOfFeature1:
            value: 5
    addOns:
    feature3Addon:
        description: ADDON description
        availableFor:
        - BASIC
        - PRO
        price: 15.95
        unit: user/month
        features:
        feature3:
            value: true
    feature4Addon:
        description: ADDON description
        availableFor:
        - BASIC
        - PRO
        dependsOn:
        - feature3Addon
        price: 20.95
        unit: user/month
        features:
        feature4:
            value: true
        usageLimits:
        limitOfFeature4:
            value: 3
        usageLimitsExtensions:
        limitOfFeature1:
            value: 2
    ```

    Para entender la sintaxis, lo único que debes tener en cuenta es lo siguiente:

    1. Toda feature que no esté listada dentro del atributo "features" de un plan, debes considerar que está incluida, pero que su "value" corresponde al "defaultValue" que se define arriba.

    2. Idem para los límites de uso de los planes.

    3. En cuanto a los add-ons, funciona distinto, todo límite de uso o feature que no esté dentro de un add-on se considerará como que no está incluida en éste (para el caso de las features), o que su valor es 0 (para el caso de los límites de uso)

    Tu tarea, por tanto, consiste en trasformar de este tipo de YAMLs a esta estructura de archivo .dzn, que debes devolver como respuesta:

    ```
    FEATURES = {{feature1, feature2, feature3, feature4}};
    USAGE_LIMITS = {{limitOfFeature1,limitOfFeature4}};
    PLANS = {{BASIC, PRO}};
    ADDONS = {{feature3Addon,feature4addon}};

    plans_prices = [0.0,35.0];
    addons_prices = [15.95,20.95];

    plans_features = array2d(PLANS, FEATURES, [
        % BASIC
        1, 0, 0, 0,
        % PRO
        1, 1, 0, 0
    ]);
    plans_usage_limits = array2d(PLANS, USAGE_LIMITS, [
        % BASIC
        2,0,
        % PRO
        5,0
    ]);

    linked_features = array2d(USAGE_LIMITS, FEATURES, [
        % limitOfFeature1
        1,0,0,0,
        % limitOfFeature4
        0,0,0,1
    ]);

    addons_features = array2d(ADDONS, FEATURES, [
        % feature3Addon
        0,0,1,0,
        % feature4Addon
        0,0,0,1
    ]);
    addons_usage_limits = array2d(ADDONS, USAGE_LIMITS, [
        % feature3Addon
        0,0,
        % feature4Addon
        0,3
    ]);
    addons_usage_limits_extensions = array2d(ADDONS, USAGE_LIMITS, [
        % feature3Addon
        0,0,
        % feature4Addon
        2,0
    ]);
    addons_available_for = array2d(ADDONS, PLANS, [
        % feature3Addon
        1,1,
        % feature4Addon
        1,1
    ]);

    addons_depends_on = array2d(ADDONS, ADDONS, [
        % feature3Addon
        0,0,
        % feature4Addon
        1,0
    ]);

    Te explico a continuación a qué corresponde cada campo para que sepas como construir la salida:

    - FEATURES: Listado de nombres de features, escritos sin comillas y entre llaves separados por comas.

    - USAGE_LIMITS: Listado de nombres de límites de uso, escritos sin comillas y entre llaves separados por comas.

    - PLANS: Listado de nombres de planes, escritos sin comillas y entre llaves separados por comas.

    - ADDONS: Listado de nombres de addons, escritos sin comillas y entre llaves separados por comas.

    - plan_prices: listado de precios de cada plan, escritos entre corchetes y como floats. Cada elemento debe estar en la posición correspondiente a su plan en el listado PLANS.

    - addons_prices: listado de precios de cada add-on, escritos entre corchetes y como floats. Cada elemento debe estar en la posición correspondiente a su plan en el listado ADDONS.

    - plans_features: array bidimensional con dimensiones PLANSxFEATURES donde la posición (i,j) indica con 0 o 1 si la feature j está disponible en el plan i. Para facilitar la lectura, debes indicar con comentarios el nombre de un plan antes de poner sus features permitidas. IMPORTANTE: de ahora en adelante, debes considerar que una feature esta incluida en un plan (i.e. su valor en el array es 1) si su value, o defaultValue en ausencia de éste, es true, o si su valueType es TEXT. En caso contrario, el valor del array debe ser 0.

    - plans_usage_limits: array bidimensional con dimensiones PLANSxUSAGE_LIMITS donde la posición (i,j) indica con un número natural o 0 el valor del usage-limit j en el plan i. Para facilitar la lectura, debes indicar con comentarios el nombre de un plan antes de poner los valores de los usage limits.

    - linked_features: array bidimensional con dimensiones USAGE_LIMITSxFEATURES donde la posición (i,j) indica con 0 o 1 si la feature j está vinculada al usage limit i. Para facilitar la lectura, debes indicar con comentarios el nombre de un usage limit antes de poner los valores para cada feature.

    - addons_features: array bidimensional con dimensiones ADDONSxFEATURES donde la posición (i,j) indica con 0 o 1 si la feature j está disponible en el addon i. Para facilitar la lectura, debes indicar con comentarios el nombre del addon antes de poner sus features incluídas.

    - addons_usage_limits: array bidimensional con dimensiones ADDONSxUSAGE_LIMITS donde la posición (i,j) indica con un número natural o 0 el valor del usage limit j en el addon i. Para facilitar la lectura, debes indicar con comentarios el nombre del addon antes de poner los valores de los usage limits.

    - addons_usage_limits_extensions: array bidimensional con dimensiones ADDONSxUSAGE_LIMITS donde la posición (i,j) indica con un número natural o 0 el valor del usage limit extension j en el addon i. Para facilitar la lectura, debes indicar con comentarios el nombre del addon antes de poner los valores de los usage limits extensions.

    - addons_available_for: array bidimensional con dimensiones ADDONSxPLANS donde la posición (i,j) indica con 0 o 1 si el add-on i está disponible para el plan j. Para facilitar la lectura, debes indicar con comentarios el nombre del addon antes de poner su disponibilidad para cada plan.

    - addons_depends_on: array bidimensional con dimensiones ADDONSxADDONS donde la posición (i,j) indica con 0 o 1 si el add-on i depende del addon j. Para facilitar la lectura, debes indicar con comentarios el nombre del addon i antes de poner sus dependencias con el resto de addons.

    Ahora una vez que entiendes como funcionan ambas estructuras y tu tarea: recibir un archivo con la estructura Pricing2Yaml en el input y devolver su equivalente en .dzn, quiero que realices la trasformación para este Pricing2Yaml:

    {pricing}
    """

def _write_response(response, path):
    # Giving a path like ./pricings/yaml/2020/quip.yml, this method saves the response in a .dzn file like ./pricings/dzn/2020/quip.dzn (create all folders if they don't exist)

    # Replace 'yaml' with 'dzn' in the path and change the extension to '.dzn'
    dzn_path = path.replace('/yaml/', '/dzn/').replace('.yml', '.dzn')
    
    # Extract the directory from the dzn path
    dzn_directory = os.path.dirname(dzn_path)
    
    # Create all directories if they don't exist
    os.makedirs(dzn_directory, exist_ok=True)
    
    # Save the response content to the dzn file
    with open(dzn_path, 'w') as file:
        file.write(response)

def _process_response(response):
    return response.replace('`', '').strip()
        
if __name__ == '__main__':
    for i in tqdm(range(len(dataset))):
        if i % 15 == 0 and i!= 0:
            time.sleep(30)
        path = dataset.get_path(i)
        
        with open(path, 'r') as file:
            pricing = file.read()
            prompt = _generate_prompt(pricing)
            response = _make_request(prompt)
            processed_response = _process_response(response)
            _write_response(processed_response, path)