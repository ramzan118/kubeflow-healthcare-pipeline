import kfp
from kfp import dsl
from kfp.components import InputPath, OutputPath, create_component_from_func

# Dummy data processing component
@create_component_from_func
def preprocess_data(
    input_data_path: InputPath('CSV'),
    processed_data_path: OutputPath('CSV')
):
    import pandas as pd
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Reading data from: {input_data_path}")
    df = pd.read_csv(input_data_path)

    # Simple preprocessing: one-hot encode gender, scale cost
    df['gender_Male'] = (df['gender'] == 'Male').astype(int)
    df['gender_Female'] = (df['gender'] == 'Female').astype(int)
    df['scaled_treatment_cost'] = df['treatment_cost'] / 1000.0

    df = df.drop(columns=['gender', 'patient_id']) # Drop original gender and ID

    logging.info(f"Processed data head:\n{df.head()}")
    df.to_csv(processed_data_path, index=False)
    logging.info(f"Processed data written to: {processed_data_path}")

# Dummy model training component
@create_component_from_func
def train_model(
    processed_data_path: InputPath('CSV'),
    model_path: OutputPath('PKL')
):
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    import joblib
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Reading processed data from: {processed_data_path}")
    df = pd.read_csv(processed_data_path)

    # Simple model: predict scaled_treatment_cost based on age, gender, diagnosis (one-hot encoded)
    # For a real project, you'd properly handle categorical features like 'diagnosis'
    features = ['age', 'gender_Male', 'gender_Female']
    
    # Handle 'diagnosis' column - for simplicity, let's just drop it for this dummy model
    # In a real scenario, you'd one-hot encode or embed it.
    if 'diagnosis' in df.columns:
        df = df.drop(columns=['diagnosis'])

    X = df[features]
    y = df['scaled_treatment_cost']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    logging.info("Model trained successfully.")
    joblib.dump(model, model_path)
    logging.info(f"Model saved to: {model_path}")

# Dummy model evaluation component
@create_component_from_func
def evaluate_model(
    model_path: InputPath('PKL'),
    processed_data_path: InputPath('CSV'),
    metrics_path: OutputPath('JSON')
):
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error, r2_score
    import joblib
    import json
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Loading model from: {model_path}")
    model = joblib.load(model_path)

    logging.info(f"Reading processed data from: {processed_data_path}")
    df = pd.read_csv(processed_data_path)

    features = ['age', 'gender_Male', 'gender_Female']
    
    # Ensure features exist, if diagnosis was dropped in training
    if 'diagnosis' in df.columns:
        df = df.drop(columns=['diagnosis'])

    X = df[features]
    y_true = df['scaled_treatment_cost']

    y_pred = model.predict(X)

    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    metrics = {
        'mse': mse,
        'r2_score': r2
    }
    logging.info(f"Model evaluation metrics: {metrics}")

    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)
    logging.info(f"Metrics saved to: {metrics_path}")

# Define the Kubeflow Pipeline
@dsl.pipeline(
    name='Healthcare Data ML Pipeline',
    description='A pipeline to preprocess healthcare data, train, and evaluate a model.'
)
def healthcare_ml_pipeline(
    data_input_gcs_uri: str
):
    # Download data from GCS using a ContainerOp with google/cloud-sdk image
    download_data_op = dsl.ContainerOp(
        name='download-data',
        image='google/cloud-sdk:latest', # Using a GCS-enabled image
        command=['sh', '-c'],
        arguments=[f'gsutil cp {data_input_gcs_uri} /tmp/healthcare_data.csv'],
        file_outputs={
            'data': '/tmp/healthcare_data.csv'
        }
    )

    preprocess_task = preprocess_data(
        input_data=download_data_op.outputs['data']
    ).add_pod_annotation(
        name="gke.cloud.google.com/observability-mode", value="true" # Enable GKE metrics for this pod
    )

    train_task = train_model(
        processed_data=preprocess_task.outputs['processed_data']
    ).add_pod_annotation(
        name="gke.cloud.google.com/observability-mode", value="true"
    )

    evaluate_task = evaluate_model(
        model=train_task.outputs['model'],
        processed_data=preprocess_task.outputs['processed_data']
    ).add_pod_annotation(
        name="gke.cloud.google.com/observability-mode", value="true"
    )

# Compile the pipeline
if __name__ == '__main__':
    # Ensure necessary libraries are available for component creation (e.g., pandas, scikit-learn, joblib)
    # These will be automatically included in the component's Docker image by KFP's `create_component_from_func`
    kfp.compiler.Compiler().compile(healthcare_ml_pipeline, 'healthcare_ml_pipeline.yaml')
