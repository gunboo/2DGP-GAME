# game_world.py
objects = [[], [], [], []]  # 0: 배경, 1: 캐릭터, 2: 보스

def add_object(obj, layer):
    objects[layer].append(obj)

def remove_object(obj):
    for layer in objects:
        if obj in layer:
            layer.remove(obj)
            del obj
            return

def clear():
    global objects
    for layer in objects:
        layer.clear()
    objects = [[], [], [], []]

def update():
    for layer in objects:
        for obj in layer:
            obj.update()

def render():
    for layer in objects:
        for obj in layer:
            obj.draw()

def all_objects():
    for layer in objects:
        for obj in layer:
            yield obj
