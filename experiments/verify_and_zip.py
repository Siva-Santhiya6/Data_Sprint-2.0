import pandas as pd
import zipfile

up = pd.read_csv(r"C:/Users/Siva Santhiya/.gemini/antigravity/brain/80f9dc9b-c986-4148-a6f3-88cd1e9b26a2/.user_uploaded/media_1795579702667_a1ff2b0c.csv")
col_up = 'label' if 'label' in up.columns else 'decision'

sub = pd.read_csv("submission.csv")
col_sub = 'label' if 'label' in sub.columns else 'decision'
diff_sub = (sub[col_sub] != up[col_up]).sum()
print(f"Diff submission.csv vs 1.000: {diff_sub} / 2000")

sub_v2 = pd.read_csv("submission_v2.csv")
col_v2 = 'label' if 'label' in sub_v2.columns else 'decision'
diff_v2 = (sub_v2[col_v2] != up[col_up]).sum()
print(f"Diff submission_v2.csv vs 1.000: {diff_v2} / 2000")

# Regenerate zip archives
with zipfile.ZipFile("submission.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write("submission.csv", arcname="submission.csv")
print("Wrote submission.zip")

with zipfile.ZipFile("submission_v2.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write("submission_v2.csv", arcname="submission_v2.csv")
print("Wrote submission_v2.zip")
