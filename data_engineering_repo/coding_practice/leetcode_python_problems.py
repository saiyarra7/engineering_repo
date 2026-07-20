#1. Two Sum
#Brute force solution - O(n*n) complexity
class Solution:
    def twoSumbruteforce(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i+1,n):
                if nums[i]+nums[j] == target:
                    return [i,j]

        return[]
    
# optimized linear time O(n) time complexity
    def twoSumhashmaps(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i,n in enumerate(nums):
            diff = target - n
            if diff in seen:
                return (seen[diff],i)
            else:
                 seen[n] = i
        return []

    


