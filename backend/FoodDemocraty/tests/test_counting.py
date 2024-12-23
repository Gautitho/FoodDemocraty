# Standard / external libraries
import sys
import os
import django

# External modules
import xpt_utils as xu

# Internal modules
import FoodDemocraty.services

class CountingTestCase(django.test.TestCase):

    ###########################################
    # Test 0
    #   6 users
    #   5 choices
    ###########################################
    def test_counting_0(self):
        # user_vote_dict = {user_id : {choice_id : grade}}
        user_vote_dict = {}
        user_vote_dict[0] = {}
        user_vote_dict[0][0] = 2
        user_vote_dict[0][1] = 2
        user_vote_dict[0][2] = 2
        user_vote_dict[0][3] = 2
        user_vote_dict[0][4] = 2

        user_vote_dict[1] = {}
        user_vote_dict[1][0] = 3
        user_vote_dict[1][2] = 3
        user_vote_dict[1][4] = 0

        user_vote_dict[2] = {}
        user_vote_dict[2][0] = 5

        user_vote_dict[3] = {}
        user_vote_dict[3][0] = 4
        user_vote_dict[3][1] = 3
        user_vote_dict[3][3] = 2
        user_vote_dict[3][4] = 1

        user_vote_dict[4] = {}
        user_vote_dict[4][0] = 0
        user_vote_dict[4][1] = 1
        user_vote_dict[4][2] = 2
        user_vote_dict[4][3] = 3
        user_vote_dict[4][4] = 4

        user_vote_dict[5] = {}
        user_vote_dict[5][3] = 5
        user_vote_dict[5][4] = 5

        # expected_ranking_dict = {choice_id : score}
        expected_ranking_dict = {}
        expected_ranking_dict[0] = 2.667
        expected_ranking_dict[1] = 1.917
        expected_ranking_dict[2] = 2.083
        expected_ranking_dict[3] = 2.167
        expected_ranking_dict[4] = 1.833

        computed_ranking_dict = FoodDemocraty.services.counting(user_vote_dict)

        log_str = ""
        error   = False
        for choice_id, score in expected_ranking_dict.items():
            if (score == computed_ranking_dict[choice_id]):
                log_str += f"  Choice {choice_id} : OK (Expected ({score}) == Computed ({computed_ranking_dict[choice_id]}))\n"
            else:
                log_str += f"  Choice {choice_id} : KO (Expected ({score}) != Computed ({computed_ranking_dict[choice_id]}))\n"
                error   = True

        if error:
            log_str = f"Missmatch between computed and expected scores :\n" + log_str
            xu.format_log(log_str, type="ERROR")
            self.fail()
        else:
            log_str = "Computed scores matches with expected."
            xu.format_log(log_str, type="SUCCESS")