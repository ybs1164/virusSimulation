import matplotlib.pyplot as plt
import objects.map as map

# m = map.Map(100, 100,
#             count=200, # 사람 수
#             incount=1, # 감염자 수
#             recount=0, # 완치자 수
#             per=0.15, # 감염 확률
#             reper=0.05, # 재감염 확률
#             radius=4, # 감염 범위
#             speed=0.8, # 이동 속도
#             retime=200, # 회복 시간
#             distanceRadius=4) # 거리두기 거리

#m = map.ClassRoom()

m = map.LunchRoom()

plt.show()