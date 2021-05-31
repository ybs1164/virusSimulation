import objects.map as map

m = map.Map(100, 100,
            count=100, # 사람 수
            incount=1, # 감염자 수
            recount=0, # 완치자 수
            per=0.15, # 감염 확률
            reper=0., # 재감염 확률
            radius=6, # 감염 범위
            speed=0.5, # 이동 속도
            retime=200, # 회복 시간
            distanceRadius=6) # 거리두기 거리