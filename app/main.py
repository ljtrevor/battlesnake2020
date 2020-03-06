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

taunt_list = """
Well, you can tell by the way I use my walk
I'm a woman's man: no time to talk
Music loud and women warm, I've been kicked around
Since I was born
And now it's all right, it's okay
And you may look the other way
We can try to understand
The New York Times' effect on man
Whether you're a brother or whether you're a mother
You're stayin' alive, stayin' alive
Feel the city breakin' and everybody shakin'
And we're stayin' alive, stayin' alive
Ah, ha, ha, ha, stayin' alive, stayin' alive
Ah, ha, ha, ha, stayin' alive
Well now, I get low and I get high
And if I can't get either, I really try
Got the wings of heaven on my shoes
I'm a dancin' man and I just can't lose
You know it's all right, it's okay
I'll live to see another day
We can try to understand
The New York Times' effect on man
Whether you're a brother or whether you're a mother
You're stayin' alive, stayin' alive
Feel the city breakin' and everybody shakin'
And we're stayin' alive, stayin' alive
Ah, ha, ha, ha, stayin' alive, stayin' alive
Ah, ha, ha, ha, stayin' alive
Life goin' nowhere, somebody help me
Somebody help me, yeah
Life goin' nowhere, somebody help me
Somebody help me, yeah, I'm stayin' alive
Well, you can tell by the way I use my walk
I'm a woman's man: no time to talk
Music loud and women warm
I've been kicked around since I was born
And now it's all right, it's okay
And you may look the other way
We can try to understand
The New York Times' effect on man
Whether you're a brother or whether you're a mother
You're stayin' alive, stayin' alive
Feel the city breakin' and everybody shakin'
And we're stayin' alive, stayin' alive
Ah, ha, ha, ha, stayin' alive, stayin' alive
Ah, ha, ha, ha, stayin' alive
Life goin' nowhere, somebody help me
Somebody help me, yeah
Life goin' nowhere, somebody help me, yeah
I'm stayin' alive
Life goin' nowhere, somebody help me
Somebody help me, yeah
Life goin' nowhere, somebody help me, yeah
I'm stayin' alive
Life goin' nowhere, somebody help me
Somebody help me, yeah
Life goin' nowhere, somebody help me, yeah
I'm stayin' alive
Life goin' nowhere, somebody help me
Somebody help me, yeah
Life goin' nowhere, somebody help me, yeah
I'm stayin' alive
""".split('\n')


counter = 0


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    global counter
    counter = 0

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
        'color': '#e52a01',
        'shout': 'Well, you can tell by the way I use my walk',
        'head_url': head_url,
    }


def get_taunt():
    global counter
    counter += 1
    return taunt_list[(counter/16 % len(taunt_list))]


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
            'shout': 'You will always remember this as the day you almost caught Captain Jack Sparrow!'
        })

    print directions_map

    edge_direction = murgatroid_controller.move_edge()
    print edge_direction

    taunt = get_taunt()

    food_directions = murgatroid_controller.get_food_directions(directions_map)
    if food_directions:
        return json.dumps({
            'move': murgatroid_controller.get_safest_direction(food_directions),
            'shout': taunt,
        })
    else:
        if edge_direction in directions_map:
            direction = edge_direction
        else:
            direction = murgatroid_controller.get_safest_direction(directions_map)

        return json.dumps({
            'move': direction,
            'shout': taunt,
        })


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
