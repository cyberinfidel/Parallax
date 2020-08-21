import graphics
import entity

bowie_graphics = {
		"Name": "Bunny Animations",
		"Template": graphics.MultiAnim,
		# "RenderLayer": self.renlayer,
		"Anims": [
			{
				"Name": "Bunny Stands",
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.stationary],
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
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runDown],
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
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runUp],
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
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runLeft],
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
				"AnimType": graphics.AnimLoop,
				"States": [entity.eStates.runRight],
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
