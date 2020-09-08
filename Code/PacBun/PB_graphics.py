import px_graphics
import px_entity

bowie_graphics = {
		"Name": "Bunny Animations",
		"Template": px_graphics.MultiAnim,
		# "RenderLayer": self.renlayer,
		"Anims": [
			{
				"Name": "Bunny Stands",
				"AnimType": px_graphics.AnimLoop,
				"States": [px_entity.eStates.stationary],
				"Frames":
					[
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 3.png", 8, 11, 0, 0.2],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": px_graphics.AnimLoop,
				"States": [px_entity.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/White/RunDown 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunDown 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunDown 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunDown 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": px_graphics.AnimLoop,
				"States": [px_entity.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/White/RunUp 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunUp 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunUp 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/White/RunUp 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": px_graphics.AnimLoop,
				"States": [px_entity.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/White/RunLeft 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 4.png", 8, 14, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": px_graphics.AnimLoop,
				"States": [px_entity.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/White/RunRight 1.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunRight 2.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunRight 3.png", 8, 14, 0, 0.05],
						["Graphics/Bunny/White/RunRight 4.png", 8, 14, 0, 0.075],
					],
			},

		]

	}	# end of bowie

