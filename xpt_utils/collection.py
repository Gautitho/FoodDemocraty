import xpt_utils

def get_sub_dict(dic, key_list):
  sub_dic = {}
  for key in key_list:
    xpt_utils.check_condition(key in dic, f"Key ({key}) does not exist in dict !")
    sub_dic[key] = dic[key]
  return sub_dic
