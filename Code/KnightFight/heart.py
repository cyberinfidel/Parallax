from controller import *
from collision import *
from graphics import *

def heartGraphics(renlayer):
	return{
			"Name": "Heart",
			"Template": MultiAnim,
			"RenderLayer": renlayer,
			"Anims":
				[
					{
						"Name": "stationary",
						"AnimType": AnimRandom,
						"State": eStates.stationary,
						"Frames":
							[
								["Graphics/Heart/Heart 7.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 6.png", 24, 30, 0.5],
							],
					},
					{
						"Name": "appear",
						"AnimType": AnimSingle,
						"State": eStates.appear,
						"Frames":
							[
								["Graphics/Heart/Heart 1.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 2.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 3.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 4.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 5.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 6.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 7.png", 24, 30, 0.5],
							],
					},
					{
						"Name": "fade",
						"AnimType": AnimSingle,
						"State": eStates.fade,
						"Frames":
							[
								["Graphics/Heart/Heart 7.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 6.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 5.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 4.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 3.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 2.png", 24, 30, 0.5],
								["Graphics/Heart/Heart 1.png", 24, 30, 0.5],
							],
					},
				]
	}

#class HeartController(Controller):
