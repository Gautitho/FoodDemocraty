# Standard / external libraries
import django
import rest_framework
import rest_framework.views
import rest_framework.response
import numpy as np

# External modules
import xpt_utils as xu

# Internal modules
import FoodDemocraty.models

# Core code
SELECTED_CHOICES = 2

# user_vote_dict = {user_id : {choice_id : grade}}
def counting(user_vote_dict):
    choice_grade_dict = {} # {choice_id : [grade]}
    for user_id, choice_dict in user_vote_dict.items():
        for choice_id, grade in choice_dict.items():
            if (grade >= 0):
                if (choice_id in choice_grade_dict):
                    choice_grade_dict[choice_id].append(grade)
                else:
                    choice_grade_dict[choice_id] = [grade]

    choice_mean_dict = {} # {choice_id : mean}
    for choice_id, grade_list in choice_grade_dict.items():
        choice_mean_dict[choice_id] = np.mean(grade_list)

    choices = 0
    selected_choice_list = []
    for cid, mean in sorted(choice_mean_dict.items(), key=lambda item: item[1], reverse=True):
        if (choices < SELECTED_CHOICES):
            restaurant = FoodDemocraty.models.Restaurant.objects.get(id=cid)
            selected_choice_dict = {}
            selected_choice_dict["id"]          = cid
            selected_choice_dict["name"]        = restaurant.name
            selected_choice_dict["description"] = restaurant.description
            selected_choice_dict["mean"]        = mean
            selected_choice_list.append(selected_choice_dict)
        else:
            break

    return selected_choice_list

class CountingView(rest_framework.views.APIView):
    def post(self, request, *args, **kwargs):
        dic = counting(request.data)
        return rest_framework.response.Response(dic, status=rest_framework.status.HTTP_201_CREATED)
