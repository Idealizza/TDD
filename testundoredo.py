# -*- coding: utf-8 -*-
import unittest


class RedoException(Exception):
    def __init__(self,msg):
        self.message = msg

class UndoException(Exception):
    def __init__(self,msg):
        self.message = msg

class Editor(object):

    def __init__(self):
        self.conteudo = []
        self.historico = []
    
    def comando(self, cmd):
        self.conteudo.append(cmd)
        self.historico = []

    def undo(self):
        if not self.conteudo:
            raise UndoException('Undo Exception')
        self.historico.append(self.conteudo.pop())
    
    def redo(self):
        if len(self.historico) == 0:
            raise RedoException('Redo unavailable')
        self.conteudo.append(self.historico.pop())



class TesteUndoRedo(unittest.TestCase):
    ''' 
    se a lista tiver 1+ comando. só podemos fazer 'undo'
    se a lista estiver vazia, não podemos fazer nada

    se já foi feito 'undo' pode fazer 'redo'
    
    If we add command 1, then command 2, then undo 2, then add command 3, we can undo 3.

    se foi feita a mesma quantidades de 'redo' do que foi feitas 'undo' não podemos mais fazer 'redo'
    '''
    def test_add_comando(self):
        editor = Editor()
        editor.comando(1)
        self.assertEqual(1, len(editor.conteudo))

    def test_undo_um_comando(self):
        editor = Editor()
        editor.comando(1)
        editor.undo()
        self.assertEqual(0, len(editor.conteudo))

    def test_undo_dois_comandos(self):
        editor = Editor()
        editor.comando(1)
        editor.comando(2)
        editor.undo()
        self.assertEqual([1], editor.conteudo)

    def test_dois_undo_um_comando(self):
        editor = Editor()
        editor.comando(1)
        editor.undo()
        self.assertRaises(UndoException, editor.undo)

    def test_undo_sem_nenhum_comando (self):
        editor = Editor()
        self.assertRaises(UndoException, editor.undo)

    def test_redo_um_comando (self):
        editor = Editor()
        editor.comando(1)
        editor.undo()
        editor.redo()
        self.assertEqual([1], editor.conteudo)

    def test_redo_dois_comandos (self) :
        editor = Editor()
        editor.comando(1)
        editor.comando(2)
        editor.undo()
        editor.redo()
        self.assertEqual([1,2], editor.conteudo)

    def test_um_undo_dois_redo (self) :
        editor = Editor()
        editor.comando(1)
        editor.comando(2)
        editor.undo()
        editor.redo()
        self.assertRaises(RedoException, editor.redo)

    def test_redo_sem_nenhum_comando (self):
        editor = Editor()
        self.assertRaises(RedoException, editor.redo)

    def test_dois_comandos_undo_comando_undo(self):
        editor = Editor()
        editor.comando(1)
        editor.comando(2)
        editor.undo()
        editor.comando(3)
        editor.comando(4)
        self.assertRaises(RedoException, editor.redo)

    def test_redo_um_comando_plusplus(self):
        editor = Editor()
        editor.comando(1)
        editor.comando(2)
        editor.undo()
        editor.undo()
        editor.redo()
        editor.redo()
        self.assertEqual([1,2], editor.conteudo)
        
if __name__ == '__main__':
    unittest.main()
    
