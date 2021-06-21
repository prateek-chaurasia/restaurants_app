import json
import re
from datetime import date, datetime, time
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from apps.helpers import *


def is_valid_request_params(input_params, valid_params, api_name=None, mandatory_params=None):
    if input_params:
        for item in input_params:
            if item not in valid_params:
                return InvalidReqParams().__dict__
                

def is_param_valid_client_api(request, api_name):
    """
    This function validates the request parameters for Client API.
    """
    offset = request.GET.get('offset', 0)
    if not isinstance(offset, int):
        return InvalidOffset().__dict__
    limit = request.GET.get('limit', 0)
    if not isinstance(limit, int):
        return InvalidLimit().__dict__
    if offset < 0:
        return InvalidOffset().__dict__
    if limit < 0:
        return InvalidLimit().__dict__
    
    if (api_name == 'get_restaurants'):
        error_dict = {}
        valid_params = ['limit', 'offset', 'restaurant_id', 'review_rating', 
                            'review_start_date', 'review_end_date', 'recommended']
        input_params = request.GET.keys()
        error_dict = is_valid_request_params(input_params, valid_params, api_name)
        if not error_dict:
            restaurant_ids = request.GET.get('restaurant_id')
            if 'restaurant_id' in input_params:
                if not isinstance(restaurant_ids, str):
                    return invalidRestaurantID().__dict__

            if 'review_rating' in input_params:
                review_rating = request.GET.get('review_rating')
                if not isinstance(review_rating, str):
                    return invalidRating().__dict__
                elif int(review_rating) not in [1,2,3,4,5]:
                    return invalidRating().__dict__

            if 'recommended' in input_params:
                recommended = request.GET.get('recommended')
                if not isinstance(recommended, str):
                    return invalidRecommendedVal().__dict__
                elif recommended not in ["Yes", "No"]:
                    return invalidRecommendedVal().__dict__

            if 'review_start_date' in input_params:
                try:
                    if request.GET.get('review_start_date'):
                        start_date = datetime.strptime(request.GET.get('review_start_date'), '%Y-%m-%d')
                        min_start_date = datetime.combine(start_date, time.min)
                    if request.GET.get('review_start_date')=='':
                        return invalidStartDate().__dict__
                except:
                    return invalidStartDate().__dict__

            if 'review_end_date' in input_params:
                try:
                    if request.GET.get('review_end_date'):
                        end_date = datetime.strptime(request.GET.get('review_end_date'), '%Y-%m-%d')
                        max_end_date = datetime.combine(end_date, time.max)
                    if request.GET.get('review_end_date')=='':
                        return invalidEndDate().__dict__
                except:
                    return invalidEndDate().__dict__

            if 'review_start_date' in input_params and 'review_end_date' in input_params: 
                try:
                    if min_start_date and max_end_date:
                        if min_start_date > max_end_date:
                            return invalidDateRange().__dict__
                except:
                    pass
        else:
            return error_dict

    return None
