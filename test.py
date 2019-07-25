#the import section
import random

current_recommendations = []

api_key = "3f44093c7132e8d90dfece35961ffafa"

def get_results(arr):
    result = []
    while (len(result) <= 5):
        index = random.randint(0,len(arr) - 1)
        if arr[index] not in result:
            result.append(arr.pop(index))
    return result


str = "What in god's name am i doing with my god's name am i doing with what am i life"
str_list = str.split()
print(str_list)
result = get_results(str_list)
print(result)
print(str_list)
