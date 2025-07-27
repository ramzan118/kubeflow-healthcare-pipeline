import pandas as pd
import os
from kfp.v2.dsl import component

@component
def process_healthcare_data(input_path: str, output_path: str) -> str:
    print(f"Processing healthcare data from {input_path}")
    
    # Verify file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    try:
        df = pd.read_csv(input_path)
        print(f"Loaded {len(df)} records")
        
        # Dummy processing - calculate risk score
        df['risk_score'] = df.apply(lambda row: 
            (row['age'] * 0.1) + 
            (10 if 'Hypertension' in row['diagnosis'] else 0) +
            (20 if 'HeartDisease' in row['diagnosis'] else 0), axis=1)
        
        # Save results
        df.to_csv(output_path, index=False)
        print(f"Saved processed data to {output_path}")
        
        return f"Processed {len(df)} records successfully"
    except Exception as e:
        print(f"Data processing failed: {str(e)}")
        raise
