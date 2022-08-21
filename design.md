- show winner
- allow game to be restarted
- better indication of whose turn it is (preview edge from green to a shade of blue/red)
- change dots to something other than blue
- show number of boxes claimed in text
- add AI
- sound?
- "juicy" animations? See this talk: https://www.youtube.com/watch?v=Fy0aCDmgnxg


```
Box {
    owner: 0
    edges: Edge[]
}
Edge {
    owner: 0,
    Boxes: Box[]
}

o <-> o <-> o
|  a  |  b  |
o <-> o <-> o
|  c  |  d  |
o <-> o <-> o
```
Control flow:

click (hover) -> two closest dots (found by iteration) -> edge -> box -> are all the edges filled?

Game over when all edges are filled? 

Checking the legality of moves? OK--see above

normalize screen coords to lst coords, then key into a data structure to find the edge:
```
((0, 0) (0, 1)) -> Edge
((0, 0) (1, 0)) -> Edge
...
```

------

not necessary probs:

```
Node: {
    n: Node,
    e: Node,
    s: Node,
    w: Node, (or null if on edge) 

    n_linked: False,
    s_linked: True,
    e_linked: False,
    w_linked: False,

    prepopulated: Box[]
}
```