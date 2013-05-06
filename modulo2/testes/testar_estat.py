# coding:

import unittest

from estat import media

class TestarFuncoesEstatisticas(unittest.TestCase):

    def testar_media(self):
        self.assertEqual(media([20, 30, 70]), 40.0)
        self.assertAlmostEqual(media([1, 5, 7]), 4 + 1/3.)
        self.assertRaises(ZeroDivisionError, media, [])
        self.assertRaises(TypeError, media, 20, 30, 70)

if __name__=='__main__':
    # Chamando da linha de comando, executa todos os testes
    unittest.main()
