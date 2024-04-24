import pandas as pd
import country_converter as coco
cc = coco.CountryConverter()

# parameters
file_path = "homework.csv"
full_list_of_columns = [
    "manufacturer_sku",
    "ean13",
    "weight",
    "length",
    "width",
    "height",
    "prop_65",
    "cost_price",
    "min_price",
    "made_to_order",
    "product__product_class__name",
    "product__brand__name",
    "product__title",
    "product__description",
    "product__bullets__0",
    "product__bullets__1",
    "product__bullets__2",
    "product__bullets__3",
    "product__bullets__4",
    "product__bullets__5",
    "product__bullets__6",
    "product__configuration__codes",
    "product__multipack_quantity",
    "product__country_of_origin__alpha_3",
    "product__parent_sku",
    "attrib__arm_height",
    "attrib__assembly_required",
    "attrib__back_material",
    "attrib__blade_finish",
    "attrib__bulb_included",
    "attrib__bulb_type",
    "attrib__color",
    "attrib__cord_length",
    "attrib__design_id",
    "attrib__designer",
    "attrib__distressed_finish",
    "attrib__fill",
    "attrib__finish",
    "attrib__frame_color",
    "attrib__hardwire",
    "attrib__kit",
    "attrib__leg_color",
    "attrib__leg_finish",
    "attrib__material",
    "attrib__number_bulbs",
    "attrib__orientation",
    "attrib__outdoor_safe",
    "attrib__pile_height",
    "attrib__seat_depth",
    "attrib__seat_height",
    "attrib__seat_width",
    "attrib__shade",
    "attrib__size",
    "attrib__switch_type",
    "attrib__ul_certified",
    "attrib__warranty_years",
    "attrib__wattage",
    "attrib__weave",
    "attrib__weight_capacity",
    "boxes__0__weight",
    "boxes__0__length",
    "boxes__0__height",
    "boxes__0__width",
    "boxes__1__weight",
    "boxes__1__length",
    "boxes__1__height",
    "boxes__1__width",
    "boxes__2__weight",
    "boxes__2__length",
    "boxes__2__height",
    "boxes__2__width",
    "boxes__3__weight",
    "boxes__3__length",
    "boxes__3__height",
    "boxes__3__width",
    "product__styles",
]

columns_renames = {
    "item number": "manufacturer_sku",
    "upc": "ean13",
    "item weight (pounds)": "weight",
    "item depth (inches)": "length",
    "item width (inches)": "width",
    "item height (inches)": "height",
    "url california label (jpg)": "prop_65", # will be converted to True or False
    "wholesale ($)": "cost_price",
    'min order qty': 'min_price',
    "item category": "product__product_class__name",
    "brand": "product__brand__name",
    "description": "product__title",
    "selling point 1": "product__bullets__1",
    "selling point 2": "product__bullets__2",
    "selling point 3": "product__bullets__3",
    "selling point 4": "product__bullets__4",
    "selling point 5": "product__bullets__5",
    "selling point 6": "product__bullets__6",
    "carton count": "product__multipack_quantity",
    # will be converted to alpha 3
    "country of origin": "product__country_of_origin__alpha_3",
    "furniture arm height (inches)": "attrib__arm_height",
    "bulb 1 included": "attrib__bulb_included",  # should be added the bulb 2 column
    "bulb 1 type": "attrib__bulb_type",
    "bulb 1 count": "attrib__number_bulbs",  # Will add bulb 2 count
    "item finish": "attrib__finish",
    "cord length (inches)": "attrib__cord_length",
    "conversion kit option": "attrib__kit",
    "item materials": "attrib__material",
    "outdoor": "attrib__outdoor_safe",
    "carton 1 weight (pounds)": "boxes__0__weight",
    "carton 1 length (inches)": "boxes__0__length",
    "carton 1 height (inches)": "boxes__0__height",
    "carton 1 width (inches)": "boxes__0__width",
    "carton 2 weight (pounds)": "boxes__1__weight",
    "carton 2 length (inches)": "boxes__1__length",
    "carton 2 height (inches)": "boxes__1__height",
    "carton 2 width (inches)": "boxes__1__width",
    "carton 3 weight (pounds)": "boxes__2__weight",
    "carton 3 length (inches)": "boxes__2__length",
    "carton 3 height (inches)": "boxes__2__height",
    "carton 3 width (inches)": "boxes__2__width",
    "item style": "product__styles",
    "furniture seat height (inches)": "attrib__seat_height",
    "furniture seat dimensions (inches)": "attrib__seat_width",
    "shade/glass description": "attrib__shade",
    "switch type": "attrib__switch_type",
    "safety rating": "attrib__ul_certified",  # will be converted based on value
    "bulb 1 wattage": "attrib__wattage",
    "furniture weight capacity (pounds)": "attrib__weight_capacity",
}

# load data
df = pd.read_csv(file_path)

# rename columns to make it easier to work
df = df.rename(columns=columns_renames)

# Handle Prop_65 info
# if it has a warning it will be set to true
for index, row in df.iterrows():
    # Check if the column you want to check has a non-null value
    if pd.notnull(row["prop_65"]):
        df.at[index, "prop_65"] = True
    else:
        df.at[index, "prop_65"] = False

# Calculate min_price
# based on the minimum order quantity
for index, row in df.iterrows():
    # Check if the column you want to check has a non-null value
    if row["min_price"] == 1:
        df.at[index, "min_price"] = pd.NA
    else:
        df.at[index, "min_price"] = row["min_price"] * row['cost_price']

# Convert to ALPHA3 country names
df['product__country_of_origin__alpha_3'] = cc.pandas_convert(series=df['product__country_of_origin__alpha_3'],to='ISO3')

# Add all bulbs
df['attrib__number_bulbs'] = df['attrib__number_bulbs'] + df['bulb 2 count']

# Handle attrib__ul_certified info
# if it has a "UL" it will be set to True
for index, row in df.iterrows():
    if row["attrib__ul_certified"] == "UL":
        df.at[index, "attrib__ul_certified"] = True
    else:
        df.at[index, "attrib__ul_certified"] = pd.NA

# Drop all columns that are not needed and create output dataframe
output_df = pd.DataFrame(columns=full_list_of_columns)
for column in full_list_of_columns:
    if column in df.columns:
        output_df[column] = df[column].copy()

# save data
output_df.to_csv("output.csv")
