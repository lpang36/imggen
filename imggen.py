import numpy as np
from cv2 import *
from collections import defaultdict
import os, random, csv
from tqdm import tqdm

#custom dictionary class
class keydefaultdict(defaultdict):
	def __missing__(self, key):
		if self.default_factory is None:
			raise KeyError( key )
		else:
			ret = self[key] = self.default_factory(key)
			return ret

#salt and pepper noise
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

#return local path
def path(*args):
	thisdir = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(thisdir,*args)
		
#overlay one image on another
def overlay(s_img,l_img,y_offset,x_offset):
	y1, y2 = y_offset, y_offset + s_img.shape[0]
	x1, x2 = x_offset, x_offset + s_img.shape[1]
	#account for alpha channel
	if s_img.shape[2]==4:
		alpha_s = s_img[:, :, 3] / 255.0
		alpha_l = 1.0 - alpha_s
		for c in range(0, 3):
			l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] + alpha_l * l_img[y1:y2, x1:x2, c])
	else:
		l_img[y_offset:(y_offset+s_img.shape[0]), x_offset:(x_offset+s_img.shape[1])] = s_img

#generate images
def make(n,foreground='foreground',background='background',out='images',data='data.csv',filetype='png',parameters={}):
	#default parameters
	def default(key): 
		defaults = {
			'reshape': True,
			'maintain_aspect': False,
			'reshape_mode': 'foreground',
			'reshape_x_limits': (0.25,4),
			'reshape_y_limits': (0.25,4),
			'rotate': True,
			'rotate_limits': (0,360),
			'rotate_increment': 90,
			'flip': True,
			'max_foregrounds': 1,
			'min_foregrounds': 1,
			'brightness': True,
			'contrast': True,
			'gain_limits': (0.75,1.25),
			'bias_limits': (-10,10),
			'blur': True,
			'blur_both': False,
			'blur_max': 0.05,
			'noise': True,
			'noise_both': False,
			'prob': 0.1,
			'target_size': None,
		}
		return defaults[key]
	params = keydefaultdict(default,parameters)
	if not os.path.isdir(path(out)):
		print('Creating output folder at '+path(out)+'.')
		os.makedirs(path(out))
	if not os.path.isfile(path(out,data)):
		print('Creating output csv file at '+path(out,data)+'.')
		os.open(path(out,data),os.O_CREAT)
	print('Generating images...')
	with open(path(out,data),'w') as csvfile:
		filewriter = csv.writer(csvfile)
		#pretty print loop
		for i in tqdm(range(0,n)):
			num_foregrounds = random.randint(params['min_foregrounds'],params['max_foregrounds'])
			row = [i,]
			fgs = []
			fgpaths = []
			#randomly select foregrounds, backgrounds
			for j in range(0,num_foregrounds):
				fgpath = random.choice(os.listdir(path(foreground)))
				fgpaths.append(fgpath)
				fgs.append(cv2.imread(path(foreground,fgpath),-1))
			bgpath = random.choice(os.listdir(path(background)))
			row.append(bgpath)
			bg = cv2.imread(path(background,bgpath),-1)
			bgwidth,bgheight,_ = np.shape(bg)
			count = 0
			#alter image
			for fg in fgs: 
				fgwidth,fgheight,_ = np.shape(fg)
				if params['reshape']:
					xsize = random.uniform(params['reshape_x_limits'][0],params['reshape_x_limits'][1])
					if params['maintain_aspect']:
						ysize = xsize
					else:
						ysize = random.uniform(params['reshape_x_limits'][0],params['reshape_x_limits'][1])
					if params['reshape_mode'] is 'foreground':
						fg = cv2.resize(fg,(0,0),fg,xsize,ysize)
					elif params['reshape_mode'] is 'background':
						fg = cv2.resize(fg,(int(xsize*bgwidth),int(ysize*bgheight)),fg)
					elif params['reshape_mode'] is 'absolute':
						fg = cv2.resize(fg,(int(xsize),int(ysize)),fg)
					fgwidth,fgheight,_ = np.shape(fg)
				if params['rotate']:
					angle = random.randint(params['rotate_limits'][0],params['rotate_limits'][1])/params['rotate_increment']*params['rotate_increment']
					M = cv2.getRotationMatrix2D((fgheight/2,fgwidth/2),angle,1)
					fg = cv2.warpAffine(fg,M,(fgheight,fgwidth))
					fgwidth,fgheight,_ = np.shape(fg)
				if params['flip']:
					if random.random<0.5:
						cv2.flip(fg,fg)
				if params['brightness']:
					gain = random.uniform(params['gain_limits'][0],params['gain_limits'][1])
					fg[:,:,:3] = fg[:,:,:3]*gain
				if params['contrast']:
					bias = random.uniform(params['bias_limits'][0],params['bias_limits'][1])
					fg[:,:,:3] = fg[:,:,:3]+bias
				if params['blur'] and not params['blur_both']:
					blur_lvl = random.randint(0,int(params['blur_max']*min(fgwidth,fgheight)[0])+1)
					if blur_lvl>0:
						fg = cv2.blur(fg,(blur_lvl,blur_lvl))
				if params['noise'] and not params['noise_both']:
					noise_prob = random.uniform(0,params['prob'])
					fg = noise(fg,noise_prob)
				fitsize = min((bgwidth+0.0)/fgwidth,(bgheight+0.0)/fgheight)
				if fitsize[0]<1:
					fg = cv2.resize(fg,(0,0),fg,fitsize[0],fitsize[0])
				fgwidth,fgheight,_ = np.shape(fg)
				x_offset = random.randint(0,bgwidth-fgwidth)
				y_offset = random.randint(0,bgheight-fgheight)
				#compose image
				overlay(fg,bg,x_offset,y_offset)
				row.append([fgpaths[count],x_offset,y_offset,fgwidth,fgheight])
				count = count+1
			if params['blur_both']:
				blur_lvl = random.randint(0,int(params['blur_max']*min(bgwidth,bgheight)[0])+1)
				if blur_lvl>0:
					cv2.blur(bg,(blur_lvl,blur_lvl))
			if params['noise_both']:
				noise_prob = random.uniform(0,params['prob'])
				bg = noise(bg,noise_prob)
			#write to output
			if params['target_size'] is not None:
				for cell in row[2:]:
					cell[1] = int(cell[1]*params['target_size'][0]/(bgwidth+0.0))
					cell[2] = int(cell[2]*params['target_size'][1]/(bgheight+0.0))
					cell[3] = int(cell[3]*params['target_size'][0]/(bgwidth+0.0))
					cell[4] = int(cell[4]*params['target_size'][1]/(bgheight+0.0))
				bg = cv2.resize(bg,params['target_size'],bg)
			imwrite(path(out,str(i)+'.'+filetype),bg)
			filewriter.writerow(row)
	print('Done.')