from kfp import compiler
from kfp import dsl
import os
import sys

# Add components directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))
from process_data import process_healthcare_data

@dsl.pipeline(name='healthcare-pipeline')
def healthcare_pipeline(
    input_path: str = '/app/data/patients.csv',
    output_path: str = '/app/data/processed_data.csv'
):
    process_task = process_healthcare_data(
        input_path=input_path,
        output_path=output_path
    )

def main():
    print("Starting pipeline compilation...")
    try:
        compiler.Compiler().compile(
            pipeline_func=healthcare_pipeline,
            package_path='healthcare_ml_pipeline.yaml'
        )
        print("Pipeline compiled successfully!")
        return 0
    except Exception as e:
        print(f"Pipeline compilation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
