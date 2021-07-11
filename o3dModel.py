#import re
import numpy as np
from numpy.lib import recfunctions as rfn
import tokenize
import sys
import os

def toUint(bytes):
        return int.from_bytes(bytes,"little",signed=False)

def fromUint(uint,byteamount):
    return int.to_bytes(uint,byteamount,byteorder='little',signed=False)

fmflag=False

class Points:
    def __init__(self,file=None,parent=None) -> None:
        if file==None and parent==None:
            self.amount=0
            self.__store=[]
            self.coords=[]
            self.normals=[]
            self.texcoords=[]
        else:
            self.__initwithFile(file,parent)
    def __initwithFile(self,file,parent):
        if toUint(file.read(1))!=23:
            print("[Warning] file may contain errors {points marker wrong}")
        self.amount=toUint(file.read(2)) if parent.version<3 else toUint(file.read(4))
        if parent.udCorrect:               
            self.__store=[]
            zinit=0
            parent.kwak=np.dtype("<u2").type(parent.kwak)
            pcm65000=self.amount%65000
            for _ in range(self.amount):
                line=np.frombuffer(file.read(32),np.dtype("<f4")).copy()
                if parent.udata==0:
                    parent.kwak=304 if parent.f2 else 0 
                parent.kwak=((parent.kwak+zinit)*pcm65000)%8000
                floating_part=1
                for o in range(3):
                    floating_part*=line[o]-np.trunc(line[o])
                zinit=np.trunc((np.abs(floating_part)*600.)%256).astype(np.dtype("<u1"))
                copy_y=line[1]
                copy_x=line[0]
                if parent.kwak<1000:
                    line[1]=line[0]
                    line[0]=copy_y
                elif parent.kwak<3000:
                    line[0]=line[2]
                    line[2]=copy_x
                elif parent.kwak>7000:
                    line[1]=line[2]
                    line[2]=copy_y
                if parent.kwak&3==0:
                    line[3]*=-1
                copy_x=line[3]
                if parent.kwak%6==0:
                    line[4]*=-1
                if parent.kwak%7==0:
                    line[5]*=-1
                copy_y=line[5]
                if parent.kwak<600:
                    line[5]=line[4]
                    line[4]=copy_y
                else:
                    if parent.kwak<4501:
                        if parent.kwak>6500:
                            line[3]=line[5]
                            line[5]=copy_x
                    else:
                        line[3]=line[4]
                        line[4]=copy_x
                if parent.kwak%5==0:
                    line[6]-=(parent.kwak%100)**2/10000.
                if parent.kwak%3==0:
                    line[7]-=(parent.kwak%50)**2/2500.
                self.__store.append(line)
            self.__store=np.array(self.__store,dtype=np.dtype("<f4")).copy()
        else:
            self.__store=np.frombuffer(file.read(32*self.amount),np.dtype("<f4")).reshape(self.amount,8)
        self.coords=self.__store[:,:3].copy()
        self.normals=self.__store[:,3:6]
        self.texcoords=self.__store[:,6:8]
    def debugOut(self):
        print(np.c_[self.coords,self.normals,self.texcoords])
    def _writeTo(self,file,parent):
        file.write(fromUint(23,1))
        pcopy=np.c_[self.coords,self.normals,self.texcoords]
        file.write(fromUint(pcopy.shape[0],2 if parent.version<3 else 4))
        if parent.udCorrect:
            zinit=0
            parent.kwak=np.dtype("<u2").type(parent.kwak)
            pcm65000=self.amount%65000
            for line in pcopy:
                if parent.udata==0:
                    parent.kwak=304 if parent.f2 else 0 
                parent.kwak=((parent.kwak+zinit)*pcm65000)%8000
                copy_y=line[1]
                copy_x=line[0]
                if parent.kwak<1000:
                    line[1]=line[0]
                    line[0]=copy_y
                elif parent.kwak<3000:
                    line[0]=line[2]
                    line[2]=copy_x
                elif parent.kwak>7000:
                    line[1]=line[2]
                    line[2]=copy_y
                floating_part=1
                for o in range(3):
                    floating_part*=line[o]-np.trunc(line[o])
                zinit=np.trunc((np.abs(floating_part)*600.)%256).astype(np.dtype("<u1"))
                copy_x=line[3]
                copy_y=line[5]
                if parent.kwak<600:
                    line[5]=line[4]
                    line[4]=copy_y
                else:
                    if parent.kwak<4501:
                        if parent.kwak>6500:
                            line[3]=line[5]
                            line[5]=copy_x
                    else:
                        line[3]=line[4]
                        line[4]=copy_x
                if parent.kwak&3==0:
                    line[3]*=-1 
                if parent.kwak%6==0:
                    line[4]*=-1
                if parent.kwak%7==0:
                    line[5]*=-1
                if parent.kwak%5==0:
                    line[6]+=(parent.kwak%100)**2/10000.
                if parent.kwak%3==0:
                    line[7]+=(parent.kwak%50)**2/2500.
        file.write(pcopy.tobytes())

