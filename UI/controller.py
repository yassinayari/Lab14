import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStores(self):
        stores = self._model.getStores()
        for store in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(store))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        k = self._view._txtIntK.value
        try:
            kint = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un numero intero."))
            self._view.update_page()
            return
        if kint < 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un numero intero positivo."))
            self._view.update_page()
            return

        self._model.buildGraph(self._view._ddStore.value, kint)
        allNodes = self._model.getAllNodes()
        self.fillDD(allNodes)

        n, a = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {a}"))


        self._view.update_page()

    def handleCerca(self, e):
        nodes = self._model.getCammino(self._view._ddNode.value)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza : {self._view._ddNode.value}"))
        for n in nodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleRicorsione(self, e):
        pass

    def fillDD(self, allNodes):
        self._view._ddNode.options.clear()
        for n in allNodes:
            self._view._ddNode.options.append(
                ft.dropdown.Option(n))
