import imggen

imggen.make(100,parameters={'rotate':False,
							'reshape_mode':'absolute',
							'reshape_x_limits':(10,100),
							'reshape_y_limits':(10,100),
							'max_foregrounds':3,
							'min_foregrounds':0})
