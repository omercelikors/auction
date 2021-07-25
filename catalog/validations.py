
class UserConfigValidation():

    FUND_FIELD_NAME = "Fund"
    MAX_BID_AMOUNT_FIELD_NAME = "Max bid amount"
    REQUIRED_MESSAGE = '{} is required'
    MIN_VAL_MESSAGE = "{} have to be bigger than {}"
    IS_NUMERIC_MESSAGE = "{} have to be numeric value"
    COMPARE_MESSAGE = "Fund field must be bigger than max bid amount field"

    def __init__(self, fund, max_bid_amount):
        self.all_messages = []
        self.fund = fund
        self.max_bid_amount = max_bid_amount

    def check_required(self):
        if not self.fund:
            self.all_messages.append(self.REQUIRED_MESSAGE.format(self.FUND_FIELD_NAME))
        if not self.max_bid_amount:
            self.all_messages.append(self.REQUIRED_MESSAGE.format(self.MAX_BID_AMOUNT_FIELD_NAME))
        return self.all_messages
    
    def check_min_val(self):
        if self.fund <= 0:
            self.all_messages.append(self.MIN_VAL_MESSAGE.format(self.FUND_FIELD_NAME, 0))
        if self.max_bid_amount <= 0:
            self.all_messages.append(self.MIN_VAL_MESSAGE.format(self.MAX_BID_AMOUNT_FIELD_NAME, 0))
        return self.all_messages

    def check_comparing(self):
        if self.fund < self.max_bid_amount:
            self.all_messages.append(self.COMPARE_MESSAGE)
        return self.all_messages

    def check_numeric(self):
        try:
            self.fund = int(self.fund)
        except ValueError:
            self.all_messages.append(self.IS_NUMERIC_MESSAGE.format(self.FUND_FIELD_NAME))
        
        try:
            self.max_bid_amount = int(self.max_bid_amount)
        except ValueError:
            self.all_messages.append(self.IS_NUMERIC_MESSAGE.format(self.MAX_BID_AMOUNT_FIELD_NAME))
        return self.all_messages
    
    def main(self):
        if self.check_numeric():
            return self.all_messages
        if self.check_required():
            return self.all_messages
        if self.check_min_val():
            return self.all_messages
        if self.check_comparing():
            return self.all_messages
