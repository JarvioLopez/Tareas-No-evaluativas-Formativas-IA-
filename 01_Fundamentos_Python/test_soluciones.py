import unittest

from soluciones_fundamentos import esta_ordenada, restar


class TestResta(unittest.TestCase):
    def test_resta_positiva(self) -> None:
        self.assertEqual(restar(10, 4), 6)

    def test_resta_con_negativos(self) -> None:
        self.assertEqual(restar(-5, -3), -2)

    def test_resta_decimal(self) -> None:
        self.assertAlmostEqual(restar(7.5, 2.25), 5.25)


class TestListaOrdenada(unittest.TestCase):
    def test_lista_ordenada(self) -> None:
        self.assertTrue(esta_ordenada([1, 2, 3, 4]))

    def test_lista_desordenada(self) -> None:
        self.assertFalse(esta_ordenada([3, 1, 2]))

    def test_lista_con_duplicados_ordenados(self) -> None:
        self.assertTrue(esta_ordenada([1, 1, 2, 2, 3]))

    def test_lista_vacia(self) -> None:
        self.assertTrue(esta_ordenada([]))


if __name__ == "__main__":
    unittest.main()
