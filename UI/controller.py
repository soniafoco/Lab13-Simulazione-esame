import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._year = None
        self._shape = None

    def fillDDyear(self):
        for n in range(1910,2015):
            self._view.ddyear.options.append(ft.dropdown.Option(data=n, text=n, on_click=self.fillDDshape))

    def fillDDshape(self, e):
        self._view.txt_result.controls.clear()
        self._view.ddshape.options = []

        self._year = e.control.data
        forme = self._model.getShapes(self._year)

        if len(forme)==0:
            self._view.txt_result.controls.append(ft.Text("Non ci sono stati avvistamenti nell'anno selezionato"))
        else:
            for forma in forme:
                self._view.ddshape.options.append(ft.dropdown.Option(data=forma, text=forma, on_click=self.readDDshape))

        self._view.update_page()

    def readDDshape(self, e):
        self._shape = e.control.data
        print(self._shape)

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()

        if self._year is None or self._shape is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno e una forma!!"))
        else:
            self._model.buildGraph(self._year, self._shape)
            nodes, edges = self._model.getDetails()
            self._view.txt_result.controls.append(ft.Text(f"Creato grafo con {nodes} nodi e {edges} archi."))

            vicini = self._model.getVicini()
            for nodo in vicini:
                self._view.txt_result.controls.append(ft.Text(f"Nodo {nodo[0].__str__()} --> somma pesi sugli archi = {nodo[1]}"))

        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut2.controls.clear()

        score, path = self._model.getPercorso()
        self._view.txtOut2.controls.append(ft.Text(f"Trovato percorso di peso massimo {score}"))
        for p in path:
            self._view.txtOut2.controls.append(ft.Text(f"{p[0]} --> {p[1]}: peso={p[2]}, distanza={p[3]}"))

        self._view.update_page()