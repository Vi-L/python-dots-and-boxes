import sys, pygame
from enum import Enum
pygame.init()

Owner = Enum('Owner', 'none red blue')

class Game:
    def __init__(self):
        edges = [Edge() for _ in range(12)]
        boxes = [Box() for _ in range(4)]

        boxes[0].edges = [edges[0], edges[2], edges[3], edges[5]]
        boxes[1].edges = [edges[1], edges[3], edges[4], edges[6]]
        boxes[2].edges = [edges[5], edges[7], edges[8], edges[10]]
        boxes[3].edges = [edges[6], edges[8], edges[9], edges[11]]

        edges[0].boxes = [boxes[0]]
        edges[1].boxes = [boxes[1]]
        edges[2].boxes = [boxes[0]]
        edges[3].boxes = [boxes[0], boxes[1]]
        edges[4].boxes = [boxes[1]]
        edges[5].boxes = [boxes[0], boxes[2]]
        edges[6].boxes = [boxes[1], boxes[3]]
        edges[7].boxes = [boxes[2]]
        edges[8].boxes = [boxes[2], boxes[3]]
        edges[9].boxes = [boxes[3]]
        edges[10].boxes = [boxes[2]]
        edges[11].boxes = [boxes[3]]

        self.edges = edges
        self.boxes = boxes
        self.player = Owner.red
        self.ply = 0

    def make_move(self, edge_index):
        edge = self.edges[edge_index] #TODO: check validity? or refactor
        if edge.owner != Owner.none:
            return False
        edge.owner = self.player
        any_claimed = False
        for box in edge.boxes:
            if self.try_claim_box(box):
                any_claimed = True

        if not any_claimed:
            self.player = self.other_player()
        return True

    def other_player(self):
        return (Owner.red if self.player == Owner.blue 
                           else Owner.blue)
    
    def try_claim_box(self, box):
        num_owned = 0
        for edge in box.edges:
            if edge.owner != Owner.none:
                num_owned += 1

        if num_owned == 4:
            box.owner = self.player
            return True
        return False  

    def check_win(self):
        red_boxes = 0
        blue_boxes = 0
        for box in self.boxes:
            if box.owner == Owner.none: return None
            if box.owner == Owner.red:
                red_boxes += 1
            else:
                blue_boxes += 1
    
        if red_boxes > blue_boxes:
            return Owner.red
        if red_boxes < blue_boxes:
            return Owner.blue
        return Owner.none #TODO: Owner kinda overloaded here?

    def get_edge_owner(self, edge_index):
        return self.edges[edge_index].owner

class Edge:
    def __init__(self):
        self.owner = Owner.none
        self.boxes = []

class Box:
    def __init__(self):
        self.owner = Owner.none
        self.edges = []



board = Game()
board.make_move(1)
board.make_move(3)
board.make_move(4)
board.make_move(10)
# print(board.edges[1].boxes[0].owner, board.player)




size = width, height = 320, 240
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 0, 255

line_color = 0, 255, 0
dot_color = 0, 0, 255
dot_rad = 10

grid_width = 3
grid_height = 3

screen = pygame.display.set_mode(size)
points = []
for h in range(grid_height):
        for w in range(grid_width):
            x = int( (w+0.5) * width // grid_width )
            y = int( (h+0.5) * height // grid_height )
            points.append( (x, y) )
print(points)         

edge_index_to_pair = [
    (points[0], points[1]),
    (points[1], points[2]),
    (points[0], points[3]),
    (points[1], points[4]),
    (points[2], points[5]),
    (points[3], points[4]),
    (points[4], points[5]),
    (points[3], points[6]),
    (points[4], points[7]),
    (points[5], points[8]),
    (points[6], points[7]),
    (points[7], points[8])
]
pair_to_edge_index = {e: i for i, e in enumerate(edge_index_to_pair)}
for i, e in enumerate(edge_index_to_pair): pair_to_edge_index[e[::-1]] = i


while 1:
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_clicked = True
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    # pygame.draw.line(screen,line_color, (60, 80), (130, 100))
    # pygame.draw.circle(screen, circle_color, (50, 50), 20)

    for point in points:
        pygame.draw.circle(screen, 
                           dot_color, 
                           point,
                           dot_rad)


    min_dist = float("inf")
    sec_min_dist = float("inf")
    closest_point = (0, 0)
    sec_closest_point = (0, 0)
    for point in points:
        dist = ( pygame.math.Vector2(*pygame.mouse.get_pos())
         .distance_to(point) )
        if dist < min_dist:
            sec_min_dist = min_dist
            min_dist = dist
            sec_closest_point = closest_point
            closest_point = point
        elif dist < sec_min_dist:
            sec_min_dist = dist
            sec_closest_point = point
    
    pygame.draw.line(screen, line_color, closest_point, sec_closest_point)

    for i in range(len(edge_index_to_pair)):
        if board.get_edge_owner(i) == Owner.red:
            pygame.draw.line(screen, red, *edge_index_to_pair[i])
        elif board.get_edge_owner(i) == Owner.blue:
            pygame.draw.line(screen, blue, *edge_index_to_pair[i])

    if mouse_clicked:
        board.make_move(pair_to_edge_index[(closest_point, sec_closest_point)])
    
    pygame.display.flip()