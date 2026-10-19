"""Clean the RS_198 (2021) load and run the data-quality checks.

Reads the raw declared table who_rs198_2021 from data.db (never overwritten),
writes two derived tables: who_rs198_2021_clean (analysis sample, one row per
country) and who_region_lookup (six WHO regions, from the REGION rows).
Prints the sample flow and the quality counts used in data_summary.md.
"""
import os
import sqlite3

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "data.db")

# WHO region names as written in parent_location, mapped to the GHO region codes
REGION_NAME_TO_CODE = {
    "Africa": "AFR",
    "Americas": "AMR",
    "South-East Asia": "SEAR",
    "Europe": "EUR",
    "Eastern Mediterranean": "EMR",
    "Western Pacific": "WPR",
}

con = sqlite3.connect(DB)
raw = pd.read_sql("SELECT * FROM who_rs198_2021", con)
names = pd.read_sql("SELECT adm0_a3, iso_a3_eh, name FROM country_names", con)

print("== Sample flow ==")
print(f"raw rows: {len(raw)}")
countries = raw[raw["spatial_type"] == "COUNTRY"].copy()
print(f"after spatial_type = COUNTRY: {len(countries)} (dropped {len(raw) - len(countries)} REGION/GLOBAL rows)")

# Units: values must be deaths per 100,000, plausibly 0-50
bad_units = countries[(countries["value"] < 0) | (countries["value"] > 50)]
print(f"values outside 0-50 per 100,000: {len(bad_units)}")
assert len(bad_units) == 0, "unit check failed"

# Duplicates on the declared key (location, year)
dups = countries.duplicated(subset=["location", "year"], keep=False)
print(f"duplicate (location, year) rows: {int(dups.sum())}")
assert not dups.any(), "duplicate country-year rows remain"

# Missingness by column and by region, on COUNTRY rows
print("\n== Missing values by column (COUNTRY rows) ==")
for col in ["value", "low", "high", "parent_location"]:
    print(f"{col}: {int(countries[col].isna().sum())} missing of {len(countries)}")

countries["region_name_raw"] = countries["parent_location"].fillna("(no region)")
print("\n== Missing value by WHO region (COUNTRY rows) ==")
by_region = countries.groupby("region_name_raw").agg(
    n=("location", "size"), n_missing_value=("value", lambda s: int(s.isna().sum()))
)
print(by_region.to_string())

missing_value = countries[countries["value"].isna()][["location", "parent_location"]]
print("\nCountries without a value (excluded, not imputed):")
print(missing_value.to_string(index=False))

# Country-to-region mapping: every country with a value must map to one region code
analysis = countries[countries["value"].notna()].copy()
unknown_region = analysis[~analysis["parent_location"].isin(REGION_NAME_TO_CODE)]
assert len(unknown_region) == 0, f"unmapped regions: {unknown_region['parent_location'].unique()}"
analysis["who_region"] = analysis["parent_location"].map(REGION_NAME_TO_CODE)

# Region lookup from the REGION rows of the same load; cross-check against country rows
region_rows = raw[raw["spatial_type"] == "REGION"][["location", "value"]].copy()
region_rows.columns = ["region_code", "value"]
region_rows["region_name"] = region_rows["region_code"].map(
    {code: name for name, code in REGION_NAME_TO_CODE.items()}
)
assert region_rows["region_name"].notna().all(), "region code not in the six-region list"
region_codes_from_countries = set(analysis["who_region"])
print(f"\nregion codes in REGION rows: {sorted(region_rows['region_code'])}")
print(f"region codes mapped from countries: {sorted(region_codes_from_countries)}")
assert region_codes_from_countries == set(region_rows["region_code"]), "region codes disagree"

# Join country names on ISO3 (either key), each code must match exactly once
name_map = {}
for _, row in names.iterrows():
    for key in [row["iso_a3_eh"], row["adm0_a3"]]:
        if isinstance(key, str):
            name_map.setdefault(key, row["name"])
analysis["country_name"] = analysis["location"].map(name_map)
unmatched = analysis[analysis["country_name"].isna()]["location"].tolist()
print(f"\nanalysis countries not matched to a name: {unmatched}")

clean = analysis[["location", "country_name", "parent_location", "who_region", "year", "value", "low", "high"]].rename(
    columns={"location": "iso3", "parent_location": "who_region_name"}
)
clean = clean.sort_values("iso3").reset_index(drop=True)
zero_values = clean[clean["value"] == 0][["iso3", "country_name"]]
print(f"zero values kept and flagged: {zero_values.values.tolist()}")

print("\n== Sample flow (final) ==")
print(f"COUNTRY rows: {len(countries)}; with a value (analysis sample): {len(clean)}; excluded: {len(countries) - len(clean)}")
print(f"countries per region (analysis sample):\n{clean['who_region'].value_counts().sort_index().to_string()}")
print(f"low non-null: {int(clean['low'].notna().sum())}; high non-null: {int(clean['high'].notna().sum())}")

print("\n== Analysis-sample value range ==")
print(clean["value"].describe().to_string())

clean_out = clean.copy()
region_out = region_rows[["region_code", "region_name", "value"]].sort_values("region_code").reset_index(drop=True)
clean_out.to_sql("who_rs198_2021_clean", con, if_exists="replace", index=False)
region_out.to_sql("who_region_lookup", con, if_exists="replace", index=False)
con.commit()

check = pd.read_sql("SELECT COUNT(*) AS n, COUNT(value) AS nv FROM who_rs198_2021_clean", con)
print(f"\nwritten who_rs198_2021_clean: {check.to_dict('records')}")
check2 = pd.read_sql("SELECT COUNT(*) AS n, COUNT(value) AS nv FROM who_region_lookup", con)
print(f"written who_region_lookup: {check2.to_dict('records')}")
con.close()
