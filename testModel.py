from model.model import Model

m = Model()

m.buildGraph(2010, "circle")

score, path = m.getPercorso()
print(score)
for p in path:
    print(f"{p[0]} --> {p[1]}: peso={p[2]}, distanza={p[3]}")