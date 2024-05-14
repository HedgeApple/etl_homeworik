"Submodule that contains the UPC_A class for handling UPC-A codes."

class UPC_A:
    """
    Validates UPC-A code and maps members to UPC-A components and conversions. Handles:
        - Validating the given code is in a valid format for UPC-A.
        - Correcting invalid codes when possible and allowed.
        - Converting UPC-A to EAN13.
        - Managing the manufacturer code, product code, and check digit for an item.
    """
    def __init__(self, code: str, autoCorrect: bool = False):
        """
        Takes in a UPC-A code and organizes into segments if properly formatted / valid.
            - 12 Digit Format: Number system digit, 5 digits for manufacturer code, 5 digits for product code, and check digit.

        Args:
            - code: The string of digits to validate.
            - autoCorrect: Flag on whether the class should correct UPC-A format errors.
        
        Returns:
            - This UPC_A object.
        """
        self.upc = code
        self.autoCorrect = autoCorrect

        self._validate_upc()

        if len(self.upc) == 12:
            self.systemDigit = self.upc[0]      # First digit is number system digit.
            self.manufCode = self.upc[1:6]      # Manufacturer code is digits 2-6 (0-based: 1-5).
            self.productCode = self.upc[6:11]   # Product code is digits 7-11 (0-based: 6-10).

            # EAN13 Conversion:
            #   Append 0 to the front of the UPC-A code.
            #   Insert dash between 3rd and 4th digit, and before the check digit.
            self.ean13 = f"0{self.systemDigit}{self.manufCode[0]}-{self.manufCode[1:]}{self.productCode}-{self.checkDigit}"
        else:
            self.systemDigit = self.manufCode = self.productCode = self.ean13 = "N/A"

    def __str__(self):
        return self.upc
    
    def __repr__(self):
        return f"UPC_A({self.upc})"
        
    def _calculate_check_digit(self) -> int:
        """
        Calculates and returns the expected check digit for the stored UPC-A code.

        Check Digit Formula:
            - Calculate (3 * Sum of odd-indexed digits + sum of even-indexed digits) mod 10.
            - Excludes 12th digit (check digit).
            - If the result is 0, check digit is 0, otherwise check digit is 10 - result.
        """
        if len(self.upc) < 11:
            return -1 # Guarantess _check_digit_is_valid() always returns false.
        
        oddSum = sum([int(self.upc[i]) for i in range(0, 12, 2)])
        evenSum = sum([int(self.upc[i]) for i in range(1, 11, 2)])
        res = (oddSum * 3 + evenSum) % 10
        if res == 0:
            return 0
        else:
            return 10 - res
        
    def _check_digit_is_valid(self) -> bool:
        "Returns whether the stored UPC-A code's check digit is valid."
        return int(self.checkDigit) == self._calculate_check_digit()

    def _validate_upc(self):
        """
        Validate the given UPC-A code matches proper format.
            - Auto-correct if allowed and possible (can only correct 11-digit codes).
            - Sets the _valid private member variable and checkDigit member variable.
        """
        if self.upc == "":
            self._valid = False
            self.checkDigit = "N/A"
            return
        
        self.checkDigit = self.upc[-1] # Check digit is always the last digit.

        if self._check_digit_is_valid() == True:
            self._valid = True
        elif len(self.upc) == 12:
            self._valid = False
        elif self.autoCorrect == True: # We only autoCorrect UPC-A codes that are not 12 digits.
            if len(self.upc) == 11:
                # Correction Case: Missing digit is likely check digit.
                #   Since the rest of the code is assigned by a global authority,
                #   it's reasonable to assume the check digit would be what's missing.
                self.checkDigit = self._calculate_check_digit()
                self.upc = f"{self.upc}{self.checkDigit}"
                self._valid = True
            else: # If we can't correct the issue, the code is invalid.
                self._valid = False
        else:
            self._valid = False

    def is_valid(self) -> bool:
        "Returns whether the stored UPC-A code is valid."
        return self._valid