class charSet:
    """Handles character sets that do not display properly."""
    def __init__(self, characterSet):
        self.charSet = characterSet

    def isSpecial(self):
        if self.charSet == 'cp437':
            return True
        else:
            return False

    def specialChars(self):
        if self.charSet == 'cp437': # is known to have non-display characters like 'delete' instead of a glyph.
            return {1: u'\u263A',2: u'\u263B',3: u'\u2665',4: u'\u2666',5: u'\u2663',6: u'\u2660',7: u'\u2022',8: u'\u25D8',9: u'\u25CB',10: u'\u25D9',11: u'\u2642',12: u'\u2640',13: u'\u266A',14: u'\u266B',15: u'\u263C',16: u'\u25BA',17: u'\u25C4',18: u'\u2195',19: u'\u203C',20: u'\u00B6',21: u'\u00A7',22: u'\u25AC',23: u'\u21A8',24: u'\u2191',25: u'\u2193',26: u'\u2192',27: u'\u2190',28: u'\u221F',29: u'\u2194',30: u'\u25B2',31: u'\u25BC',127: u'\u2302'}
        else:
            return {}

