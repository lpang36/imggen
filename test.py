import imggen

imggen.make(100,parameters={'rotate':False,
							'reshape_mode':'absolute',
							'reshape_x_limits':(50,200),
							'reshape_y_limits':(50,200),
							'max_foregrounds':1,
							'min_foregrounds':1,
						    'target_size':(400,300)})
