import bottle
import json
import os
import random
import sys

from model.point import Point
from model.snake import Snake
from model.board import Board
from model.board import FOOD
from controller.murgatroid_controller import MurgatroidController

EMPTY = u'empty'
FOOD = u'food'
BODY = u'body'
HEAD = u'head'
MURGATROID = u'murgatroid'


UP = u'up'
RIGHT = u'right'
DOWN = u'down'
LEFT = u'left'


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'murgatroid'
    }

@bottle.post('/move')
def move():
    data = bottle.request.json
    board = Board.from_json(data)
    murgatroid_controller = MurgatroidController(board)

    directions_map = murgatroid_controller.get_possible_directions()
    if not directions_map:
        # Commit suicide honorably so as not to give any victories to
        # the other inferior snakes!
        return json.dumps({
            'move': murgatroid_controller.seppuku(),
            'taunt': 'You will always remember this as the day you almost caught Captain Jack Sparrow!'
        })

    edge_direction = murgatroid_controller.move_edge()

    # WIP
    food_directions = [
        direction
        for direction, data in directions_map.iteritems()
        if data['state'] == FOOD
    ]

    if food_directions:
        return json.dumps({
            'move': random.choice(food_directions),
            'taunt': 'Sssssssssssssaucy'
        })
    else:
        return json.dumps({
            'move': edge_direction if edge_direction in directions_map else random.choice(directions_map.keys()),
            'taunt': 'MURGATROIIIIIID'
        })


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