class Faces:
    def __init__(self,file=None,parent=None) -> None:
        if file==None and parent==None:
            self.amount=0
            self.__store=[]
            self.indices=[]
            self.texIndice=[]
        else:
            self.__initwithFile(file,parent)
    def __initwithFile(self,file,parent):
        if toUint(file.read(1))!=73:
            print("[Warning] file may contain errors {faces marker wrong}")
        self.amount=toUint(file.read(2)) if parent.version<3 else toUint(file.read(4))#or <3 must check later maybe
        if parent.f1:
            self.__store=rfn.structured_to_unstructured(np.frombuffer(file.read(14*self.amount),np.dtype("<u4,<u4,<u4,<u2")),dtype=np.dtype("<u4"))#.reshape(self.amount,4)
        else:
            self.__store=np.frombuffer(file.read(8*self.amount),np.dtype("<u2")).reshape(self.amount,4)
        self.indices=self.__store[:,:3]
        self.texIndice=self.__store[:,3:4]
    def debugOut(self):
        print(np.c_[self.indices,self.texIndice])
    def _writeTo(self,file,parent):
        file.write(fromUint(73,1))
        pcopy=np.c_[self.indices,self.texIndice]
        file.write(fromUint(pcopy.shape[0],2 if parent.version<3 else 4))
        file.write(rfn.unstructured_to_structured(pcopy,np.dtype("<u4,<u4,<u4,<u2") if parent.f1 else np.dtype("<u2,<u2,<u2,<u2")).tobytes())

class Textures:
    def __init__(self,file=None) -> None:
        if file==None:
            self.amount=0
            self.fdata=[]
            self.names=[]
        else:
            self.__initwithFile(file)
    def __initwithFile(self,file) -> None:
        if toUint(file.read(1))!=38:
            print("[Warning] file may contain errors {textures marker wrong}")
        self.amount=toUint(file.read(2))
        self.names=[]
        self.fdata=[]#(diff?)faceColor(RGBA)specularColor(RGB)emissiveColor(RGB)power(float)
        for _ in range(self.amount):
            self.fdata.append(np.frombuffer(file.read(44),np.dtype("<f4")))#11x4(float)
            self.names.append(file.read(toUint(file.read(1))).decode())
    def _writeTo(self,file):
        file.write(fromUint(38,1))
        file.write(fromUint(self.amount,2))
        for i in range(self.amount):
            file.write(self.fdata[i].tobytes())
            encodedString=self.names[i].encode()
            file.write(fromUint(len(encodedString),1))
            file.write(encodedString)
    
