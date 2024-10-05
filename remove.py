from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        
        nums = sorted(nums)
        output = []

        seen = []

        for pos1, num1 in enumerate(nums):
            for pos2, num2 in enumerate(nums): 
                if [num1, num2] in seen or [num2, num1] in seen:
                    continue

                seen.append([num1, num2])
                
                if pos1 == pos2:
                    continue

                start = 0 
                end = len(nums) - 1
                target = - (num1 + num2)
                done = False

                while start < end and not done: 
                    middle = (start + end) // 2
                    print(start, end, middle)

                    while middle == pos1 or middle == pos2:
                        if middle > len(nums): 
                            done = True
                            break
                        middle += 1
                        
                    if nums[middle] == target:
                        output.append([num1, num2, target])
                        break
                    elif start == end - 1: 
                        break
                    elif nums[middle] < target: 
                        start = middle
                    else: 
                        end = middle

        return output
        

s = Solution()

print(s.threeSum([-1,0,1,2,-1,-4]))
