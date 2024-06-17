import unittest
import buscaminas as ms

class TestMinesweeper(unittest.TestCase):

    def test_mark_mine(self):
        sentence = ms.Sentence([(0,1), (0,2), (0,3)], 2)

        # Primera celda
        sentence.mark_mine((0,1))
        self.assertEqual({(0,2), (0,3)}, sentence.cells)

        # Segunda celda
        sentence.mark_mine((0,2))
        self.assertEqual({(0,3)}, sentence.cells)

        # Celda NO en la oración
        sentence.mark_mine((2,1))
        self.assertEqual({(0,3)}, sentence.cells)

        # Comprobar conteo de minas
        self.assertEqual(0, sentence.count)

    def test_mark_safe(self):
        sentence = ms.Sentence([(0,1), (0,2), (0,3)], 2)

        # Primera celda
        sentence.mark_safe((0,1))
        self.assertEqual({(0,2), (0,3)}, sentence.cells)

        # Segunda celda
        sentence.mark_safe((0,2))
        self.assertEqual({(0,3)}, sentence.cells)

        # Celda NO en la oración
        sentence.mark_safe((2,1))
        self.assertEqual({(0,3)}, sentence.cells)

        # Comprobar conteo de minas
        self.assertEqual(2, sentence.count)

    def test_known_mines(self):

        # Todas son minas
        sentence = ms.Sentence([(0,1), (0,2), (0,3)], 3)
        self.assertEqual({(0,1), (0,2), (0,3)}, sentence.known_mines())

        # No conocidas
        sentence = ms.Sentence([(0,1), (0,2), (0,3)], 2)
        self.assertIsNone(sentence.known_mines())

    def test_known_safes(self):

        # Todas son seguras
        sentence = ms.Sentence([(0,1), (0,2), (0,3)], 0)
        self.assertEqual({(0,1), (0,2), (0,3)}, sentence.known_safes())

        # No conocidas
        sentence = ms.Sentence([(0,1), (0,2), (0,3)], 2)
        self.assertIsNone(sentence.known_safes())

    def test_get_cell_neighbors(self):
        msAi = ms.MinesweeperAI()

        # Vecino de la esquina superior izquierda
        cell = (0,0)
        self.assertEqual(
            msAi.get_cell_neighbors(cell, 0)[0],
            [(0,1), (1,0), (1,1)]
        )

        # Vecino de la esquina superior derecha
        cell = (0,7)
        self.assertEqual(
            msAi.get_cell_neighbors(cell, 0)[0],
            [(0,6), (1,6), (1,7)]
        )

        # Vecino de la esquina inferior derecha
        cell = (7,7)
        self.assertEqual(
            msAi.get_cell_neighbors(cell, 0)[0],
            [(6,6), (6,7), (7,6)]
        )

        # Vecino de la esquina inferior izquierda
        cell = (7,0)
        self.assertEqual(
            msAi.get_cell_neighbors(cell, 0)[0],
            [(6,0), (6,1), (7,1)]
        )

        # Vecino del centro
        cell = (4,4)
        self.assertEqual(
            msAi.get_cell_neighbors(cell, 0)[0],
            [(3,3), (3,4), (3,5), (4,3), (4,5), (5,3), (5,4), (5,5)]
        )

    def test_add_knowledge(self):

        # Sin minas vecinas
        msAi = ms.MinesweeperAI()
        msAi.add_knowledge((7,0), 0)
        self.assertEqual(msAi.knowledge, [])

        # Todas las minas vecinas
        msAi = ms.MinesweeperAI()
        msAi.add_knowledge((7,7), 3)
        self.assertEqual(msAi.knowledge, [])

        # Desconocido
        msAi = ms.MinesweeperAI()
        msAi.add_knowledge((0,0), 1)
        sentence = ms.Sentence([(0,1),(1,0),(1,1)], 1)
        self.assertEqual(msAi.knowledge, [sentence])

        # Caso de ejemplo
        msAi = ms.MinesweeperAI(3, 3)
        msAi.add_knowledge((0,0), 1)
        msAi.add_knowledge((0,1), 1)
        msAi.add_knowledge((0,2), 1)
        msAi.add_knowledge((2,1), 2)
        sentence = ms.Sentence({(2,0),(2,2)}, 1)
        self.assertEqual(msAi.knowledge, [sentence])

    def test_make_safe_move(self):

        # Tener movimientos seguros
        msAi = ms.MinesweeperAI(3, 3)
        msAi.add_knowledge((0,0), 1)
        msAi.add_knowledge((0,1), 1)
        msAi.add_knowledge((0,2), 1)
        msAi.add_knowledge((2,1), 2)
        self.assertIsNotNone(msAi.make_safe_move())

        # Sin movimientos seguros
        msAi = ms.MinesweeperAI()
        msAi.add_knowledge((7,7), 3)
        self.assertIsNone(msAi.make_safe_move())

    def test_make_random_move(self):

        # Cualquier movimiento
        msAi = ms.MinesweeperAI(3, 3)
        msAi.add_knowledge((0,0), 1)
        msAi.add_knowledge((0,1), 1)
        msAi.add_knowledge((0,2), 1)
        msAi.add_knowledge((2,1), 2)
        move = msAi.make_random_move()
        self.assertIsNotNone(move)


if __name__ == "__main__":
    unittest.main()