"""
Custom error codes and errors to be sent in response body.
"""

class InvalidOffset():
    """
    Error class with custom error_code, error.
    Called if Parameter ``offset`` is invalid.
    """
    def __init__(self):
        self.error_code = 4019  #: error_code = 4019
        self.error = "Invalid 'offset'"  #: error = "Invalid 'offset'"


class InvalidLimit():
    """
    Error class with custom error_code, error.
    Called if Parameter ``limit`` is invalid.
    """
    def __init__(self):
        self.error_code = 4020  #: error_code = 4020
        self.error = "Invalid 'limit'"  #: error = "Invalid 'limit'"


class InvalidReqParams():
    """
    Error class with custom error_code, error.
    Called if Parameter ``limit`` is invalid.
    """
    def __init__(self):
        self.error_code = 4040  #: error_code = 4020
        self.error = "Invalid 'Request Parameters'"  #: error = "Invalid 'limit'"

        
class invalidStartDate():
    """
    Error class with custom error_code, error.
    Called if Parameter ``review_start_date`` is invalid.
    """
    def __init__(self):
        self.error_code = 4043  #: error_code = 4043
        self.error = "Invalid 'review_start_date'"  #: error = "Invalid 'review_start_date'"


class invalidEndDate():
    """
    Error class with custom error_code, error.
    Called if Parameter ``review_end_date`` is invalid.
    """
    def __init__(self):
        self.error_code = 4044  #: error_code = 4043
        self.error = "Invalid 'review_end_date'"  #: error = "Invalid 'review_end_date'"

class StartDateMissing():
    """
    Error class with custom error_code, error.
    Called if Parameter ``review_start_date`` is invalid.
    """
    def __init__(self):
        self.error_code = 4045  #: error_code = 4043
        self.error = "'review_start_date Missing'"  #: error = "Invalid 'review_start_date'"


class EndDateMissing():
    """
    Error class with custom error_code, error.
    Called if Parameter ``review_end_date`` is invalid.
    """
    def __init__(self):
        self.error_code = 4046  #: error_code = 4046
        self.error = "'review_end_date Missing'"  #: error = "Invalid 'review_end_date'"


class invalidDateRange():
    """
    Error class with custom error_code, error.
    Called if Parameter ``Invalid Date Range`` is invalid.
    """
    def __init__(self):
        self.error_code = 4047  #: error_code = 4047
        self.error = "'review_end_date' cannot be less than 'review_start_date'"  #: error =
        # "Invalid 'Date range'"


class invalidRestaurantID():
    """
    Error class with custom error_code, error.
    Called if Parameter ``Invalid Restaurant ID`` is invalid.
    """
    def __init__(self):
        self.error_code = 4049  #: error_code = 4049
        self.error = "Invalid 'restaurant_id'"  #: error = "Invalid 'restaurant_id'"


class invalidRating():
    """
    Error class with custom error_code, error.
    Called if Parameter ``Invalid Rating`` is invalid.
    """
    def __init__(self):
        self.error_code = 4050  #: error_code = 4050
        self.error = "Invalid 'review_rating' it should be like '1,2,3,4,5' values 1 to 5 allowed"  #: error = "Invalid 'review_rating'"


class invalidRecommendedVal():
    """
    Error class with custom error_code, error.
    Called if Parameter ``Invalid Recommended`` is invalid.
    """
    def __init__(self):
        self.error_code = 4050  #: error_code = 4050
        self.error = "Invalid 'recommended' it should be 'Yes' or 'No'"  #: error = "Invalid 'recommended'"


