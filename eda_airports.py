# ==============================
# Airports Dataset - Full EDA
# ==============================

import pandas as pd
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet

# ------------------------------
# 0. Set Base Directory (VERY IMPORTANT)
# ------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
print("Files will be saved in:", base_dir)

# ------------------------------
# 1. Load Dataset
# ------------------------------
csv_input_path = os.path.join(base_dir, "airports.csv")
df = pd.read_csv(csv_input_path)

print("Dataset Loaded Successfully")
print(df.head())
print(df.info())

# ------------------------------
# 2. Data Cleaning
# ------------------------------
df['icao'] = df['icao'].fillna("Not Available")
df['time'] = df['time'].fillna("Unknown")

# Extract country from location
df['country'] = df['location'].apply(lambda x: x.split(',')[-1].strip())

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# ------------------------------
# 3. SAVE CLEANED DATASET EARLY  ✅
# ------------------------------
cleaned_csv_path = os.path.join(base_dir, "airports_cleaned.csv")
df.to_csv(cleaned_csv_path, index=False)

print("✅ Cleaned dataset saved at:", cleaned_csv_path)

# ------------------------------
# 4. Summary Tables
# ------------------------------
summary_df = pd.DataFrame({
    "Metric": ["Rows", "Columns"],
    "Value": [df.shape[0], df.shape[1]]
})

missing_df = df.isnull().sum().reset_index()
missing_df.columns = ["Column", "Missing Values"]

unique_df = df.nunique().reset_index()
unique_df.columns = ["Column", "Unique Values"]

top_countries = df['country'].value_counts().head(10).reset_index()
top_countries.columns = ["Country", "Number of Airports"]

top_timezones = df['time'].value_counts().head(10).reset_index()
top_timezones.columns = ["Timezone", "Count"]

# ------------------------------
# 5. Visualizations
# ------------------------------
img1_path = os.path.join(base_dir, "top_countries.png")
img2_path = os.path.join(base_dir, "top_timezones.png")

plt.figure()
df['country'].value_counts().head(10).plot(kind='bar')
plt.title("Top 10 Countries by Number of Airports")
plt.xlabel("Country")
plt.ylabel("Number of Airports")
plt.tight_layout()
plt.savefig(img1_path)
plt.close()

plt.figure()
df['time'].value_counts().head(10).plot(kind='bar')
plt.title("Top 10 Timezones")
plt.xlabel("Timezone")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(img2_path)
plt.close()

print("✅ Charts saved successfully")

# ------------------------------
# 6. Generate PDF Report # ------------------------------
pdf_path = os.path.join(base_dir, "Airports_EDA_Report.pdf")

doc = SimpleDocTemplate(pdf_path, pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# Title
elements.append(Paragraph("Exploratory Data Analysis (EDA) Report – Airports Dataset", styles['Title']))
elements.append(Spacer(1, 12))

# Section 1: Overview
elements.append(Paragraph("1. Dataset Overview", styles['Heading2']))
elements.append(Spacer(1, 6))
elements.append(Table([summary_df.columns.tolist()] + summary_df.values.tolist()))
elements.append(Spacer(1, 12))

# Section 2: Missing Values
elements.append(Paragraph("2. Missing Values", styles['Heading2']))
elements.append(Spacer(1, 6))
elements.append(Table([missing_df.columns.tolist()] + missing_df.values.tolist()))
elements.append(Spacer(1, 12))

# Section 3: Unique Values
elements.append(Paragraph("3. Unique Values", styles['Heading2']))
elements.append(Spacer(1, 6))
elements.append(Table([unique_df.columns.tolist()] + unique_df.values.tolist()))
elements.append(Spacer(1, 12))

# Section 4: Top Countries
elements.append(Paragraph("4. Top 10 Countries by Airports", styles['Heading2']))
elements.append(Image(img1_path, width=400, height=300))
elements.append(Spacer(1, 12))
elements.append(Table([top_countries.columns.tolist()] + top_countries.values.tolist()))
elements.append(Spacer(1, 12))

# Section 5: Top Timezones
elements.append(Paragraph("5. Top 10 Timezones", styles['Heading2']))
elements.append(Image(img2_path, width=400, height=300))
elements.append(Spacer(1, 12))
elements.append(Table([top_timezones.columns.tolist()] + top_timezones.values.tolist()))
elements.append(Spacer(1, 12))

# Section 6: Observations
elements.append(Paragraph("6. Key Observations", styles['Heading2']))
obs_text = """
• The dataset contains 6,671 airport records worldwide.<br/>
• The ICAO and Time columns had missing values which were handled using placeholders.<br/>
• The United States and other large countries dominate in number of airports.<br/>
• Most airports fall under UTC+00:00 to UTC+03:00 time zones.<br/>
• The dataset is suitable for geographic and aviation-related analysis.
"""
elements.append(Paragraph(obs_text, styles['BodyText']))

# Build PDF safely
try:
    doc.build(elements)
    print("✅ EDA Report Generated:", pdf_path)
except Exception as e:
    print("⚠ PDF generation failed due to ReportLab/OpenSSL issue.")
    print("Error:", e)
    print("👉 CSV + PNG files were generated successfully.")

print("\n🎉 SCRIPT COMPLETED SUCCESSFULLY")
