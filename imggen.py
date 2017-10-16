import numpy as np
from cv2 import *
from collections import defaultdict
import os, random
import csv

class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret

def noise(image,prob):
	output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def path(*args):
	thisdir = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(thisdir,args)
		
def overlay(s_img,l_img,x_offset,y_offset):
	y1, y2 = y_offset, y_offset + s_img.shape[0]
	x1, x2 = x_offset, x_offset + s_img.shape[1]
	if s_image.shape[2]==4:
		alpha_s = s_img[:, :, 3] / 255.0
		alpha_l = 1.0 - alpha_s
		for c in range(0, 3):
			l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] + alpha_l * l_img[y1:y2, x1:x2, c])
	else:
		l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img

def make(n,foreground='/foregrounds',background='/backgrounds',out='/images',data='data.csv',type='png',parameters=None):
	default = {
		'reshape': True,
		'reshape_x_limits': (0.5,2)
		'reshape_y_limits': (0.5,2)
		'rotate': True,
		'flip': True,
		'max_foregrounds': 1,
		'min_foregrounds': 1,
		'brightness': True,
		'contrast': True,
		'gain_limits': (0.5,2),
		'bias_limits': (-50,50),
		'blur': True,
		'blur_both': False,
		'blur_max': 10,
		'noise': True,
		'noise_both': False,
		'prob': 0.01,
	}
	params = keydefaultdict(default,parameters)
	if not os.path.isdir(path(out)):
		os.makedirs(path(out))
	with open(path(out,data)) as csvfile:
		filewriter = csv.writer(csvfile)
		for i in range(0,n):
			int num_foregrounds = random.randint(params['min_foregrounds'],params['max_foregrounds'])
			row = [i,]
			fgs = []
			fgpaths = []
			for j in range(0,num_foregrounds):
				fgpath = random.choice(os.listdir(path(foreground)))
				fgpaths.append(fgpath)
				fgs.append(cv2.imread(fgpath),-1)
			bgpath = random.choice(os.listdir(path(foreground)))
			row.append(bgpath)
			bg = cv2.imread((bgpath),-1)
			bgwidth,bgheight = cv2.GetSize(bg)
			count = 0
			for fg in fgs: 
				fgwidth,fgheight = cv2.GetSize(fg)
				if params['reshape']:
					xsize = random.uniform(params['reshape_x_limits'][0],params['reshape_x_limits'][1])
					ysize = random.uniform(params['reshape_x_limits'][0],params['reshape_x_limits'][1])
					cv2.resize(fg,fg,fx=xsize,fy=ysize)
					fgwidth,fgheight = cv2.GetSize(fg)
				if params['rotate']:
					angle = random.randint(0,4)
					M = cv2.getRotationMatrix2D((fgheight/2,fgwidth/2),angle,1)
					fg = cv2.warpAffine(,M,(fgheight,fgwidth))
					fgwidth,fgheight = cv2.GetSize(fg)
				if params['flip']:
					if random.random<0.5:
						cv2.flip(fg,fg)
				if params['brightness']:
					gain = random.uniform(params['gain_limits'][0],params['gain_limits'][1])
					fg = fg*gain
				if params['contrast']:
					bias = random.uniform(params['bias_limits'][0],params['bias_limits'][1])
					fg = fg+bias
				if params['blur'] and not params['blur_both']:
					cv2.blur(fg,random.randint(0,params['blur_max']))
				if params['noise'] and not params['noise_both']:
					fg = noise(fg,params['prob'])
				x_offset = random.randint(0,bgwidth-fgwidth)
				y_offset = random.randint(0,bgheight-fgheight)
				overlay(fg,bg,x_offset,y_offset)
				row.append([fgpath[count],x_offset,y_offset,fgwidth,fgheight])
				count = count+1
			if params['blur_both']:
				cv2.blur(bg,random.randint(0,params['blur_max']))
			if params['noise_both']:
				bg = noise(bg,params['prob'])
			imshow('output',bg)
			imwrite(path(out,i+'.png',bg))
			filewriter.writerow(row)