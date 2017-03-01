import bottle
import os
import random

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


def generate_board(data):
    # Generate width x height board
    # All cells begin with a state of 'empty'
    board = [
        [EMPTY for _ in range(data['width'])]
        for _ in range(data['height'])
    ]

    # Populate board with food
    for food in data['food']:
        board[food[0]][food[1]] = FOOD

    for snake in data['snakes']:
        coords = snake['coords']

        # Mark our own snek as Murgatroid
        # TODO: Un-hard-code our own name
        if snake['name'] == u'murgatroid':
            for coord in coords:
                board[coord[0]][coord[1]] = MURGATROID
        else:
            # Set the coordinates of the head
            head = coords[0]
            board[head[0]][head[1]] = HEAD

            # Set the coordinates of the body
            for coord in coords[1:]:
                board[coord[0]][coord[1]] = BODY

    return board

@bottle.post('/move')
def move():
    data = bottle.request.json
    board = generate_board(data)

    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']

    return {
        'move': random.choice(directions),
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
