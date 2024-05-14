"""
Submodule containing the ItemConverter class. This class helps with:
    - Translating input data for a given item / row into the desired format.
"""

# Python Built-In Imports
from re import IGNORECASE, search
from typing import Dict

# Custom Imports
from config import DistanceMetric, WeightMetric, RegexStrings
from submodules.conversions import Converter
from submodules.upc import UPC_A

class ItemFormatter:
    "Formats a dictionary of input data from and item / row into the desired format."
    def __init__(self):
        self._given: Dict[str, str] = {} # Input
        self._formatted: Dict[str, str] = {} # Output

    def process(self, properties: Dict[str, str]):
        """
        Calling this method begins the conversion process.
        Starts by saving a version of the given properties with whitespace stripped from the values.

        For the mostpart conversions have to be manually defined / coded.
        Some improvements could involve using a mapping for attributes that are directly copied w/o any changes.
        """
        # Clean up all values received
        for key, value in properties.items():
            if key == 'description':
                if ",white" in value:
                    value = value.replace(",white", " In White")
                if "-Ebony" in value:
                    value = value.replace("-Ebony", "- Ebony")
                self._given[key] = Converter.set_word_to_num(value.strip()).title()
            else:
                self._given[key] = value.strip()

        # MANUFACTURER SKU and EAN13 code
        self._formatted['manufacturer_sku'] = self._given['item number']
        upc = UPC_A(self._given['upc'])
        self._formatted['ean13'] = upc.ean13

        # WEIGHT
        self._formatted['weight'] = Converter.to_pounds(self._given['item weight (pounds)'], WeightMetric.lb)
        
        # LENGTH, WIDTH, and HEIGHT - Force units to inches.
        for outProp, inProp in [('length', 'item depth (inches)'),
                                ('width', 'item width (inches)'),
                                ('height', 'item height (inches)')]:
            self._formatted[outProp] = Converter.to_inches(self._given[inProp], DistanceMetric.inch)

        # CALIFORNIA P65
        if 'P65' in self._given['url california label (jpg)'] \
            or 'P65' in self._given['url california label (pdf)']:
            self._formatted['prop_65'] = True
        else:
            self._formatted['prop_65'] = False

        # COST & MINIMUM PRICES - Force unit of accounting (two decimals).
        for outProp, inProp in [('cost_price', 'wholesale ($)'),
                                ('min_price', 'map ($)')]:
            self._formatted[outProp] = Converter.format_currency(self._given[inProp])

        # MADE TO ORDER (Pt. 1)
        # We set a default value here and we'll change it later
        # since Python 3.7 and on preserves insertion order.
        # This has to be handled when we're processing product bullets.
        self._formatted['made_to_order'] = ""

        # PRODUCT CLASS NAME, BRAND NAME, and PRODUCT TITLE
        # These are direct copies, we just force the text to be formatted as a title.
        for outProp, inProp in [('product__product_class__name', 'item category'),
                                ('product__brand__name', 'brand'),
                                ('product__title', 'description')]:
            self._formatted[outProp] = self._given[inProp].title()

        # PRODUCT DESCRIPTION
        self._formatted['product__description'] = self._given['long description']

        # PRODUCT BULLETS & MADE TO ORDER (Pt. 2)
        # We finish Made To Order here as we need to check
        # the bullet points for any mention of customization.
        custom = False
        for i in range(7):
            self._formatted[f'product__bullets__{i}'] = self._given[f'selling point {i+1}'].title()
            if "custom" in self._given[f'selling point {i+1}'].lower():
                custom = True
        self._formatted['made_to_order'] = custom

        # PRODUCT CONFIG CODES
        self._formatted['product__configuration__codes'] = ""

        # MULTIPACK QUANTITY - Need to check different attributes for certain strings.
        self._formatted['product__multipack_quantity'] = "1"
        # Check if the item number denotes a multipack.
        itemNum = self._given['item number']
        itemNumRes = search(RegexStrings.SHORT_SET, itemNum)
        if not (itemNumRes is None):
            self._formatted['product__multipack_quantity'] = itemNumRes.group(1)
        else: # Check both descriptions for any string denoting a multipack.
            desc = self._given['description']
            longDesc = self._given['long description']
            for reStr in RegexStrings.SET_NUMS:
                descRes = search(reStr, desc, IGNORECASE)
                if not (descRes is None):
                    self._formatted['product__multipack_quantity'] = descRes.group(1)
                    break
                else:
                    longDescRes = search(reStr, longDesc, IGNORECASE)
                    if not (longDescRes is None):
                        self._formatted['product__multipack_quantity'] = longDescRes.group(1)
                        break

        # COUNTRY ALPHA 3
        self._formatted['product__country_of_origin__alpha_3'] = Converter.get_alpha_3(self._given['country of origin'])

        # PARENT SKU - This will be calculated later by ParentProcessor class.
        self._formatted['product__parent_sku'] = ""

        # ARM HEIGHT
        self._formatted['product__arm_height'] = Converter.to_inches(self._given['furniture arm height (inches)'], DistanceMetric.inch)

        # ASSEMBLY REQUIRED
        # This property was a bit weird. At first I thought any 'carton count'
        # greater than one would indicate multiple pieces and therefore assembly
        # required. However, it could be the case multiple complete / assembled
        # pieces are just shipped in multiple cartons. This same principle applies
        # if I were to try checking for one or more 'multi-piece dimension' properties,
        # as these could still be assembled pieces of furniture that are part of a set.
        # Therefore, without a clear property indicating assembly, I decided it would
        # be beast to leave this blanks.
        self._formatted['product__assembly_required'] = ""

        # BACK MATERIAL
        self._formatted['attrib__back_material'] = ""

        # BLADE FINISH
        self._formatted['attrib__blade_finish'] = ""

        # BULB INCLUDED
        # Two possible sets of columns for bulbs, so we'll check both.
        bulb1 = self._given['bulb 1 included']
        bulb2 = self._given['bulb 2 included']
        self._formatted['attrib__bulb_included'] = ", ".join([inc for inc in [bulb1, bulb2] if inc != ""])

        # BULB TYPE
        # Same principle as 'Bulb Included' applies here.
        bulb1 = self._given['bulb 1 type']
        bulb2 = self._given['bulb 2 type']
        self._formatted['attrib__bulb_type'] = ", ".join([inc for inc in [bulb1, bulb2] if inc != ""])

        # COLOR
        self._formatted['attrib__color'] = self._given['primary color family']

        # CORD LENGTH
        self._formatted['attrib__cord_length'] = Converter.to_inches(self._given['cord length (inches)'], DistanceMetric.inch)

        # DESIGN ID
        self._formatted['attrib__designer_id'] = ""

        # DESIGNER
        self._formatted['attrib__designer'] = self._given['licensed by']

        # DISTRESSED FINISH
        self._formatted['attrib__distressed_finish'] = ("distressed" in self._given['item finish'])
        
        # FILL
        self._formatted['attrib__fill'] = ""

        # FINISH
        self._formatted['attrib__finish'] = self._given['item finish']

        # FRAME COLOR
        self._formatted['attrib__frame_color'] = ""

        # HARDWIRE
        text = self._given['switch type']
        if text == "":
            self._formatted['attrib__hardwire'] = ""
        else:
            self._formatted['attrib__hardwire'] = ('hardwired' in text.lower())

        # KIT
        self._formatted['attrib__kit'] = Converter.YN_to_bool(self._given['conversion kit option'])

        # LEG COLOR
        self._formatted['attrib__leg_color'] = ""

        # LEG FINISH
        self._formatted['attrib__leg_finish'] = ""

        # MATERIAL
        self._formatted['attrib__material'] = self._given['item materials']

        # NUMBER BULBS
        count1 = self._given['bulb 1 count']
        count2 = self._given['bulb 2 count']
        if count1 == "" and count2 == "":
            self._formatted['attrib__number_bulbs'] = ""
        else:
            total = 0
            for count in [count1, count2]:
                if count.isdigit():
                    total += int(count)
            self._formatted['attrib__number_bulbs'] = str(total)

        # ORIENTATION
        self._formatted['attrib__orientation'] = ""

        # OUTDOOR SAFE
        self._formatted['attrib__outdoor_safe'] = Converter.YN_to_bool(self._given['outdoor'])

        # PILE HEIGHT
        # For the sake of time and prioritization I'm skipping this property. Normally,
        # I would just search the item type or description for keywords like 'carpet'
        # or 'rug,' however, there are some edge case products like rug displays
        # that would lead to "false positive" entries as rugs. If there were none of
        # these edge case products, then pile height would just be the rug's height.
        self._formatted['pile_height'] = ""

        # SEAT DEPTH, WIDTH, HEIGHT
        # Depth and width are a single string separated by 'x', so we separate
        # any non-empty string and set the width to be the smaller value.
        seatDimensions = self._given['furniture seat dimensions (inches)'].lower()
        seatDimensions = seatDimensions.split('x')

        if len(seatDimensions) > 1: # Multiple values, assume each is a different value.
            seatD = Converter.to_inches(max(seatDimensions), DistanceMetric.inch)
            seatW = Converter.to_inches(min(seatDimensions), DistanceMetric.inch)
        else: # Only one value, assume this means both are equal.
            dist = Converter.to_inches(seatDimensions[0], DistanceMetric.inch)
            seatD = dist
            seatW = dist
        
        self._formatted['attrib__seat_depth'] = seatD
        self._formatted['attrib__seat_height'] = Converter.to_inches(self._given['furniture seat height (inches)'], DistanceMetric.inch)
        self._formatted['attrib__seat_width'] = seatW

        # SHADE
        self._formatted['attrib__shade'] = self._given['shade/glass description'].title()

        # SIZE
        text = self._given['description'].lower()
        if self._given['description'] == "":
            self._formatted['attrib__size'] = ""
        elif "small" in text:
            self._formatted['attrib__size'] = "Small"
        elif "medium" in text:
            self._formatted['attrib__size'] = "Medium"
        elif "large" in text:
            self._formatted['attrib__size'] = "Large"
        elif "short" in text:
            self._formatted['attrib__size'] = "Short"
        elif "tall" in text:
            self._formatted['attrib__size'] = "Tall"
        else:
            self._formatted['attrib__size'] = ""

        # SWITCH TYPE
        self._formatted['attrib__switch_type'] = self._given['switch type']

        # UL CERTIFIED
        self._formatted['attrib__ul_certified'] = ('UL' in self._given['safety rating'])

        # WARRANTY YEARS
        # There isn't really any data on warranties in the CSV so we'll leave it blank for now.
        self._formatted['attrib__warranty_years'] = ""

        # WATTAGE
        bulb1 = self._given['bulb 1 wattage']
        bulb2 = self._given['bulb 2 wattage']
        self._formatted['attrib__wattage'] = ", ".join([inc for inc in [bulb1, bulb2] if inc != ""])

        # WEAVE
        # There's a lot of properties that weave could be, such as rugs vs. lamp shades.
        # Example also doesn't clarify so what we want to track, such as whether theres IS
        # a weave vs. the style / color / pattern / etc. of the weave, so we'll leave it blank.
        self._formatted['attrib__weave'] = ""

        # WEIGHT CAPACITY
        self._formatted['attrib__weight_capacity'] = Converter.to_pounds(self._given['furniture weight capacity (pounds)'], WeightMetric.lb)

        # INDIVIDUAL BOXES
        i = 1
        while f'carton {i} weight (pounds)' in self._given.keys():
            self._formatted[f'boxes__{i-1}__weight'] = Converter.to_pounds(self._given[f'carton {i} weight (pounds)'], WeightMetric.lb)

            for outProp, inProp in [(f'boxes__{i-1}__length', f'carton {i} length (inches)'),
                                    (f'boxes__{i-1}__height', f'carton {i} height (inches)'),
                                    (f'boxes__{i-1}__width', f'carton {i} width (inches)')]:
                text = self._given[inProp]
                self._formatted[outProp] = Converter.to_inches(self._given[inProp], DistanceMetric.inch)
            i += 1

        # PRODUCT STYLES
        self._formatted['product_styles'] = self._given['item style']

    def formatted_headers(self):
        return self._formatted.keys()
    
    def export(self):
        return self._formatted