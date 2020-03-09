from django.db import models

class PrimarySector(models.Model):
    name = models.CharField(max_length=10)

class SecondarySector:
    pass

class TertiarySector:
    pass


'''
가정/생활
건강/미용
결혼/출산/육아
교육/취업
금융/보험
꽃/이벤트
레저스포츠/취미
문화/미디어
부동산
산업기기
성인
식품/음료
여행/교통
의류/패션잡화
인쇄/문구/사무기기
자동차
전문서비스
전자/가전
IT/텔레콤
건축/인테리어

'''