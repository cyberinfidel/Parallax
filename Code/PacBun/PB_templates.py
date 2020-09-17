import px_graphics
import px_message_box
import px_director

import PacBun
import title
import high_score
import new_high_score
import bunny
import fox
import tile

graphics = {
	'bowie': {
		"Name": "Bunny Animations",
		"Template": px_graphics.MultiAnim,
		# "RenderLayer": self.renlayer,
		"Anims": [
			{
				"Name": "Bunny Stands",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.idle],
				"Frames":
					[
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 3.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/White/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/White/Idle 2.png", 8, 11, 0, 0.2],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runDown],
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
				"States": [PacBun.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/White/RunUp 2.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/White/RunUp 3.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/White/RunUp 4.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/White/RunUp 1.png", 8, 9, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/White/RunLeft 1.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 2.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 3.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/White/RunLeft 4.png", 8, 10, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/White/RunRight 1.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/White/RunRight 2.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/White/RunRight 3.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/White/RunRight 4.png", 8, 10, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Enters Hole Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleRight],
				"Frames": [
					["Graphics/Bunny/White/Hole 1.png", 5, 4, 0, 0.1],
					["Graphics/Bunny/White/Hole 4.png", 1, 2, 0, 0.1],
				],
			},
			{
				"Name": "Bunny Enters Hole Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleLeft],
				"Frames": [
					["Graphics/Bunny/White/Hole 1.png", 5, 4, 0, 0.1],
					["Graphics/Bunny/White/Hole 4.png", 1, 2, 0, 0.1],
				]
			},
			{
				"Name": "Bunny Enters Hole Up",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleUp],
				"Frames":
					[
						["Graphics/Bunny/White/Hole 1.png", 5, 4, 0, 0.1],
						["Graphics/Bunny/White/Hole 4.png", 1, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Enters Hole Down",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleDown],
				"Frames":
					[
						["Graphics/Bunny/White/Hole 2.png", 5, 4, 0, 0.1],
						["Graphics/Bunny/White/Hole 4.png", 1, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleRight],
				"Frames":
					[
						["Graphics/Bunny/White/Hole 3.png", 6, 4, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleLeft],
				"Frames":
					[
						["Graphics/Bunny/White/Hole 3.png", 2, 4, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Up",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleUp],
				"Frames":
					[
						["Graphics/Bunny/White/Hole 3.png", 4, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Down",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleDown],
				"Frames":
					[
						["Graphics/Bunny/White/Hole 3.png", 4, 6, 0, 0.1],
					],
			},

		]

	},	# end of bowie
	'pacbun': {
		"Name": "Bunny Animations",
		"Template": px_graphics.MultiAnim,
		# "RenderLayer": self.renlayer,
		"Anims": [
			{
				"Name": "Bunny Stands",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.idle],
				"Frames":
					[
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 3.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Yellow/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Yellow/Idle 1.png", 8, 11, 0, 0.8],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/Yellow/RunDown 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunDown 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunDown 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Yellow/RunDown 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/Yellow/RunUp 2.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Yellow/RunUp 3.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Yellow/RunUp 4.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Yellow/RunUp 1.png", 8, 9, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/Yellow/RunLeft 1.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Yellow/RunLeft 2.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Yellow/RunLeft 3.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Yellow/RunLeft 4.png", 8, 10, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/Yellow/RunRight 1.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Yellow/RunRight 2.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Yellow/RunRight 3.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Yellow/RunRight 4.png", 8, 10, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Enters Hole Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleRight],
				"Frames": [
					["Graphics/Bunny/Yellow/Hole 1.png", 5, 4, 0, 0.1],
					["Graphics/Bunny/Yellow/Hole 4.png", 1, 2, 0, 0.1],
				],
			},
			{
				"Name": "Bunny Enters Hole Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleLeft],
				"Frames": [
					["Graphics/Bunny/Yellow/Hole 1.png", 5, 4, 0, 0.1],
					["Graphics/Bunny/Yellow/Hole 4.png", 1, 2, 0, 0.1],
				]
			},
			{
				"Name": "Bunny Enters Hole Up",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleUp],
				"Frames":
					[
						["Graphics/Bunny/Yellow/Hole 1.png", 5, 4, 0, 0.1],
						["Graphics/Bunny/Yellow/Hole 4.png", 1, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Enters Hole Down",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleDown],
				"Frames":
					[
						["Graphics/Bunny/Yellow/Hole 2.png", 5, 4, 0, 0.1],
						["Graphics/Bunny/Yellow/Hole 4.png", 1, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleRight],
				"Frames":
					[
						["Graphics/Bunny/Yellow/Hole 3.png", 6, 4, 0, 0.5],
					],
			},
			{
				"Name": "Bunny Leaves Hole Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleLeft],
				"Frames":
					[
						["Graphics/Bunny/Yellow/Hole 3.png", 2, 4, 0, 0.5],
					],
			},
			{
				"Name": "Bunny Leaves Hole Up",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleUp],
				"Frames":
					[
						["Graphics/Bunny/Yellow/Hole 3.png", 4, 2, 0, 0.5],
					],
			},
			{
				"Name": "Bunny Leaves Hole Down",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleDown],
				"Frames":
					[
						["Graphics/Bunny/Yellow/Hole 3.png", 4, 6, 0, 0.5],
					],
			},

		]

	},	# end of pacbun
	'pinkie': {
		"Name": "Bunny Animations",
		"Template": px_graphics.MultiAnim,
		# "RenderLayer": self.renlayer,
		"Anims": [
			{
				"Name": "Bunny Stands",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.idle],
				"Frames":
					[
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 3.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Pink/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Pink/Idle 2.png", 8, 11, 0, 0.2],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/Pink/RunDown 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunDown 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunDown 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Pink/RunDown 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/Pink/RunUp 2.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Pink/RunUp 3.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Pink/RunUp 4.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Pink/RunUp 1.png", 8, 9, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/Pink/RunLeft 1.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Pink/RunLeft 2.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Pink/RunLeft 3.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Pink/RunLeft 4.png", 8, 10, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/Pink/RunRight 1.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Pink/RunRight 2.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Pink/RunRight 3.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Pink/RunRight 4.png", 8, 10, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Enters Hole Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleRight],
				"Frames": [
					["Graphics/Bunny/Pink/Hole 1.png", 5, 4, 0, 0.1],
					["Graphics/Bunny/Pink/Hole 5.png", 1, 2, 0, 0.1],
				],
			},
			{
				"Name": "Bunny Enters Hole Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleLeft],
				"Frames": [
					["Graphics/Bunny/Pink/Hole 1.png", 5, 4, 0, 0.1],
					["Graphics/Bunny/Pink/Hole 5.png", 1, 2, 0, 0.1],
				]
			},
			{
				"Name": "Bunny Enters Hole Up",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleUp],
				"Frames":
					[
						["Graphics/Bunny/Pink/Hole 1.png", 5, 4, 0, 0.1],
						["Graphics/Bunny/Pink/Hole 5.png", 1, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Enters Hole Down",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleDown],
				"Frames":
					[
						["Graphics/Bunny/Pink/Hole 2.png", 5, 4, 0, 0.1],
						["Graphics/Bunny/Pink/Hole 5.png", 1, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleRight],
				"Frames":
					[
						["Graphics/Bunny/Pink/Hole 3.png", 6, 4, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleLeft],
				"Frames":
					[
						["Graphics/Bunny/Pink/Hole 3.png", 2, 4, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Up",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleUp],
				"Frames":
					[
						["Graphics/Bunny/Pink/Hole 3.png", 4, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Down",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleDown],
				"Frames":
					[
						["Graphics/Bunny/Pink/Hole 3.png", 4, 6, 0, 0.1],
					],
			},

		]

	},	# end of pinkie
	'blue': {
		"Name": "Bunny Animations",
		"Template": px_graphics.MultiAnim,
		# "RenderLayer": self.renlayer,
		"Anims": [
			{
				"Name": "Bunny Stands",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.idle],
				"Frames":
					[
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 1.png", 8, 11, 0, 0.8],
						["Graphics/Bunny/Blue/Idle 2.png", 8, 11, 0, 0.2],
						["Graphics/Bunny/Blue/Idle 3.png", 8, 11, 0, 0.2],
					]
			},
			{
				"Name": "Bunny Runs Down",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runDown],
				"Frames":
					[
						["Graphics/Bunny/Blue/RunDown 2.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunDown 3.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunDown 4.png", 8, 11, 0, 0.05],
						["Graphics/Bunny/Blue/RunDown 1.png", 8, 11, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runUp],
				"Frames":
					[
						["Graphics/Bunny/Blue/RunUp 2.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Blue/RunUp 3.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Blue/RunUp 4.png", 8, 9, 0, 0.05],
						["Graphics/Bunny/Blue/RunUp 1.png", 8, 9, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runLeft],
				"Frames":
					[
						["Graphics/Bunny/Blue/RunLeft 1.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Blue/RunLeft 2.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Blue/RunLeft 3.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Blue/RunLeft 4.png", 8, 10, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runRight],
				"Frames":
					[
						["Graphics/Bunny/Blue/RunRight 1.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Blue/RunRight 2.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Blue/RunRight 3.png", 8, 10, 0, 0.05],
						["Graphics/Bunny/Blue/RunRight 4.png", 8, 10, 0, 0.075],
					],
			},
			{
				"Name": "Bunny Enters Hole Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleRight],
				"Frames": [
					["Graphics/Bunny/Blue/Hole 1.png", 5, 4, 0, 0.1],
					["Graphics/Bunny/Blue/Hole 5.png", 1, 2, 0, 0.1],
				],
			},
			{
				"Name": "Bunny Enters Hole Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleLeft],
				"Frames": [
					["Graphics/Bunny/Blue/Hole 1.png", 5, 4, 0, 0.1],
					["Graphics/Bunny/Blue/Hole 5.png", 1, 2, 0, 0.1],
				]
			},
			{
				"Name": "Bunny Enters Hole Up",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleUp],
				"Frames":
					[
						["Graphics/Bunny/Blue/Hole 1.png", 5, 4, 0, 0.1],
						["Graphics/Bunny/Blue/Hole 5.png", 1, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Enters Hole Down",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.enterHoleDown],
				"Frames":
					[
						["Graphics/Bunny/Blue/Hole 2.png", 5, 4, 0, 0.1],
						["Graphics/Bunny/Blue/Hole 5.png", 1, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Right",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleRight],
				"Frames":
					[
						["Graphics/Bunny/Blue/Hole 3.png", 7, 4, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Left",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleLeft],
				"Frames":
					[
						["Graphics/Bunny/Blue/Hole 3.png", 3, 4, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Up",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleUp],
				"Frames":
					[
						["Graphics/Bunny/Blue/Hole 3.png", 5, 2, 0, 0.1],
					],
			},
			{
				"Name": "Bunny Leaves Hole Down",
				"AnimType": px_graphics.AnimNoLoop,
				"States": [PacBun.eStates.leavesHoleDown],
				"Frames":
					[
						["Graphics/Bunny/Blue/Hole 3.png", 5, 6, 0, 0.1],
					],
			},

		]

	},	# end of blue
	'fox': {
		"Name": "Fox Animations",
		"Template": px_graphics.MultiAnim,
		# "RenderLayer": self.renlayer,
		"Anims": [
			{
				"Name": "Fox Stands",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.idle],
				"Frames":
					[
						["Graphics/Fox/Pant/Pant_000.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_001.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_002.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_003.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_004.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_005.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_006.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_007.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_008.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_009.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_010.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_011.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_012.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_013.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_014.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_015.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_016.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_017.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_018.png", 11, 15, 0, 0.02],
						["Graphics/Fox/Pant/Pant_019.png", 11, 15, 0, 0.02],
					]
			},
			{
				"Name": "Fox Cleans L",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.cleanLeft],
				"Frames":
					[
						["Graphics/Fox/CleanL/CleanL_000.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_001.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_002.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_003.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_004.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_014.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_015.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_016.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_017.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_018.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanL/CleanL_019.png", 15, 15, 0, 0.02],
					]
			},
			{
				"Name": "Fox Cleans L",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.cleanRight],
				"Frames":
					[
						["Graphics/Fox/CleanR/CleanR_000.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_001.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_002.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_003.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_004.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_005.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_006.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_007.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_008.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_009.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_010.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_011.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_012.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_013.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_014.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_015.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_016.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_017.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_018.png", 15, 15, 0, 0.02],
						["Graphics/Fox/CleanR/CleanR_019.png", 15, 15, 0, 0.02],
					]
			},
			{
				"Name": "Fox Runs Down",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runDown],
				"Frames":
					[
						["Graphics/Fox/RunD_000.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_001.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_002.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_003.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_004.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_005.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_006.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_007.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_008.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_009.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_010.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_011.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_012.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_013.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_014.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_015.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_016.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_017.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_018.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunD_019.png", 6, 20, 0, 0.02],
					],
			},
			{
				"Name": "Bunny Runs Up",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runUp],
				"Frames":
					[
						["Graphics/Fox/RunU_000.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_001.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_002.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_003.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_004.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_005.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_006.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_007.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_008.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_009.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_010.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_011.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_012.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_013.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_014.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_015.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_016.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_017.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_018.png", 6, 20, 0, 0.02],
						["Graphics/Fox/RunU_019.png", 6, 20, 0, 0.02],
					],
			},
			{
				"Name": "Bunny Runs Left",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runLeft],
				"Frames":
					[
						["Graphics/Fox/Left/Run_000.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_001.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_002.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_003.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_004.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_005.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_006.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_007.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_008.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_009.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_010.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_011.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_012.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_013.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_014.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_015.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_016.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_017.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_018.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Left/Run_019.png", 20, 11, 0, 0.02],
					],
			},
			{
				"Name": "Bunny Runs Right",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.runRight],
				"Frames":
					[
						["Graphics/Fox/Run_000.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_001.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_002.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_003.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_004.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_005.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_006.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_007.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_008.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_009.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_010.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_011.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_012.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_013.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_014.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_015.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_016.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_017.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_018.png", 20, 11, 0, 0.02],
						["Graphics/Fox/Run_019.png", 20, 11, 0, 0.02],
					],
			},
			{
				"Name": "PacBun Caught",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.caughtPacBun],
				"Frames":
					[
						["Graphics/Fox/FoxCaught 1.png", 11, 15, 0, 0.02],
					],
			},
			{
				"Name": "Pinkie Caught",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.caughtPinkie],
				"Frames":
					[
						["Graphics/Fox/FoxCaught 3.png", 11, 15, 0, 0.02],
					],
			},
			{
				"Name": "Blue Caught",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.caughtBlue],
				"Frames":
					[
						["Graphics/Fox/FoxCaught 2.png", 11, 15, 0, 0.02],
					],
			},
			{
				"Name": "Bowie Caught",
				"AnimType": px_graphics.AnimLoop,
				"States": [PacBun.eStates.caughtBowie],
				"Frames":
					[
						["Graphics/Fox/FoxCaught 4.png", 11, 15, 0, 0.02],
					],
			},
		]

	},	# end of fox
	'tile': {
		"Name": "Path Graphics",
		"Template": px_graphics.MultiAnim,
		# "RenderLayer": self.renlayer,
		"Anims": [
			{
				"Name": "Path without Poo",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.path],
				"Frames":
					[["Graphics/Path/Path.png", 8, 8, 0, 0.8]],
			},
			{
				"Name": "Path with Poo",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.poo],
				"Frames":
					[["Graphics/Path/Path Poo.png", 8, 8, 0, 0.8]],
			},
			{
				"Name": "Path with Hole",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.hole],
				"Frames":
					[["Graphics/Path/Path Hole.png", 8, 8, 0, 0.8]],
			},
			{
				"Name": "Hedge",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.hedge],
				"Frames":
					[
						["Graphics/Hedge/Hedge 1.png", 10, 12, -1, 0.8],
						["Graphics/Hedge/Hedge 2.png", 10, 12, -1, 0.8],
						["Graphics/Hedge/Hedge 3.png", 10, 12, -1, 0.8],
					],
			},
			{
				"Name": "Void",
				"AnimType": px_graphics.AnimSingle,
				"States": [tile.eTileStates.void],
				"Frames":
					[["Graphics/Tunnel/Tunnel 01.png", 8, 8, 0, 0.8]],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up_down_left_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 14.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up_down],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 04.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_left_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 05.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 06.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up_left],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 07.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_down_left],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 08.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_down_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 09.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up_left_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 10.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up_down_left],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 11.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_down_left_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 12.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up_down_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 13.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up_down_left_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 02.png", 8, 8, 0, 0.8],
						["Graphics/Tunnel/Tunnel 03.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_up],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 15.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_left],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 16.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_down],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 17.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Tunnel",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.tunnel_right],
				"Frames":
					[
						["Graphics/Tunnel/Tunnel 18.png", 8, 8, 0, 0.8],
					],
			},
			{
				"Name": "Path with Cutscene Hole",
				"AnimType": px_graphics.AnimRandomStatic,
				"States": [tile.eTileStates.cutscene_hole],
				"Frames":
					[["Graphics/Path/Path Hole.png", 8, 8, 0, 0.8]],
			},

		]

	},	# end of tile
	'title': {
		"Name": "Title Picture",
		"Template": px_graphics.SingleImage,
		# "RenderLayer": renlayer,
		"Image":
			["Graphics/Title/Title.png", 108, 21, 0],
	},
	'escape': {
		"Name": "Escape Overlay",
		"Template": px_graphics.SingleAnim,
		"Anims": [
			{
				"Name": "Path with Cutscene Hole",
				"AnimType": px_graphics.AnimLoop,
				"Frames": [
					["Graphics/Title/Escape.png", 8, 8, 0, 0.8],
					["Graphics/Title/Escape2.png", 8, 8, 0, 0.8],
				],
			},
		]
	},
	'high_score': {
		"Name": "Scoreboard",
		"Template": high_score.ScoreTable,
	},
	'new_high_score': {
		"Name": "Scoreboard",
		"Template": new_high_score.NewScore,
	},
	'message': {
		"Name": "Message",
		"Template": px_message_box.MessageBox,
	},
}

components = {
	"controllers": {
		'bunny_controller': bunny.makeController,
		'fox_controller': fox.makeController,
		'tile_controller': tile.makeController,
		'title_controller': title.makeController,
		'high_score_controller': high_score.makeController,
		'new_high_score_controller': new_high_score.makeController,
		'message_controller': px_message_box.makeController,
		'director_controller': px_director.makeController,
	},
	"colliders": {
		'bunny_collider': bunny.makeCollider,
		'fox_collider': fox.makeCollider,
	},
	"graphics": {
		'pacbun_graphics': graphics['pacbun'],
		'pinkie_graphics': graphics['pinkie'],
		'bowie_graphics': graphics['bowie'],
		'blue_graphics': graphics['blue'],
		'fox_graphics': graphics['fox'],
		'tile_graphics': graphics['tile'],
		'title_graphics': graphics['title'],
		'escape_graphics': graphics['escape'],
		'high_score_graphics': graphics['high_score'],
		'new_high_score_graphics': graphics['new_high_score'],
		'message_graphics': graphics['message'],
	}
}

# templates that are available in the whole game
game_templates = {
	'pacbun': {
		'controller': components['controllers']['bunny_controller'],
		'collider': components['colliders']['bunny_collider'],
		'graphics': { 'component': components['graphics']['pacbun_graphics'], 'render layer': 'game'}
	},
	'pinkie': {
		'controller': components['controllers']['bunny_controller'],
		'collider': components['colliders']['bunny_collider'],
		'graphics': { 'component': components['graphics']['pinkie_graphics'], 'render layer': 'game'}
	},
	'blue': {
		'controller': components['controllers']['bunny_controller'],
		'collider': components['colliders']['bunny_collider'],
		'graphics': { 'component': components['graphics']['blue_graphics'], 'render layer': 'game'}
	},
	'bowie': {
		'controller': components['controllers']['bunny_controller'],
		'collider': components['colliders']['bunny_collider'],
		'graphics': { 'component': components['graphics']['bowie_graphics'], 'render layer': 'game'}
	},
	'fox': {
		'controller': components['controllers']['fox_controller'],
		'collider': components['colliders']['fox_collider'],
		'graphics': { 'component': components['graphics']['fox_graphics'], 'render layer': 'game'}
	},
	'tile': {
		'controller': components['controllers']['tile_controller'],
		'graphics': { 'component': components['graphics']['tile_graphics'], 'render layer': 'game'}
	},
	'director': {
		'controller': components['controllers']['director_controller'],
	},
	'high_scores':{
		'controller': components['controllers']['high_score_controller'],
		'graphics': { 'component': components['graphics']['high_score_graphics'], 'render layer': 'overlay'},
	},
	'title':{
		'graphics': { 'component': components['graphics']['title_graphics'], 'render layer': 'overlay'},
	},
	'new_high_score':{
		'controller': components['controllers']['new_high_score_controller'],
		'graphics': { 'component': components['graphics']['new_high_score_graphics'], 'render layer': 'overlay'},
	},
	'message':{
		'controller': components['controllers']['message_controller'],
		'graphics': { 'component': components['graphics']['message_graphics'], 'render layer': 'overlay'},
	},
	'pacbun bye': {
		'graphics': {'component': components['graphics']['pacbun_graphics'], 'render layer': 'game'},
	},
	'pinkie bye': {
		'graphics': {'component': components['graphics']['pinkie_graphics'], 'render layer': 'game'},
	},
	'blue bye': {
		'graphics': {'component': components['graphics']['blue_graphics'], 'render layer': 'game'},
	},
	'bowie bye': {
		'graphics': {'component': components['graphics']['bowie_graphics'], 'render layer': 'game'},
	},
}