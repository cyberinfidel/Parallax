import px_graphics
import px_message_box
import px_director

import PacBun
from PB_graphics import graphics
import title
import high_score
import new_high_score
import bunny
import fox
import tile


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