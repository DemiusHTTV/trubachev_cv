import matplotlib.pyplot as plt 
import numpy as np 

class ImagingModel():
    def __init__(self,shape=(256,256)):
        self.h, self.w = shape
        self.y, self.x = np.meshgrid(np.arange(self.h),
                                                np.arange(self.w))
    def create_reflection(self, background =0.85,foreground = 0.03):
        n =np.zeros((self.h,self.w)) + background
        circle = ((self.x -self.w//2)**2 + (self.y-self.h//2)**2)<100**2
        n[circle]=foreground
        return n
    def point_light(self,cx,cy):
        distance = np.sqrt((self.x - cx)**2 + (self.y -cy)**2)
        return np.exp(-distance/50)
    
model = ImagingModel((512,512))
r =model.create_reflection()

plt.ion()
p1 = (model.h//2,model.w//2)
p2 = [10,10]
p3 =[model.h - 10 , model.w -10]
interns_p1 = []
interns_p2 = []
interns_p3 = []
iters =4
step = 5
for angle, rad in zip(range(0,360*iters,step),np.linspace(50,50,250,int(360*iters/step))):
    x = model.w//2 +rad* np.cos(np.deg2rad(angle))
    y = model.w//2 +rad* np.sin(np.deg2rad(angle))
    i = model.point_light(x,y)
    f =r *i
    interns_p1.append(f[*p1])
    interns_p1.append(f[*p2])
    interns_p1.append(f[*p3])
    plt.clf()
    plt.clim(0,1)
    plt.subplot(121)
    plt.scatter(p1[1],p1[0])
    plt.scatter(p1[1],p1[0])
    plt.scatter(p1[1],p1[0])
    plt.subplot(122)
    plt.plot(interns_p1, label='p1')
    plt.plot(interns_p2, label='p2')
    plt.plot(interns_p3, label='p3')
    plt.legend()
    plt.imshow(f)
    plt.pause(0.01)
    if not plt. get_fignums():
        break
plt.ioff()
plt.show