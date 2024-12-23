# Standard / external libraries
import django
import rest_framework
import rest_framework.views
import rest_framework.response
import math
import statistics

# External modules
import xpt_utils as xu

# Internal modules
import FoodDemocraty.models

# Core code
SELECTED_CHOICES = 3

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

    users = len(user_vote_dict)
    choice_score_dict = {} # {choice_id : mean}
    for choice_id, grade_list in choice_grade_dict.items():
        padd_grade_list = grade_list + [2] * (users - len(grade_list))
        median          = math.ceil(statistics.median(padd_grade_list))
        score           = median
        # Reducing equal score occurences
        for grade in padd_grade_list:
            if (grade < median):
                score -= 1 / users
            if (grade > median):
                score += 0.5 / users
        choice_score_dict[choice_id] = round(score, 3)

    return choice_score_dict

class CountingView(rest_framework.views.APIView):
    def post(self, request, *args, **kwargs):
        choice_score_dict = counting(request.data)

        choices = 0
        selected_choice_list = []
        for cid, score in sorted(choice_score_dict.items(), key=lambda item: item[1], reverse=True):
            if (choices < SELECTED_CHOICES):
                restaurant = FoodDemocraty.models.Restaurant.objects.get(id=cid)
                selected_choice_dict = {}
                selected_choice_dict["id"]          = cid
                selected_choice_dict["name"]        = restaurant.name
                selected_choice_dict["description"] = restaurant.description
                selected_choice_dict["score"]        = score
                selected_choice_list.append(selected_choice_dict)
                choices += 1
            else:
                break

        return rest_framework.response.Response(selected_choice_list, status=rest_framework.status.HTTP_201_CREATED)
