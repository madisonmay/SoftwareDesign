def sum13(nums):
  if len(nums) == 0:
    return 0
  res = 0
  if nums[0] != 13:
    res += nums[0]
  if len(nums) > 1:
    for i in range(1, len(nums)):
      if nums[i] != 13 and nums[i-1] != 13:
        res += nums[i] 
  return res

print sum13([13, 1, 2, 13, 2, 1, 13])