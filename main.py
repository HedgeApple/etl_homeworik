# Python Built-In Imports
from csv import DictReader, DictWriter
import sys
from typing import List

# Custom Imports
from config import DEF_INPUT_FILENAME, DEF_INPUT_PATH, DEF_OUTPUT_FILENAME, DEF_OUTPUT_PATH
from submodules import ItemFormatter

def progress_bar(current, total, bar_length=20):
    """
    Handles outputting a progress bar.
    
    Args:
        - current: The number of finished rows.
        - total: The total number of rows to process.
        - bar_length: Length of the progress bar.
    """
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    sys.stdout.write(f"\r\tProgress: [{arrow}{padding}] {int(fraction*100)}% "\
                        f"({current}/{total})")
    sys.stdout.flush()

def process_parents(inventory: List[ItemFormatter]):
    """
    Assigns parent SKU to each item after removing
    keywords used for variants from descriptions.

    Args:
        - inventory: The list of ItemFormatter objects to process.
    
    Returns:
        - A processed list of ItemFormatter objects with parent SKUs assigned.
    """
    curSKU = 0
    baseSKU = 100000
    total = len(inventory)

    print("Cleaning formatted descriptions...")
    complete = 0
    processed = []
    # Preprocess descriptions to clean and remove as many keywords used by variants as possible.
    for item in inventory:
        desc = item._given['description']
        for targStr in [" - ", " In "]:
            if targStr in desc:
                index = desc.find(targStr)
                desc = desc[:index]

        for targStr in [" Led"]:
            desc = desc.replace(targStr, '')
        item._given['description'] = desc
        complete += 1
        progress_bar(complete, total)
    print(", Done.")
    # Sorting by description places similar descriptions together in order.
    processed = sorted(inventory, key=(lambda d: d._given['description']))

    print("Assigning parent SKUs...")
    complete = 1
    prevDesc = processed[0]._given['description']
    processed[0]._formatted['product__parent_sku'] = f"O-{baseSKU + curSKU}"
    for i in range(1, len(processed)):
        if processed[i]._given['description'] != prevDesc: # Different Description, may need to increment curSKU
            prevSep = prevDesc.split()
            curSep = processed[i]._given['description'].split()
            if len(prevSep) == len(curSep): # Same number of words in description
                # Count the number of mistmatched words
                mismatches = 0
                for j in range(len(prevSep)):
                    if prevSep[j] != curSep[j]:
                        mismatches += 1

                if mismatches > 1: # Multiple words vary, likely not variants
                    curSKU += 1
            else: # Different number of words in description, likely not variants
                curSKU += 1
        
        prevDesc = processed[i]._given['description']
        processed[i]._formatted['product__parent_sku'] = f"O-{baseSKU + curSKU}"
        complete += 1
        progress_bar(complete, total)
    print(", Done.")
    
    return processed

def main():
    allItems: List[ItemFormatter] = []

    total = 0
    try:
        # Count the number of items in the default input file.
        with open(DEF_INPUT_PATH, 'r', encoding='utf8') as inFile:
            reader = DictReader(inFile)
            total = sum(1 for row in reader)

        # Process each item from the default input file.
        with open(DEF_INPUT_PATH, 'r', encoding='utf8') as inFile:
            reader = DictReader(inFile)
            try:
                complete = 0
                print(f"Processing {DEF_INPUT_FILENAME}... ({total} Rows)")
                for row in reader:
                    newItem = ItemFormatter()
                    newItem.process(row)
                    allItems.append(newItem)
                    complete += 1
                    progress_bar(complete, total)
                print(", Done.")
            except Exception as e:
                sys.exit(f"\nError in file '{DEF_INPUT_FILENAME}', line {reader.line_num}: {e}\nExiting...")
    except Exception as e:
        sys.exit(f"Error occurred while accessing '{DEF_INPUT_FILENAME}': {e}\nExiting...")

    finished = process_parents(allItems)

    headers = allItems[0].formatted_headers()

    # Output to default output file.
    print(f"Outputting data to {DEF_OUTPUT_FILENAME}...", end="")
    try:
        with open(DEF_OUTPUT_PATH, 'w', encoding='utf8', newline='') as outFile:
            writer = DictWriter(outFile, fieldnames=headers)
            try:
                writer.writeheader()
                for item in finished:
                    writer.writerow(item.export())
            except Exception as e:
                sys.exit(f"\nError writing to file {DEF_OUTPUT_FILENAME}, item {item}: {e}")
    except Exception as e:
        sys.exit(f"\nError occurred while accessing '{DEF_OUTPUT_FILENAME}': {e}")
    print(" Finished.")

if __name__ == "__main__":
    main()