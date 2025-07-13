def num_dif(y, h, a, b, fr, fc, fp):
    ans1 = []
    ans2 = []
    for i in range(len(y)):
        if(i == 0):
            ans1.append(fp1(y[0],y[1],y[2],h))
            ans2.append(fp2(y[0],y[1],y[2],y[3],h))
        elif(i == len(y)-1):
            ans1.append(fr1(y[i-2],y[i-1],y[i],h))
            ans2.append(fr2(y[i-3],y[i-2],y[i-1],y[i],h))
        else:
            ans1.append(fc1(y[i+1],y[i-1],h))
            ans2.append(fc2(y[i-1],y[i],y[i+1],h))
    return ans1, ans2
        
def fr1(y1:float, y2:float, y3:float, h):
    return ((y1-4*y2+3*y3)/2*h)
def fr2(y1:float, y2:float, y3:float, y4:float, h):
    return ((-y1+4*y2-5*y3+2*y4)/h^2)
def fp1(y1:float, y2:float, y3:float, h):
    return ((-3*y3+4*y2-y1)/2*h)
def fp2(y1:float, y2:float, y3:float, y4:float, h):
    return ((2*y1-5*y2+4*y3-y4)/h^2)
def fc1(y1:float, y2:float, h):
    return ((y2-y1)/2*h)
def fc2(y1:float, y2:float, y3:float, h):
    return ((y1-2*y2+y3)/h^2)