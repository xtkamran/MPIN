# class MPINAnalyzer:
#     COMMON_4DIGIT_PINS = [
#         '1234', '1111', '0000', '1212', '7777', '1004', '2000', '4444', '2222',
#         '6969', '9999', '3333', '5555', '6666', '1122', '1313', '8888', '4321',
#         '2001', '1010', '2580', '0007', '1818', '1230', '1110', '1210', '1000'
#     ]
    
#     COMMON_6DIGIT_PINS = [
#         '123456', '111111', '000000', '121212', '112233', '123123', '123321',
#         '654321', '111222', '121314', '100100', '200200', '102030', '110110',
#         '101010', '112211', '200000', '123654', '111000', '147258', '258369'
#     ]

#     def __init__(self, pin_length=4):
#         self.pin_length = pin_length
#         self.common_pins = self.COMMON_6DIGIT_PINS if pin_length == 6 else self.COMMON_4DIGIT_PINS
        
#     def analyze(self, mpin, demographics=None):
#         reasons = []
        
#         # Validate input length
#         if len(mpin) != self.pin_length or not mpin.isdigit():
#             return {
#                 'valid': False,
#                 'strength': 'INVALID',
#                 'reasons': ['INVALID_LENGTH' if len(mpin) != self.pin_length else 'NON_DIGIT']
#             }
        
#         # Check for common PINs
#         if mpin in self.common_pins:
#             reasons.append('COMMONLY_USED')
        
#         # Check demographic patterns if provided
#         if demographics:
#             reasons += self._check_demographic_patterns(mpin, demographics)
        
#         strength = 'STRONG' if not reasons else 'WEAK'
        
#         return {
#             'valid': True,
#             'strength': strength,
#             'reasons': reasons
#         }
    
#     def _check_demographic_patterns(self, mpin, demographics):
#         reasons = []
#         patterns = []
        
#         # For 4-digit MPINs
#         if self.pin_length == 4:
#             # Check DDMM patterns
#             if 'user_dob' in demographics:
#                 dd_mm = demographics['user_dob'].replace('-', '').replace('/', '')[:4]
#                 patterns.extend([dd_mm, dd_mm[:2]+dd_mm[2:], dd_mm[2:]+dd_mm[:2]])
            
#             if 'spouse_dob' in demographics:
#                 spouse_dd_mm = demographics['spouse_dob'].replace('-', '').replace('/', '')[:4]
#                 patterns.extend([spouse_dd_mm, spouse_dd_mm[:2]+spouse_dd_mm[2:], spouse_dd_mm[2:]+spouse_dd_mm[:2]])
            
#             if 'anniversary' in demographics:
#                 anniv_dd_mm = demographics['anniversary'].replace('-', '').replace('/', '')[:4]
#                 patterns.extend([anniv_dd_mm, anniv_dd_mm[:2]+anniv_dd_mm[2:], anniv_dd_mm[2:]+anniv_dd_mm[:2]])
        
#         # For 6-digit MPINs
#         else:
#             # Check DDMMYY and YYMMDD patterns
#             if 'user_dob' in demographics:
#                 dob_parts = demographics['user_dob'].replace('-', '').replace('/', '')
#                 if len(dob_parts) >= 6:  # Full date available
#                     patterns.extend([
#                         dob_parts[:6],  # DDMMYY
#                         dob_parts[4:6] + dob_parts[2:4] + dob_parts[:2],  # YYMMDD
#                         dob_parts[:2] + dob_parts[2:4] + dob_parts[4:6],  # DDMMYY
#                         dob_parts[4:6] + dob_parts[:4],  # YYDDMM
#                         dob_parts[2:4] + dob_parts[:2] + dob_parts[4:6]  # MMDDYY
#                     ])
            
#             if 'spouse_dob' in demographics:
#                 spouse_dob_parts = demographics['spouse_dob'].replace('-', '').replace('/', '')
#                 if len(spouse_dob_parts) >= 6:
#                     patterns.extend([
#                         spouse_dob_parts[:6],
#                         spouse_dob_parts[4:6] + spouse_dob_parts[2:4] + spouse_dob_parts[:2],
#                         spouse_dob_parts[:2] + spouse_dob_parts[2:4] + spouse_dob_parts[4:6],
#                         spouse_dob_parts[4:6] + spouse_dob_parts[:4],
#                         spouse_dob_parts[2:4] + spouse_dob_parts[:2] + spouse_dob_parts[4:6]
#                     ])
            
#             if 'anniversary' in demographics:
#                 anniv_parts = demographics['anniversary'].replace('-', '').replace('/', '')
#                 if len(anniv_parts) >= 6:
#                     patterns.extend([
#                         anniv_parts[:6],
#                         anniv_parts[4:6] + anniv_parts[2:4] + anniv_parts[:2],
#                         anniv_parts[:2] + anniv_parts[2:4] + anniv_parts[4:6],
#                         anniv_parts[4:6] + anniv_parts[:4],
#                         anniv_parts[2:4] + anniv_parts[:2] + anniv_parts[4:6]
#                     ])
        
#         # Check if MPIN matches any demographic pattern
#         for pattern in patterns:
#             if mpin == pattern:
#                 if pattern.startswith(demographics.get('user_dob', 'XX')[:2]):
#                     reasons.append('DEMOGRAPHIC_DOB_SELF')
#                 elif 'spouse_dob' in demographics and pattern.startswith(demographics['spouse_dob'][:2]):
#                     reasons.append('DEMOGRAPHIC_DOB_SPOUSE')
#                 elif 'anniversary' in demographics and pattern.startswith(demographics['anniversary'][:2]):
#                     reasons.append('DEMOGRAPHIC_ANNIVERSARY')
#                 break
        
