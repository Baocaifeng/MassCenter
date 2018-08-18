#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
#data type
class OBJECT :
    def __init__(self, _id, _type):
        self._id = _id
        self._type = _type
    #return object by _id        
    def getObjectById(self, _id, _conter):
        for con in _conter :
            if (con._id == _id) :
                return con    

class FACE(OBJECT):
    def __init__(self, _id, _type, outer_loop, inner_loops):
        self._id = _id
        self._type = _type
        self._inner_loops = inner_loops
        self._outer_loop = outer_loop
         
    def getMassCenter(self, loops, vertices):
        ver1 = self._inner_loops[:]
        temp = []
        for v in ver1 :
            inner_loop = self.getObjectById(v, loops)
            [s, area, center]=inner_loop.getFactor(vertices) 
            area = -area
            temp.append([area, center])
        
        ver2 = self._outer_loop[:]
        outer_loop = self.getObjectById(ver2, loops)
        [s, area, center]=outer_loop.getFactor(vertices)
        temp.append([area, center])    
        
        area = 0
        x = 0
        y = 0
        for i in range(len(temp)):
            area = area+temp[i][0]
            x = x+temp[i][1][0]*temp[i][0]
            y = y+temp[i][1][1]*temp[i][0]
        
        x = x/area
        y = y/area 
        return [x, y] 
        
class LOOP(OBJECT):
    def __init__(self,_id, _type, _vertices):
        self._id =_id
        self._type = _type
        self._vertices = _vertices
             
    def getFactor(self, vertices):
        #tell concavity and convexity
        ver = self._vertices[:]
        if (len(ver)<3):
            print('invalid loop !')
            return None
        elif (len(ver)==3):
            s = ver[:]
            area = self.getTriAreaByVertice(ver, vertices)
            center = self.getTriCenterByVertice(ver, vertices)
            return [s, area, center]
        else:     
            [num, p] = self.tellConvexity(ver, vertices)
                    
            s = []
            area = []
            center = []   
            while (num>0):
                s_temp = [ver[p]]+[ver[p+1]]+[ver[p+2]]
                area_temp = self.getTriAreaByVertice(s_temp, vertices)
                center_temp = self.getTriCenterByVertice(s_temp, vertices)
                s.append(s_temp)
                area.append(area_temp)
                center.append(center_temp)
                ver.remove(ver[p+1])
                [num, p] = self.tellConvexity(ver, vertices)
            
            while (len(ver)>=3):
                s_temp = [ver[0]]+[ver[1]]+[ver[2]]
                area_temp = self.getTriAreaByVertice(s_temp, vertices)
                center_temp = self.getTriCenterByVertice(s_temp, vertices)
                s.append(s_temp)
                area.append(area_temp)
                center.append(center_temp)
                ver.remove(ver[1])
                    
            total_a = sum(area)
            total_x = 0
            total_y = 0
            for i in range(len(area)):
                total_x = total_x+area[i]*center[i][0]
                total_y = total_y+area[i]*center[i][1]
            total_x = total_x/total_a
            total_y = total_y/total_a     
            return [s, total_a, [total_x, total_y]]    
           
    #get area and center of triangle by vertices             
    def getTriAreaByVertice(self, points, vertices):
        if (len(points)==3) :
            a = self.getVertexById(points[0], vertices)
            b = self.getVertexById(points[1], vertices)
            c = self.getVertexById(points[2], vertices)
            area = (a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y))/2 
            return abs(area)  
         
    def getTriCenterByVertice(self, points, vertices):
        if (len(points) == 3):  
            sum_x=0
            sum_y=0
            for ver in points :
                for vertex in vertices :
                    if (ver == vertex._id) :
                        sum_x  = sum_x + vertex.x
                        sum_y  = sum_y + vertex.y   
                                         
            center_x = sum_x/len(points)
            center_y = sum_y/len(points)
            return [center_x, center_y]        
            
    def getVertexById(self, point_id, vertices):
        for ver in vertices :
            if (ver._id == point_id) :
                return ver      
            
    def tellConvexity(self, points, vertices):
        #tell concavity and convexity
        if (len(points)>3) : 
            t = []
            for i in range(len(points)):
                j = i+1
                k = i+2
                if (j>= len(points)):
                    j = j-len(points)
                if (k>= len(points)):
                    k = k-len(points)
                        
                v0 = self.getVertexById(points[i], vertices)  
                v1 = self.getVertexById(points[j], vertices)
                v2 = self.getVertexById(points[k], vertices)      
                #v01 = [(v1.x-v0.x) (v1.y-v0.y)]
                #v12 = [(v2.x-v1.x) (v2.y-v1.y)]
                t0 = (v1.x-v0.x)*(v2.y-v1.y)-(v2.x-v1.x)*(v1.y-v0.y) 
                if (t0<0):
                    t.append(-1)
                else :
                    t.append(1)       
            num = t.count(1) 
            if (num>0):
                p = t.index(1)+1  
            else:
                p = None    
            return [num, p]         

class VERTEX(OBJECT):
    def __init__(self,_id, _type, position):
        self._id =_id
        self._type = _type 
        [x, y] = self.getPosition(position)
        self.x = x
        self.y = y
        
    def getPosition(self, position):
        if '|' in position :
            p = position.find('|')
            x = float(position[:p])
            y = float(position[p+1:])
            return [x, y]
        else :
            print('invalid position !')
            
def main():
    #input
    f = open('inputData.txt','r')
    a = f.read()
    f.close()
    dic = eval(a)
    
    vertices = []
    for ver in dic['vertices'] :
        v = VERTEX(ver['id'],ver['type'],ver['position'])
        vertices.append(v)
    loops = []
    for loop in dic['loops'] :
        l = LOOP(loop['id'], loop['type'], loop['vertices'])
        loops.append(l)
    faces = []
    for face in dic['faces'] :
        f = FACE(face['id'], face['type'], face['outer_loop'], face['inner_loops'])
        faces.append(f)
    
    #output
    for face in faces :
        [x, y] = face.getMassCenter(loops, vertices)
        x = format(x, '.2f')
        y = format(y, '.2f')
        print(face._id + ' => '+ str(x)+'|'+str(y))

if __name__ == '__main__' :
    main()    
    