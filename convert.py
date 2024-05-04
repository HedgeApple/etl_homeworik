import csv, sys

# Development process:
# 1. Open up the file:
#       - Default encoding will lead to an error, utf8 seems to work fine.
# 2. Output the first item row to a more 'reader-friendly' formatted file.
#       - DictReader helps with this a it automatically grabs the headers as the first row of the file.

class Converter:
    def __init__(self, targetFile: str):
        # with open('formatted.csv', 'w', encoding='utf-8'):
        #     self._writer = csv.DictWriter()
        self._targetFile = targetFile

        with open("exampleFirstRow.txt", 'w', encoding='utf8') as outFile:
            with open("example.csv", newline='', encoding='utf8') as infile:
                self._reader = csv.DictReader(infile)
                try:
                    for row in self._reader:
                        for key, val in row.items():
                            outFile.write(f"{key}: {val}\n")
                        break
                except csv.Error as e:
                    sys.exit('file {}, line {}: {}'.format(self._targetFile, self._reader.line_num, e))

        with open("homeworkFirstRow.txt", 'w', encoding='utf8') as outFile:
            with open(self._targetFile, newline='', encoding='utf8') as infile:
                self._reader = csv.DictReader(infile)
                try:
                    for row in self._reader:
                        for key, val in row.items():
                            outFile.write(f"{key}: {val}\n")
                        break
                except csv.Error as e:
                    sys.exit('file {}, line {}: {}'.format(self._targetFile, self._reader.line_num, e))
    def convert_upc(self, row):
        """
        Description:
            Converts the UPC to desired formats.
            All the UPCs are 12 digits so we assume UPC-A

            Conversions:
                - EAN13: Appends 0. First three digits are the GS1 prefix,
                         next section is the manufacturer code,
                         final section is the product code.
                - Gtin:
        """
        "Convert the UPC to desired formats."
        # UPC is 12 digits.
        # EAN13 adds a 0 to the front and add a dash between:
        # 2 and 3rd digits, 11th and 12th digits. Account for python's 0-based indexing and ignoring last index
        # Example didn't have anything for Gtin so we'll ignore it.
        ean13 = f'0{row['upc'][0:2]}-{row['upc'][2-11]}-{row['upc'][11]}'


    def convert_boxes(self, row):
        for i in range(4):  # Iterates through [0 - 3]
            print()

    def convert_row(self, row):
        self._writer.writerow({
            "manufacturer_sku", "ean13", "weight", "length", "width", "height",
            "prop_65", "cost_price", "min_price", "made_to_order",
            "product__product_class__name", "product__brand__name", "product__title", "product__description",
            "product__bullets__0", "product__bullets__1", "product__bullets__2", "product__bullets__3", "product__bullets__4", "product__bullets__5", "product__bullets__6",
            "product__configuration__codes", "product__multipack_quantity", "product__country_of_origin__alpha_3", "product__parent_sku",
            "attrib__arm_height", "attrib__assembly_required", "attrib__back_material", "attrib__blade_finish", "attrib__bulb_included", "attrib__bulb_type", "attrib__color",
            "attrib__cord_length", "attrib__design_id", "attrib__designer", "attrib__distressed_finish", "attrib__fill", "attrib__finish", "attrib__frame_color", "attrib__hardwire",
            "attrib__kit", "attrib__leg_color", "attrib__leg_finish", "attrib__material", "attrib__number_bulbs", "attrib__orientation", "attrib__outdoor_safe", "attrib__pile_height",
            "attrib__seat_depth", "attrib__seat_height", "attrib__seat_width", "attrib__shade", "attrib__size", "attrib__switch_type", "attrib__ul_certified", "attrib__warranty_years",
            "attrib__wattage", "attrib__weave", "attrib__weight_capacity",
            "boxes__0__weight", "boxes__0__length", "boxes__0__height", "boxes__0__width",
            "boxes__1__weight", "boxes__1__length", "boxes__1__height", "boxes__1__width",
            "boxes__2__weight", "boxes__2__length", "boxes__2__height", "boxes__2__width",
            "boxes__3__weight", "boxes__3__length", "boxes__3__height", "boxes__3__width",
            "product__styles"
        })
        print()

headers = ["manufacturer_sku", "ean13", "weight", "length", "width", "height",
           "prop_65", "cost_price", "min_price", "made_to_order",
           "product__product_class__name", "product__brand__name", "product__title", "product__description",
           "product__bullets__0", "product__bullets__1", "product__bullets__2", "product__bullets__3", "product__bullets__4", "product__bullets__5", "product__bullets__6",
           "product__configuration__codes", "product__multipack_quantity", "product__country_of_origin__alpha_3", "product__parent_sku",
           "attrib__arm_height", "attrib__assembly_required", "attrib__back_material", "attrib__blade_finish", "attrib__bulb_included", "attrib__bulb_type", "attrib__color",
           "attrib__cord_length", "attrib__design_id", "attrib__designer", "attrib__distressed_finish", "attrib__fill", "attrib__finish", "attrib__frame_color", "attrib__hardwire",
           "attrib__kit", "attrib__leg_color", "attrib__leg_finish", "attrib__material", "attrib__number_bulbs", "attrib__orientation", "attrib__outdoor_safe", "attrib__pile_height",
           "attrib__seat_depth", "attrib__seat_height", "attrib__seat_width", "attrib__shade", "attrib__size", "attrib__switch_type", "attrib__ul_certified", "attrib__warranty_years",
           "attrib__wattage", "attrib__weave", "attrib__weight_capacity",
           "boxes__0__weight", "boxes__0__length", "boxes__0__height", "boxes__0__width",
           "boxes__1__weight", "boxes__1__length", "boxes__1__height", "boxes__1__width",
           "boxes__2__weight", "boxes__2__length", "boxes__2__height", "boxes__2__width",
           "boxes__3__weight", "boxes__3__length", "boxes__3__height", "boxes__3__width",
           "product__styles"]


def main():
    conv = Converter("homework.csv")

main()