class Model:
    def __Matrix(self,file=None):
        if file==None:
            self.matrix=[]
        else:
            self.__MatrixwithFile(file)
    def __MatrixwithFile(self,file):
        if toUint(file.read(1))!=121:  
            print("[Warning] file may contain errors {matrix marker wrong}")
        self.matrix=np.frombuffer(file.read(64),np.dtype("<f4")).reshape(4,4)#4x4x4(float)

    def __Matrix_writeTo(self,file):
        file.write(fromUint(121,1))
        file.write(self.matrix.tobytes())

    def align_vertices(self):
        points=np.c_[self.points.coords,np.ones(self.points.coords.shape[0])]
        points=points.dot(self.matrix)
        self.points.mcoords=np.copy((points/points[:,3:])[:,:3])

    def __update_vars(self):
        self.f1=True if self.flags&1==1 else False
        self.f2=True if self.flags&2==2 else False
        
        self.udCorrect= False if self.version<4 or self.udata==4294967295 else True
        if self.udCorrect:
            self.ud=self.udata+self.version-4
            self.kwak=(self.ud+381)%65000 if self.f2 else self.ud%65000
        else:
            self.ud=0
            self.kwak=0

    def __init__(self,filename=''):
        if filename=='':
            self.version=7
            self.flags=0
            self.udata=4294967295
            self.udCorrect=False
            self.__update_vars()
            self.points=Points()
            self.faces=Faces()
            self.textures=Textures()
            self.__Matrix()
        else:
            self.__initwithFile(filename)

    def __initwithFile(self,filename):
         with open(filename,'rb')as f:
            if toUint(f.read(2))==6532:
                self.version=toUint(f.read(1))
                
                if self.version>2:
                    self.flags=np.frombuffer(f.read(1),np.dtype("<u1"))[0]
                    if self.version>3:
                        self.udata=np.frombuffer(f.read(4),np.dtype("<u4"))[0]
                    else:
                        self.udata=0
                else:
                    self.udata=0
                    self.flags=0
                
                self.__update_vars()

                self.points=Points(f,self)#8x4(float)

                self.faces=Faces(f,self)#4x2(ushort)

                self.textures=Textures(f)
                
                self.__Matrix(f)
            else:
                print("[Warning] {o3d marker wrong}")
                self.__init__()

    def info(self):
        print("version:"+str(self.version))
        print(str(self.flags))
        print(str(self.udata))

    def pointsInfo(self):
        self.points.debugOut()

    def facesInfo(self):
        self.faces.debugOut()
        

    def matrixInfo(self):
        print(self.matrix)

    def texturesInfo(self):
        print("Textures:")
        for i in range(self.textures.amount):
            print("[{:3d}]".format(i),end=" ")
            print(self.textures.fdata[i],end=" ")
            print(self.textures.names[i])

    def extendedInfo(self):
        self.info()
        self.texturesInfo()
        self.pointsInfo()
        self.facesInfo()
        self.matrixInfo()

    def writeTo(self,filename,version,flag1:bool,flag2:bool,key):
        with open(filename,'wb')as file:
            file.write(fromUint(6532,2))
            file.write(fromUint(version,1))
            #protection
            if self.faces.amount>4294967295 and (flag1==False or version<3):
                if version<3:
                    version=3
                flag1=True
            self.version=version
            if self.version>2:
                self.flags=flag1&(flag2<<1)
                if self.version>3:
                    self.udata=key
                else:
                    self.udata=0
            else:
                self.udata=0
                self.flags=0
            self.f1=True if self.flags&1==1 else False
            self.f2=True if self.flags&2==2 else False
            
            self.udCorrect= False if self.version<4 or self.udata==4294967295 else True
            if self.udCorrect:
                self.ud=self.udata+self.version-4
                self.kwak=(self.ud+381)%65000 if self.f2 else self.ud%65000
            else:
                self.ud=0
                self.kwak=0

            if self.version>2:
                file.write(fromUint(self.flags,1))
                if self.version>3:
                    file.write(fromUint(self.udata,4))

            self.points._writeTo(file,self)
            self.faces._writeTo(file,self)
            self.textures._writeTo(file)
            self.__Matrix_writeTo(file)
    
    def exportDirectXAsciiFrame(self,filename):
        with open(filename,'w')as file:
            file.write("xof 0302txt 0064\ntemplate Header {\n <3D82AB43-62DA-11cf-AB39-0020AF71E433>\n WORD major;\n WORD minor;\n DWORD flags;\n}\n\ntemplate Vector {\n <3D82AB5E-62DA-11cf-AB39-0020AF71E433>\n FLOAT x;\n FLOAT y;\n FLOAT z;\n}\n\ntemplate Coords2d {\n <F6F23F44-7686-11cf-8F52-0040333594A3>\n FLOAT u;\n FLOAT v;\n}\n\ntemplate Matrix4x4 {\n <F6F23F45-7686-11cf-8F52-0040333594A3>\n array FLOAT matrix[16];\n}\n\ntemplate ColorRGBA {\n <35FF44E0-6C7C-11cf-8F52-0040333594A3>\n FLOAT red;\n FLOAT green;\n FLOAT blue;\n FLOAT alpha;\n}\n\ntemplate ColorRGB {\n <D3E16E81-7835-11cf-8F52-0040333594A3>\n FLOAT red;\n FLOAT green;\n FLOAT blue;\n}\n\ntemplate Material {\n <3D82AB4D-62DA-11cf-AB39-0020AF71E433>\n ColorRGBA faceColor;\n FLOAT power;\n ColorRGB specularColor;\n ColorRGB emissiveColor;\n [...]\n}\n\ntemplate MeshFace {\n <3D82AB5F-62DA-11cf-AB39-0020AF71E433>\n DWORD nFaceVertexIndices;\n array DWORD faceVertexIndices[nFaceVertexIndices];\n}\n\ntemplate MeshTextureCoords {\n <F6F23F40-7686-11cf-8F52-0040333594A3>\n DWORD nTextureCoords;\n array Coords2d textureCoords[nTextureCoords];\n}\n\ntemplate MeshMaterialList {\n <F6F23F42-7686-11cf-8F52-0040333594A3>\n DWORD nMaterials;\n DWORD nFaceIndexes;\n array DWORD faceIndexes[nFaceIndexes];\n [Material]\n}\n\ntemplate MeshNormals {\n <F6F23F43-7686-11cf-8F52-0040333594A3>\n DWORD nNormals;\n array Vector normals[nNormals];\n DWORD nFaceNormals;\n array MeshFace faceNormals[nFaceNormals];\n}\n\ntemplate Mesh {\n <3D82AB44-62DA-11cf-AB39-0020AF71E433>\n DWORD nVertices;\n array Vector vertices[nVertices];\n DWORD nFaces;\n array MeshFace faces[nFaces];\n [...]\n}\n\ntemplate FrameTransformMatrix {\n <F6F23F41-7686-11cf-8F52-0040333594A3>\n Matrix4x4 frameMatrix;\n}\n\ntemplate Frame {\n <3D82AB46-62DA-11cf-AB39-0020AF71E433>\n [...]\n}\n\n")
            for i in range(self.textures.amount):
                fd=self.textures.fdata[i]
                file.write(f"Material Material_{i+1} {{\n"\
					f" {fd[0]:.6f};{fd[1]:.6f};{fd[2]:.6f};{fd[3]:.6f};;\n"\
					f" {fd[10]:.6f};\n"\
					f" {fd[4]:.6f};{fd[5]:.6f};{fd[6]:.6f};;\n"\
					f" {fd[7]:.6f};{fd[8]:.6f};{fd[9]:.6f};;\n"\
					f" TextureFilename {{\n"\
					f" \"{self.textures.names[i]}\";\n"\
					f" }}\n"\
					f"}}\n"\
					f"\n")    
            #file.write()
            file.write("Header {\n 1;\n 0;\n 1;\n}\n")
            file.write("\nFrame Model1 {\n FrameTransformMatrix {\n")
            for o in range(len(self.matrix)):
                i=self.matrix[o]
                file.write(f"  {i[0]:.6f},{i[1]:.6f},{i[2]:.6f},{i[3]:.6f}")
                if o!=3:
                    file.write(",\n")
                else:
                    file.write(";;\n")
            file.write(" }\nMesh Model1 {\n")
            file.write(f" {self.points.amount};\n")
            for i in range(self.points.amount):
                o=self.points.coords[i]
                file.write(f" {o[0]:.6f};{o[2]:.6f};{o[1]:.6f};")
                if i!=self.points.amount-1:
                    file.write(",\n")
                else:
                    file.write(";\n")
            file.write(f"\n {self.faces.amount};\n")
            for i in range(self.faces.amount):
                o=self.faces.indices[i]
                file.write(f" 3;{o[2]},{o[1]},{o[0]};")
                if i!=self.faces.amount-1:
                    file.write(",\n")
                else:
                    file.write(";\n")
            file.write("\n MeshMaterialList {\n")
            file.write(f"  {self.textures.amount};\n")
            file.write(f"  {self.faces.amount};\n")
            for i in range(self.faces.amount):
                o=self.faces.texIndice[i]
                file.write(f"  {o[0]}")
                if i!=self.faces.amount-1:
                    file.write(",\n")
                else:
                    file.write(";;\n")
            for i in range(self.textures.amount):
                file.write(f"  {{Material_{i+1}}}\n")
            file.write(" }\n\n MeshNormals {\n")
            file.write(f"  {self.points.amount};\n")
            for i in range(self.points.amount):
                o=self.points.normals[i]
                file.write(f"  {o[0]:.6f};{o[2]:.6f};{o[1]:.6f};")
                if i!=self.points.amount-1:
                    file.write(",\n")
                else:
                    file.write(";\n")
            file.write(f"\n  {self.faces.amount};\n")
            for i in range(self.faces.amount):
                o=self.faces.indices[i]
                file.write(f"  3;{o[1]},{o[0]},{o[2]};")
                if i!=self.faces.amount-1:
                    file.write(",\n")
                else:
                    file.write(";\n")
            file.write(" }\n\n MeshTextureCoords {\n")
            file.write(f"  {self.points.amount};\n")
            for i in range(self.points.amount):
                o=self.points.texcoords[i]
                file.write(f"  {o[0]:.6f};{(1.-o[1]):.6f};")
                if i!=self.points.amount-1:
                    file.write(",\n")
                else:
                    file.write(";\n")
            file.write("  }\n }\n}")

    def importDirectXAsciiFrame(self,filename)->bool:
        with open(filename,'rb') as file:
            tokens=tokenize.tokenize(file.readline)
            token=tokens.__next__()
            if not(token.type==59 and token.string=='utf-8'):
                print('expected utf-8 but '+token.string+' present')
                return False
            token=tokens.__next__()
            if not(token.type==1 and token.string=='xof'):
                print('expected xof but '+token.string+' present')
                return False
            while True:
                token=tokens.__next__()
                if token.type==4 or token.type==58:
                    break
            def nt():
                token=tokens.__next__()
                while token.exact_type==4 or token.exact_type==58:
                    token=tokens.__next__()
                return token
            symbols={
                ';':13,'{':25,'}':26,',':12,'-':15
            }

            strucs={}#stub for vf
            def ss(symbol:str):
                token=nt()
                if token.exact_type!=symbols[symbol]:
                    print(f'expected {symbol} but '+token.string+' present')
                    return False
                return True
            def vn(varname:str):
                token=tokens.__next__()
                if token.exact_type==25:
                    return '{'
                if token.type!=1:
                    print(f'expected {varname} but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                    return False
                return token.string
            def et(tokenName:str):
                token=nt()
                if not(token.exact_type==1 and token.string==tokenName):
                    print(f'expected {tokenName} but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                    return False
                return True
            def st():#string
                token=nt()
                if token.exact_type!=3:
                    print('expected <string> but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                    return False
                return token.string[1:-1]
            def rv(count:int):
                vec=[]
                for _ in range(count):
                    token=nt()
                    if token.exact_type==15:
                        fv=-1
                        token=tokens.__next__()
                    else:
                        fv=1
                    if token.exact_type!=2:
                        print('expected number but '+token.string+' present')
                        return False
                    vec.append(fv*float(token.string))
                    if not ss(';'):return False
                return vec
            def fv(count:int):
                vec=[]
                for i in range(count):
                    token=nt()
                    if token.exact_type==15:
                        fv=-1
                        token=tokens.__next__()
                    else:
                        fv=1
                    if token.exact_type!=2:
                        print('expected number but '+token.string+' present')
                        return False
                    vec.append(fv*float(token.string))
                    if i!=count-1:
                        if not ss(','):return False
                return vec
            def vf()->bool:
                while True:
                    token=nt()
                    if token.exact_type==26:
                        return True
                    if token.exact_type==1:
                        if token.string in strucs:
                            if not strucs[token.string]():
                                print("failed parsing "+token.string)
                                return False
                            else:
                                continue
                        else:
                            print('unknown token present '+token.string)
                            return False
                    else:
                        print('expected <structName> but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                        return False

            def mf()->bool:
                v=vn('<materialName>')
                if not v:return False 
                if v!='{':
                    if not ss('{'):return False
                faceColor=rv(4)
                if not faceColor:return False
                if not ss(';'):return False
                power=rv(1)
                if not power:return False
                specularColor=rv(3)
                if not specularColor:return False
                if not ss(';'):return False
                emissiveColor=rv(3)
                if not emissiveColor:return False
                if not ss(';'):return False
                if not et('TextureFilename'):return False
                if not ss('{'):return False
                materialName=st()
                if not materialName:return False
                if not ss(';'):return False
                if not ss('}'):return False
                if not ss('}'):return False
                fdata=[]
                fdata.extend(faceColor)
                fdata.extend(specularColor)
                fdata.extend(emissiveColor)
                fdata.extend(power)
                self.textures.fdata.append(fdata)
                self.textures.names.append(materialName)
                if not fmflag:
                    self.textures.amount+=1
                return True
            def tf()->bool:
                v=vn('<structName>')
                if not v:return False 
                if v!='{':
                    if not ss('{'):return False
                counter=0
                while counter>=0:
                    token=tokens.__next__()
                    if token.exact_type==25:#{
                        counter+=1
                        continue
                    if token.exact_type==26:#}
                        if counter==0:
                            return True
                        else:
                            counter-=1
                print('no opening bracet }')
                return False
            def hf()->bool:
                if not ss('{'):return False
                if not rv(3):return False
                if not ss('}'):return False
                return True
            def ff()->bool:
                v=vn('<modelName>')
                if not v:return False
                if v!='{':
                    if not ss('{'):return False
                if not vf():return False
                return True
            def ft()->bool:
                if not ss('{'):return False
                matrix=fv(16)
                if not matrix:return False
                if self.matrix==[]:
                    self.matrix=np.array(matrix,dtype=np.dtype('<f4')).reshape(4,4)
                if not ss(';'):return False
                if not ss(';'):return False
                if not ss('}'):return False
                return True
            def me()->bool:
                v=vn('<modelName>')
                if not v:return False
                if v!='{':
                    if not ss('{'):return False
                pcount=rv(1)
                if not pcount:return False
                pcount=int(pcount[0])
                if self.points.amount==0:
                    self.points.amount=pcount
                if pcount!=self.points.amount:
                    print('Points amount mismatch')
                    return False
                matrix=[]
                for i in range(pcount):
                    line=rv(3)
                    if not line:return False
                    matrix.append(line)
                    if i!=pcount-1:
                        if not ss(','):return False
                    else:
                        if not ss(';'):return False
                if self.points.coords==[]:
                    self.points.coords=np.array(matrix,dtype=np.dtype('<f4')).reshape(pcount,3)
                
                fcount=rv(1)
                if not fcount:return False
                fcount=int(fcount[0])
                if self.faces.amount==0:
                    self.faces.amount=fcount
                if fcount!=self.faces.amount:
                    print('Faces amount mismatch')
                    return False
                matrix=[]
                for i in range(fcount):
                    polyVert=rv(1)
                    if not polyVert or polyVert[0]!=3:
                        print("The only supported type of polygons is triangles")
                        return False
                    line=fv(3)
                    if not line:return False
                    matrix.append(line)
                    if not ss(';'):return False
                    if i!=fcount-1:
                        if not ss(','):return False
                    else:
                        if not ss(';'):return False
                if self.faces.indices==[]:
                    self.faces.indices=np.array(matrix,dtype=np.dtype('<u4')).reshape(fcount,3)
                if not vf():return False
                return True
            def mm()->bool:
                global fmflag
                if not ss('{'):return False
                mcount=rv(1)
                if not mcount:return False
                mcount=int(mcount[0])
                if self.textures.amount==0:
                    fmflag=True
                    self.textures.amount=mcount
                if mcount!=self.textures.amount:
                    print('Material amount mismatch')
                    return False
                fcount=rv(1)
                if not fcount:return False
                fcount=int(fcount[0])
                if self.faces.amount==0:
                    self.faces.amount=fcount
                if fcount!=self.faces.amount:
                    print('Faces amount mismatch')
                    return False
                matrix=[]
                if fmflag:
                    for i in range(fcount):
                        line=rv(1)
                        if not line:return False
                        matrix.append(line)
                        if i!=fcount-1:
                            if not ss(','):return False
                        else:
                            if not ss(';'):return False
                else:
                    matrix=fv(fcount)
                    if not matrix: return False
                    if not ss(';'):return False
                    if not ss(';'):return False

                if self.faces.texIndice==[]:
                    self.faces.texIndice=np.array(matrix,dtype=np.dtype('<u4')).reshape(fcount,1)
                
                if fmflag:
                    if not vf(): return False
                    return True
                for _ in range(mcount):
                    if not ss('{'):return False
                    v=vn('<materialName>')
                    if not v:return False
                    if v=='{':
                        print('Nope, not this time')
                        return False
                    if not ss('}'):return False
                if not ss('}'):return False
                return True
            def mn()->bool:
                if not ss('{'):return False
                pcount=rv(1)
                if not pcount:return False
                pcount=int(pcount[0])
                if self.points.amount==0:
                    self.points.amount=pcount
                if pcount!=self.points.amount:
                    print('Points amount mismatch')
                    return False
                matrix=[]
                for i in range(pcount):
                    line=rv(3)
                    if not line:return False
                    matrix.append(line)
                    if i!=pcount-1:
                        if not ss(','):return False
                    else:
                        if not ss(';'):return False
                if self.points.normals==[]:
                    self.points.normals=np.array(matrix,dtype=np.dtype('<f4')).reshape(pcount,3)
                fcount=rv(1)
                if not fcount:return False
                fcount=int(fcount[0])
                if self.faces.amount==0:
                    self.faces.amount=fcount
                if fcount!=self.faces.amount:
                    print('Faces amount mismatch')
                    return False
                matrix=[]
                for i in range(fcount):
                    polyVert=rv(1)
                    if not polyVert or polyVert[0]!=3:
                        print("The only supported type of polygons is triangles")
                        return False
                    line=fv(3)
                    if not line:return False
                    matrix.append(line)
                    if not ss(';'):return False
                    if i!=fcount-1:
                        if not ss(','):return False
                    else:
                        if not ss(';'):return False
                if self.faces.indices==[]:
                    self.faces.indices=np.array(matrix,dtype=np.dtype('<u4')).reshape(fcount,3)
                if not ss('}'):return False
                return True
            def mt()->bool:
                global fmflag
                if not ss('{'):return False
                pcount=rv(1)
                if not pcount:return False
                pcount=int(pcount[0])
                if self.points.amount==0:
                    self.points.amount=pcount
                if pcount!=self.points.amount:
                    print('Points amount mismatch')
                    return False
                matrix=[]
                for i in range(pcount):
                    line=rv(2)
                    if not line:return False
                    matrix.append(line)
                    if fmflag:
                        if i==pcount-1:
                            if not ss(','):return False
                        else:
                            if not ss(';'):return False
                    else:
                        if i!=pcount-1:
                            if not ss(','):return False
                        else:
                            if not ss(';'):return False
                if self.points.texcoords==[]:
                    self.points.texcoords=np.array(matrix,dtype=np.dtype('<f4')).reshape(pcount,2)
                if not ss('}'):return False
                return True
            strucs={
                'Material':mf,
                'template':tf,
                'Header':hf,
                'Frame':ff,
                'FrameTransformMatrix':ft,
                'Mesh':me,
                'MeshMaterialList':mm,
                'MeshNormals':mn,
                'MeshTextureCoords':mt,
            }
            for i in tokens:
                if i.type==1:
                    if i.string in strucs:
                        if not strucs[i.string]():
                            print("failed parsing "+i.string)
                            return False
                    else:
                        print(i.type,i.exact_type,"'"+i.string+"'")    
                elif i.type==4 or i.type==58:
                    pass
                else:
                    print(i.type,i.exact_type,"'"+i.string+"'")
            if self.points.normals==[]:
                self.points.normals=np.c_[np.ones([self.points.amount,1]),np.zeros([self.points.amount,2])].astype(np.dtype('<f4'))
            self.textures.fdata=np.array(self.textures.fdata,dtype=np.dtype('<f4')).reshape(self.textures.amount,11).copy()
            self.points.coords=np.c_[self.points.coords[:,0],self.points.coords[:,2],self.points.coords[:,1]].copy()
            self.points.normals=np.c_[self.points.normals[:,0],self.points.normals[:,2],self.points.normals[:,1]].copy()
            self.points.texcoords[:,1]=1.-self.points.texcoords[:,1]
            self.faces.indices=np.c_[self.faces.indices[:,1],self.faces.indices[:,0],self.faces.indices[:,2]].copy()
            self.points.__store=np.c_[self.points.coords,self.points.normals,self.points.texcoords]
            self.faces.__store=np.c_[self.faces.indices,self.faces.texIndice]
            if self.matrix==[]:
                self.matrix=np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]],dtype=np.dtype('<f4'))
            if True:pass                
            else:
                print("Unsupported directx ascii frame format")
        return True

    def exportWaveFront(self,filename):
        matfilename=os.path.splitext(filename)[0]+'.mtl'
        with open(matfilename,'w')as file:
            for i in range(self.textures.amount):
                file.write('newmtl Material_'+str(i+1))
                cm=self.textures.fdata[i]
                file.write(f'\nKa {1:.6f} {1:.6f} {1:.6f}')
                file.write(f'\nKd {cm[0]:.6f} {cm[1]:.6f} {cm[2]:.6f}')
                file.write(f'\nKs {cm[4]:.6f} {cm[5]:.6f} {cm[6]:.6f}')
                file.write(f'\nKe {cm[7]:.6f} {cm[8]:.6f} {cm[9]:.6f}')
                file.write('\nillum 2')
                file.write(f'\nd {cm[3]:.6f}')
                file.write(f'\nNs {cm[10]:.6f}')
                file.write(f'\nmap_Kd {self.textures.names[i]}')
                file.write('\n\n')
        with open(filename,'w')as file:
            file.write('mtllib ') 
            file.write(os.path.split(matfilename)[1])
            file.write('\n\ng Object')
            for i in self.points.coords:
                file.write(f'\nv {-i[0]:.6f} {i[1]:.6f} {i[2]:.6f}')
            for i in self.points.normals:
                file.write(f'\nvn {i[0]:.6f} {i[1]:.6f} {i[2]:.6f}')
            for i in self.points.texcoords:
                file.write(f'\nvt {i[0]:.6f} {1-i[1]:.6f}')
            faces=np.c_[self.faces.indices+1,self.faces.texIndice]#.astype(np.dtype('<u4'))
            for i in range(self.textures.amount):
                file.write('\nusemtl Material_'+str(i+1))
                for o in faces:
                    if o[3]==i:
                        file.write(f'\nf {o[1]}/{o[1]}/{o[1]} {o[0]}/{o[0]}/{o[0]} {o[2]}/{o[2]}/{o[2]}')
                        #file.write(f'\nf {o[2]}/{o[2]}/{o[2]} {o[1]}/{o[1]}/{o[1]} {o[0]}/{o[0]}/{o[0]}')
                        #file.write(f'\nf {o[0]}/{o[0]}/{o[0]} {o[1]}/{o[1]}/{o[1]} {o[2]}/{o[2]}/{o[2]}')
                        #file.write(f'\nf {o[0]} {o[1]} {o[2]}')

    def importmtl(self,filename):
        mats={}
        with open(filename,'rb')as file:
            tokens=tokenize.tokenize(file.readline)
            token=tokens.__next__()
            if not(token.type==59 and token.string=='utf-8'):
                print('expected utf-8 but '+token.string+' present')
                return False
            def nn():
                while True:
                    token=tokens.__next__()
                    if token.exact_type==4 or token.exact_type==58 or token.exact_type==0:
                        break 
                return True                   
            def vn(varname:str):
                token=tokens.__next__()
                if token.type!=1:
                    print(f'expected {varname} but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                    return False
                return token.string
            def fc(cnt:int,notint:bool=True,negative:bool=False):
                numa=[]
                for _ in range(cnt):
                    num=tokens.__next__()
                    if negative and num.exact_type==15:
                        sign=-1
                        num=tokens.__next__()
                    else:
                        sign=1
                    if num.exact_type!=2:
                        print('expected <number> but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                        return False
                    if notint:
                        num=float(num.string)
                    else:
                        num=int(num.string)
                    num*=sign
                    numa.append(num)
                return numa

            colors={}

            def uc():
                nonlocal colors
                if colors!={}:
                    if 'n' not in colors:
                        print('missing materialTexture')
                        return False
                    if 'e' not in colors:
                        print('missing emissive color')
                        return False
                    if 's' not in colors:
                        print('missing specular color')
                        return False
                    if 'd' not in colors:
                        print('missing diffuse color')
                        return False
                    if 'o' not in colors:
                        print('missing opacity (d)')
                        return False
                    if 'i' not in colors:
                        print('missing power (Ns)')
                        return False
                    self.textures.names.append(colors['n'])
                    __arr=colors['d']
                    __arr.extend(colors['o'])
                    __arr.extend(colors['s'])
                    __arr.extend(colors['e'])
                    __arr.extend(colors['i'])
                    self.textures.fdata.append(__arr)
                    colors={}
                return True

            def nm()->bool:
                matName=vn("<materialName>")
                if not matName:return False
                mats[matName]=self.textures.amount
                if not uc():
                    print('current material is',{v:k for k,v in mats.items()}[self.textures.amount-1])  
                    return False
                nn()
                self.textures.amount+=1
                return True
            def kk(key:str,num:int)->bool:
                nonlocal colors
                numa=fc(num)
                if not numa:return False
                colors[key]=numa
                nn()
                return True
            def kd()->bool:
                if not kk('d',3):return False 
                return True
            def ks()->bool:
                if not kk('s',3):return False 
                return True
            def ke()->bool:
                if not kk('e',3):return False 
                return True
            def df()->bool:
                if not kk('o',1):return False 
                return True
            def ns()->bool:
                if not kk('i',1):return False 
                return True
            def mk()->bool:
                nonlocal colors
                __name=''
                while True:
                    i=tokens.__next__()
                    if i.exact_type==4 or i.exact_type==58:
                        break
                    __name+=i.string
                colors['n']=__name
                return True
            strucs={
                'newmtl':nm,
                'Ka':nn,
                'Kd':kd,
                'Ks':ks,
                'Ke':ke,
                'd':df,
                'Ns':ns,
                'illum':nn,
                'map_Kd':mk,
                'Ni':nn
            }
            for i in tokens:
                if i.type==1:
                    if i.string in strucs:
                        if not strucs[i.string]():
                            print("failed parsing "+i.string)
                            return False
                    else:
                        print(i.type,i.exact_type,"'"+i.string+"'")
                elif i.exact_type==57:
                    nn()
                elif i.type==4 or i.type==58:
                    pass
                else:
                    print(i.type,i.exact_type,"'"+i.string+"'")
            if not uc():
                print('current material is',{v:k for k,v in mats.items()}[self.textures.amount-1]) 
                return False
            self.textures.fdata=np.array(self.textures.fdata,dtype=np.dtype('<f4')).reshape(self.textures.amount,11).copy()
        return mats
            
    def importWaveFront(self,filename):
        with open(filename,'rb')as file:
            tokens=tokenize.tokenize(file.readline)
            token=tokens.__next__()
            if not(token.type==59 and token.string=='utf-8'):
                print('expected utf-8 but '+token.string+' present')
                return False
            def nt():
                token=tokens.__next__()
                while token.exact_type==4 or token.exact_type==58:
                    token=tokens.__next__()
                return token
            matnames={}
            currentmaterial=-1
            adv_face=[]
            symbols={
                ';':13,'{':25,'}':26,',':12,'-':15,'#':57,'/':17
            }
            def nn():
                while True:
                    token=tokens.__next__()
                    if token.exact_type==4 or token.exact_type==58 or token.exact_type==0:
                        break  
                return True                  
            strucs={}#stub for vf
            def vn(varname:str):
                token=tokens.__next__()
                if token.type!=1:
                    print(f'expected {varname} but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                    return False
                return token.string
            def fc(cnt:int,notint:bool=True,negative:bool=False):
                numa=[]
                for _ in range(cnt):
                    num=tokens.__next__()
                    if negative and num.exact_type==15:
                        sign=-1
                        num=tokens.__next__()
                    else:
                        sign=1
                    if num.exact_type!=2:
                        print('expected <number> but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                        return False
                    if notint:
                        num=float(num.string)
                    else:
                        num=int(num.string)
                    num*=sign
                    numa.append(num)
                return numa
           
                while True:
                    token=nt()
                    if token.exact_type==26:
                        return True
                    if token.exact_type==1:
                        if token.string in strucs:
                            if not strucs[token.string]():
                                print("failed parsing "+token.string)
                                return False
                            else:
                                continue
                        else:
                            print('unknown token present '+token.string)
                            return False
                    else:
                        print('expected <structName> but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                        return False

            def ml()->bool:
                nonlocal matnames
                __name=''
                while True:
                    i=tokens.__next__()
                    if i.exact_type==4 or i.exact_type==58:
                        break
                    __name+=i.string
                mtlfilename=__name
                if not mtlfilename:return False
                #nn()
                matnames=self.importmtl(os.path.split(filename)[0]+'/'+mtlfilename)
                if not matnames:
                    print('failed importing materials from',mtlfilename)
                    return False
                return True
            def vc()->bool:
                i=fc(3,True,True)
                if not i:return False
                self.points.coords.append(i)
                nn()
                return True
            def vt()->bool:
                i=fc(2,True,True)
                if not i:return False
                self.points.texcoords.append(i)
                nn()
                return True
            def nv()->bool:
                i=fc(3,True,True)
                if not i:return False
                self.points.normals.append(i)
                nn()
                return True
            def um()->bool:
                nonlocal currentmaterial
                i=vn('<materialName>')
                if not i:return False
                currentmaterial=matnames[i]
                nn()
                return True
            def fa()->bool:
                nonlocal adv_face
                o=[]
                u=[]
                i=tokens.__next__()
                for _ in range(3):
                    if i.exact_type!=2:
                        print('expected <vertexIndex>  but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                        return False
                    o.append(int(i.string))
                    u.append(int(i.string))
                    i=tokens.__next__()
                    if i.exact_type==2:
                        u.append(1)
                        u.append(1)
                        continue
                    elif i.exact_type!=17:
                        print('expected <vertexIndex> or / but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                        return False
                    i=tokens.__next__()
                    if i.exact_type==17:
                        i=tokens.__next__()
                        if i.exact_type==2:
                            u.append(1)
                            u.append(int(i.string))
                            i=tokens.__next__()
                            continue
                        else:
                            print('expected <normalIndex> but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                            return False
                    elif i.exact_type!=2:
                        print('expected <uvIndex> or / but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                        return False
                    u.append(int(i.string))
                    i=tokens.__next__()
                    if i.exact_type==17:
                        i=tokens.__next__()
                        if i.exact_type==2:
                            u.append(int(i.string))
                            i=tokens.__next__()
                            continue
                        else:
                            print('expected <normalIndex> but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                            return False
                    print('expected / but '+token.string+' present of type '+str(token.type)+" "+str(token.exact_type))
                    return False
                adv_face.append(u)
                self.faces.indices.append(o)
                self.faces.texIndice.append(currentmaterial)
                if not( i.exact_type==4 or i.exact_type==58 or i.exact_type==0):nn()
                return True
            strucs={
                'mtllib':ml,
                'g':nn,
                'v':vc,
                'vt':vt,
                'vn':nv,
                'usemtl':um,
                'f':fa,
                'o':nn,
                's':nn,
            }
            for i in tokens:
                if i.type==1:
                    if i.string in strucs:
                        if not strucs[i.string]():
                            print("failed parsing "+i.string)
                            return False
                    else:
                        print(i.type,i.exact_type,"'"+i.string+"'")
                elif i.exact_type==57:
                    nn()
                elif i.type==4 or i.type==58:
                    pass
                else:
                    print(i.type,i.exact_type,"'"+i.string+"'")
            self.points.amount=len(self.points.coords)
            self.faces.amount=len(self.faces.indices)
            if self.points.normals==[]:
                self.points.normals=np.c_[np.ones([self.points.amount,1]),np.zeros([self.points.amount,2])].astype(np.dtype('<f4'))
            if self.points.texcoords==[]:
                self.points.texcoords=np.zeros((self.points.amount,2)).astype(np.dtype('<f4'))
            self.points.coords=np.array(self.points.coords,dtype=np.dtype('<f4'))
            self.points.normals=np.array(self.points.normals,dtype=np.dtype('<f4'))
            self.points.texcoords=np.array(self.points.texcoords,dtype=np.dtype('<f4'))
            if not(self.points.amount==len(self.points.texcoords) and self.points.amount==len(self.points.normals)):
                adv_face=np.array(adv_face,dtype=np.dtype('<u4'))-1
                nc=self.points.normals
                tc=self.points.texcoords
                self.points.normals=np.zeros_like(self.points.coords)
                self.points.texcoords=np.zeros((len(self.points.coords),2),dtype=self.points.coords.dtype)
                adv_face=adv_face.reshape((-1,3))
                for i in adv_face:
                    self.points.normals[i[0]]=nc[i[2]]
                    self.points.texcoords[i[0]]=tc[i[1]]
            self.faces.indices=np.array(self.faces.indices,dtype=np.dtype('<u4'))
            self.faces.texIndice=np.array(self.faces.texIndice,dtype=np.dtype('<u4')).reshape((self.faces.amount,1))
            self.faces.indices-=1
            #self.points.coords=np.c_[self.points.coords[:,0],self.points.coords[:,2],self.points.coords[:,1]].copy()
            #self.points.normals=np.c_[self.points.normals[:,0],self.points.normals[:,2],self.points.normals[:,1]].copy()
            self.points.coords[:0]*=-1
            self.points.texcoords[:,1]=1.-self.points.texcoords[:,1]
            self.faces.indices=np.c_[self.faces.indices[:,1],self.faces.indices[:,0],self.faces.indices[:,2]].copy()
            self.points.__store=np.c_[self.points.coords,self.points.normals,self.points.texcoords].astype(np.dtype('<f4'))
            self.faces.__store=np.c_[self.faces.indices,self.faces.texIndice].astype(np.dtype('<u4'))
            if self.points.amount!=len(self.points.__store):
                print("not enough vertex coords")
                return False
            if self.matrix==[]:
                self.matrix=np.array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]],dtype=np.dtype('<f4'))
        return True
def main():
    #obj=O3d("D:\\Program Files (x86)\\OMSI 2.2.027\\Vehicles\\debug\\unrecognized\\golf2_main.o3d.bak")
    #obj=O3d(sys.argv[1])
    #filename="D:\\Program Files (x86)\\OMSI 2.2.027\\Vehicles\\A3\\model\\A3_Rollband.o3d"
    filename=sys.argv[1]
    obj=Model(filename)
    '''pat=os.path.split(filename)
    isOk=False
    while True:
        pat=os.path.split(pat[0])
        if pat[1].lower()=='model':
            isOk=True
            break
        if pat[0]<8:
            break
    if isOk:
        look=pat[0]+'\\texture\\'
        print(obj.textures.names)
        for subdir, dirs, files in os.walk(look):
            for file in files:
                print(file)
                if file in obj.textures.names:
                    print(subdir+file)
                    #os.system("copy "+' '+os.path.split(filename)+'\\') 
    else:
        print("Couldn't find texture directory")                  
        os.system("pause")
    '''
    #os.system("copy")
    #obj.extendedInfo()
    #obj.texturesInfo()
    obj.exportDirectXAsciiFrame(filename[:-4]+".x")

if __name__ == '__main__':
    main()
