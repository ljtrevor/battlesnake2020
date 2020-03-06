import bottle
import json
import os
import random
import sys

from bottle import HTTPResponse

from model.point import Point
from model.snake import Snake
from model.board import Board
from model.board import FOOD
from controller.murgatroid_controller import MurgatroidController


SHOUT = "doosting hot moms since '97"

@bottle.route("/")
def index():
    return SHOUT

@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)

@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#ecb7bf", "headType": "bwc-earmuffs", "tailType": "small-rattle"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post('/move')
def move():
    data = bottle.request.json
    board = Board.from_json(data)
    murgatroid_controller = MurgatroidController(board)

    directions_map = murgatroid_controller.get_possible_directions()

    edge_direction = murgatroid_controller.move_edge()

    food_directions = murgatroid_controller.get_food_directions(directions_map)
    if food_directions:
        return json.dumps({
            'move': murgatroid_controller.get_safest_direction(food_directions),
            'shout': SHOUT,
        })
    else:
        if edge_direction in directions_map:
            direction = edge_direction
        else:
            direction = murgatroid_controller.get_safest_direction(directions_map)

        return json.dumps({
            'move': direction,
            'shout': SHOUT,
        })

@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
