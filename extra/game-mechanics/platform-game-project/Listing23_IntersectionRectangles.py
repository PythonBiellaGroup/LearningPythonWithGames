
def RectanglesIntersect(centreA, halfSizeA, centreB, halfSizeB):
    if centreA[0] - halfSizeA[0] < centreB[0] + halfSizeB[0] and centreA[0] + halfSizeA[0] > centreB[0] - halfSizeB[0]:
        if centreA[1] - halfSizeA[1] < centreB[1] + halfSizeB[1] and centreA[1] + halfSizeA[1] > centreB[1] - halfSizeB[1]:
            return True
    return False        

