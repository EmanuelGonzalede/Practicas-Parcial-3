import itertools
import random


class Minesweeper():
    """
    Representación del juego Buscaminas
    """

    def __init__(self, height=8, width=8, mines=8):

        # Establecer la anchura, altura y número de minas inicial
        self.height = height
        self.width = width
        self.mines = set()

        # Inicializar un campo vacío sin minas
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Añadir minas aleatoriamente
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # Al principio, el jugador no ha encontrado ninguna mina
        self.mines_found = set()

    def print(self):
        """
        Imprime una representación textual
        de dónde están ubicadas las minas.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Devuelve el número de minas que están
        dentro de una fila y columna de una celda dada,
        sin incluir la propia celda.
        """

        # Mantener el conteo de minas cercanas
        count = 0

        # Recorrer todas las celdas dentro de una fila y columna
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignorar la propia celda
                if (i, j) == cell:
                    continue

                # Actualizar el conteo si la celda está dentro del rango y es una mina
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Verifica si todas las minas han sido marcadas.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Declaración lógica sobre un juego de Buscaminas
    Una oración consiste en un conjunto de celdas del tablero,
    y un conteo del número de esas celdas que son minas.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Devuelve el conjunto de todas las celdas en self.cells conocidas como minas.
        """
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        Devuelve el conjunto de todas las celdas en self.cells conocidas como seguras.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Actualiza la representación interna del conocimiento dado el hecho de que
        una celda se sabe que es una mina.
        """
        newCells = set()
        for item in self.cells:
            if item != cell:
                newCells.add(item)
            else:
                self.count -= 1
        self.cells = newCells

    def mark_safe(self, cell):
        """
        Actualiza la representación interna del conocimiento dado el hecho de que
        una celda se sabe que es segura.
        """
        newCells = set()
        for item in self.cells:
            if item != cell:
                newCells.add(item)
        self.cells = newCells
        


class MinesweeperAI():
    """
    Jugador del juego Buscaminas
    """

    def __init__(self, height=8, width=8):

        # Establecer altura y ancho inicial
        self.height = height
        self.width = width

        # Mantener un registro de las celdas en las que se ha hecho clic
        self.moves_made = set()

        # Mantener un registro de las celdas conocidas como seguras o minas
        self.mines = set()
        self.safes = set()

        # Lista de oraciones sobre el juego conocidas como verdaderas
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marca una celda como mina, y actualiza todo el conocimiento
        para marcar esa celda como mina también.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marca una celda como segura, y actualiza todo el conocimiento
        para marcar esa celda como segura también.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Llamado cuando el tablero de Buscaminas nos dice, para una celda segura dada,
        cuántas celdas vecinas tienen minas.

        Esta función debería:
            1) marcar la celda como un movimiento que se ha realizado
            2) marcar la celda como segura
            3) añadir una nueva oración a la base de conocimiento de la IA
               basada en el valor de `celda` y `cuenta`
            4) marcar celdas adicionales como seguras o como minas
               si se puede concluir basado en la base de conocimiento de la IA
            5) añadir nuevas oraciones a la base de conocimiento de la IA
               si se pueden inferir del conocimiento existente
        """
        # Marcar celda como segura y agregar a moves_made
        self.mark_safe(cell)
        self.moves_made.add(cell)

        # Crear y agregar oración al conocimiento
        neighbors, count = self.get_cell_neighbors(cell, count)
        sentence = Sentence(neighbors, count)
        self.knowledge.append(sentence)

        # Conclusión
        new_inferences = []
        for s in self.knowledge:
            if s == sentence:
                continue
            elif s.cells.issuperset(sentence.cells):
                setDiff = s.cells-sentence.cells
                # Seguras conocidas
                if s.count == sentence.count:
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)
                # Minas conocidas
                elif len(setDiff) == s.count - sentence.count:
                    for mineFound in setDiff:
                        self.mark_mine(mineFound)
                # Inferencia conocida
                else:
                    new_inferences.append(
                        Sentence(setDiff, s.count - sentence.count)
                    )
            elif sentence.cells.issuperset(s.cells):
                setDiff = sentence.cells-s.cells
                # Seguras conocidas
                if s.count == sentence.count:
                    for safeFound in setDiff:
                        self.mark_safe(safeFound)
                # Minas conocidas
                elif len(setDiff) == sentence.count - s.count:
                    for mineFound in setDiff:
                        self.mark_mine(mineFound)
                # Inferencia conocida
                else:
                    new_inferences.append(
                        Sentence(setDiff, sentence.count - s.count)
                    )

        self.knowledge.extend(new_inferences)
        self.remove_dups()
        self.remove_sures()

    def make_safe_move(self):
        """
        Devuelve una celda segura para elegir en el tablero de Buscaminas.
        El movimiento debe ser conocido como seguro y no ser un movimiento
        que ya se haya realizado.

        Esta función puede usar el conocimiento en self.mines, self.safes
        y self.moves_made, pero no debe modificar ninguno de esos valores.
        """
        safeCells = self.safes - self.moves_made
        if not safeCells:
            return None
        # print(f"Pool: {safeCells}")
        move = safeCells.pop()
        return move

    def make_random_move(self):
        """
        Devuelve un movimiento para realizar en el tablero de Buscaminas.
        Debe elegir aleatoriamente entre celdas que:
            1) no hayan sido elegidas ya, y
            2) no sean conocidas como minas
        """
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.mines and (i,j) not in self.moves_made:
                    all_moves.add((i,j))
        # No quedan movimientos
        if len(all_moves) == 0:
            return None
        # Devolver disponible
        move = random.choice(tuple(all_moves))
        return move
               
    def get_cell_neighbors(self, cell, count):
        i, j = cell
        neighbors = []

        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if (row >= 0 and row < self.height) \
                and (col >= 0 and col < self.width) \
                and (row, col) != cell \
                and (row, col) not in self.safes \
                and (row, col) not in self.mines:
                    neighbors.append((row, col))
                if (row, col) in self.mines:
                    count -= 1

        return neighbors, count

    def remove_dups(self):
        unique_knowledge = []
        for s in self.knowledge:
            if s not in unique_knowledge:
                unique_knowledge.append(s)
        self.knowledge = unique_knowledge

    def remove_sures(self):
        final_knowledge = []
        for s in self.knowledge:
            final_knowledge.append(s)
            if s.known_mines():
                for mineFound in s.known_mines():
                    self.mark_mine(mineFound)
                final_knowledge.pop(-1)
            elif s.known_safes():
                for safeFound in s.known_safes():
                    self.mark_safe(safeFound)
                final_knowledge.pop(-1)
        self.knowledge = final_knowledge