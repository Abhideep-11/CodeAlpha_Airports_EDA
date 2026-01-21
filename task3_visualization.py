import pandas as pd
import matplotlib.pyplot as plt

# ========== 1. Load Dataset ==========
df = pd.read_csv("airports_cleaned.csv")
print("Dataset loaded successfully!")

# ========== 2. Ensure Country Column Exists ==========
if "country" not in df.columns:
    df["country"] = df["location"].apply(lambda x: x.split(",")[-1].strip())

# ========== 3. Visualization 1: Top 10 Countries ==========
top_countries = df["country"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_countries.plot(kind="bar")
plt.title("Top 10 Countries by Number of Airports")
plt.xlabel("Country")
plt.ylabel("Number of Airports")
plt.tight_layout()
plt.savefig("viz_top_countries.png")
plt.close()

print("Saved: viz_top_countries.png")

# ========== 4. Visualization 2: Top 10 Time Zones ==========
top_timezones = df["time"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_timezones.plot(kind="bar")
plt.title("Top 10 Time Zones by Number of Airports")
plt.xlabel("Time Zone")
plt.ylabel("Number of Airports")
plt.tight_layout()
plt.savefig("viz_top_timezones.png")
plt.close()

print("Saved: viz_top_timezones.png")

# ========== 5. Visualization 3: Airport Distribution by Continent (Approx) ==========
continent_map = {
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "India": "Asia",
    "China": "Asia",
    "Japan": "Asia",
    "United Kingdom": "Europe",
    "Germany": "Europe",
    "France": "Europe",
    "Australia": "Oceania",
    "Brazil": "South America"
}

df["continent"] = df["country"].map(continent_map).fillna("Other")
continent_counts = df["continent"].value_counts()

plt.figure(figsize=(8, 6))
continent_counts.plot(kind="pie", autopct="%1.1f%%")
plt.title("Airport Distribution by Continent (Approx)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("viz_continent_distribution.png")
plt.close()

print("Saved: viz_continent_distribution.png")

print("\nTask-3 visualizations generated successfully!")
