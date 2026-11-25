import pandas as pd
import os

uploaded_path = r"C:/Users/Siva Santhiya/.gemini/antigravity/brain/80f9dc9b-c986-4148-a6f3-88cd1e9b26a2/.user_uploaded/media_1795579702667_a1ff2b0c.csv"

df_uploaded = pd.read_csv(uploaded_path)
print(f"Uploaded shape: {df_uploaded.shape}")
print(df_uploaded.head())

if os.path.exists("submission.csv"):
    df_sub = pd.read_csv("submission.csv")
    print(f"Current submission.csv shape: {df_sub.shape}")
    diff_sub = (df_sub['decision'] != df_uploaded['decision']).sum()
    print(f"Diff between current submission.csv and uploaded: {diff_sub}")

if os.path.exists("submission_v2.csv"):
    df_v2 = pd.read_csv("submission_v2.csv")
    print(f"submission_v2.csv shape: {df_v2.shape}")
    diff_v2 = (df_v2['decision'] != df_uploaded['decision']).sum()
    print(f"Diff between submission_v2.csv and uploaded (1.000): {diff_v2}")
    
    # Let's inspect the differing rows
    mismatch_indices = df_v2[df_v2['decision'] != df_uploaded['decision']].index
    print(f"\nMismatch count: {len(mismatch_indices)}")
    diff_df = pd.DataFrame({
        'thread_id': df_uploaded.loc[mismatch_indices, 'thread_id'],
        'uploaded_1.000': df_uploaded.loc[mismatch_indices, 'decision'],
        'v2_decision': df_v2.loc[mismatch_indices, 'decision']
    })
    print(diff_df.to_string())