#         return reasons
    
#     def generate_strong_pin(self):
#         """Generate a random strong PIN that doesn't match common patterns"""
#         import random
#         while True:
#             pin = ''.join([str(random.randint(0, 9)) for _ in range(self.pin_length)])
#             result = self.analyze(pin)
#             if result['strength'] == 'STRONG':
#                 return pin






class MPINAnalyzer:
    COMMON_4DIGIT_PINS = [
        '1234', '1111', '0000', '1212', '7777', '1004', '2000', '4444', '2222',
        '6969', '9999', '3333', '5555', '6666', '1122', '1313', '8888', '4321',
        '2001', '1010', '2580', '0007', '1818', '1230', '1110', '1210', '1000'
    ]
    
    COMMON_6DIGIT_PINS = [
        '123456', '111111', '000000', '121212', '112233', '123123', '123321',
        '654321', '111222', '121314', '100100', '200200', '102030', '110110',
        '101010', '112211', '200000', '123654', '111000', '147258', '258369'
    ]

    def __init__(self, pin_length=4):
        self.pin_length = pin_length
        self.common_pins = self.COMMON_6DIGIT_PINS if pin_length == 6 else self.COMMON_4DIGIT_PINS
        
    def analyze(self, mpin, demographics=None):
        reasons = []
        
        # Validate input length
        if len(mpin) != self.pin_length or not mpin.isdigit():
            return {
                'valid': False,
                'strength': 'INVALID',
                'reasons': ['INVALID_LENGTH' if len(mpin) != self.pin_length else 'NON_DIGIT']
            }
        
        # Check for common PINs
        if mpin in self.common_pins:
            reasons.append('COMMONLY_USED')
        
        # Check demographic patterns if provided
        if demographics:
            reasons += self._check_demographic_patterns(mpin, demographics)
        
        strength = 'STRONG' if not reasons else 'WEAK'
        
        return {
            'valid': True,
            'strength': strength,
            'reasons': reasons
        }
    
    def _check_demographic_patterns(self, mpin, demographics):
        reasons = []
        patterns = []
        
        # Extract dates in DDMM format
        def extract_dates(date_str):
            if not date_str:
                return []
            
            # Clean the date string
            clean_date = ''.join(c for c in date_str if c.isdigit())
            
            dates = []
            if len(clean_date) >= 4:
                # DDMM format
                dd_mm = clean_date[:2] + clean_date[2:4]
                dates.append(dd_mm)
                # MMDD format
                dates.append(clean_date[2:4] + clean_date[:2])
                # Last 2 digits of year + DD
                if len(clean_date) >= 6:
                    dates.append(clean_date[4:6] + clean_date[:2])
                    # DD + last 2 digits of year
                    dates.append(clean_date[:2] + clean_date[4:6])
            
            return dates

        # For 4-digit MPINs
        if self.pin_length == 4:
            # Check user DOB patterns
            user_dates = extract_dates(demographics.get('user_dob', ''))
            if mpin in user_dates:
                reasons.append('DEMOGRAPHIC_DOB_SELF')
            
            # Check spouse DOB patterns
            spouse_dates = extract_dates(demographics.get('spouse_dob', ''))
            if mpin in spouse_dates:
                reasons.append('DEMOGRAPHIC_DOB_SPOUSE')
            
            # Check anniversary patterns
            anniv_dates = extract_dates(demographics.get('anniversary', ''))
            if mpin in anniv_dates:
                reasons.append('DEMOGRAPHIC_ANNIVERSARY')
        
        # For 6-digit MPINs
        else:
            # Extract dates in DDMMYY format
            def extract_6digit_dates(date_str):
                if not date_str:
                    return []
                
                clean_date = ''.join(c for c in date_str if c.isdigit())
                if len(clean_date) < 6:
                    return []
                
                dates = []
                # DDMMYY
                dates.append(clean_date[:6])
                # YYMMDD
                dates.append(clean_date[4:6] + clean_date[2:4] + clean_date[:2])
                # MMDDYY
                dates.append(clean_date[2:4] + clean_date[:2] + clean_date[4:6])
                # DDYYMM
                dates.append(clean_date[:2] + clean_date[4:6] + clean_date[2:4])
                # YYDDMM
                dates.append(clean_date[4:6] + clean_date[:2] + clean_date[2:4])
                
                return dates

            # Check user DOB patterns
            user_dates = extract_6digit_dates(demographics.get('user_dob', ''))
            if mpin in user_dates:
                reasons.append('DEMOGRAPHIC_DOB_SELF')
            
            # Check spouse DOB patterns
            spouse_dates = extract_6digit_dates(demographics.get('spouse_dob', ''))
            if mpin in spouse_dates:
                reasons.append('DEMOGRAPHIC_DOB_SPOUSE')
            
            # Check anniversary patterns
            anniv_dates = extract_6digit_dates(demographics.get('anniversary', ''))
            if mpin in anniv_dates:
                reasons.append('DEMOGRAPHIC_ANNIVERSARY')
        
        return reasons
    
    def generate_strong_pin(self):
        """Generate a random strong PIN that doesn't match common patterns"""
        import random
        while True:
            pin = ''.join([str(random.randint(0, 9)) for _ in range(self.pin_length)])
            result = self.analyze(pin)
            if result['strength'] == 'STRONG':
                return pin