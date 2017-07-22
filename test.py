class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        result=0
        while len(height)>=2:
            cur_max=height[0]
            cur_second=0
            index_max=0
            index_second=0
            for i in range(1,len(height)):
                if height[i]>cur_max:
                    cur_second=cur_max
                    index_second=cur_second
                    cur_max=height[i]
                    index_max=i
                elif height[i]>cur_second:
                    cur_second=height[i]
                    index_second=i
            if index_max<index_second:
                for index in range(index_max+1,index_second):
                    result=+cur_second-height[index]
                del height[index_max:index_second]
            else:
                for index in range(index_second+1,index_max):
                    result=+cur_second-height[index]
                del height[index_second:index_max]
        return result

example=Solution()
print(example.trap([0,2,0]))