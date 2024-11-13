
#from typing import List

def add_em_up(nums: 'list'=[]) -> int:
    tot = 0
    for num in nums:
        tot += num
    return tot
mylist = [5,6,7,8]
sum = add_em_up(mylist)
print(sum)

