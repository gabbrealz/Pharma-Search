import os
import sys

app_filepath = os.path.dirname(__file__)

sys.path.append(app_filepath+"/inverted_index")
sys.path.append(app_filepath+"/general_functionality")
sys.path.append(app_filepath+"/gui")
sys.path.append(app_filepath+"/prefix_tree")

from PyQt5.QtWidgets import QApplication

from multiprocessing import Pool, cpu_count
from setup_main import MainWindow

from searcher import Searcher
from loader import Loader
from history import History
from prefix_tree2 import Trie
from trie_node import TrieNode
from auto_completer import TrieModel



if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        pool = Pool(processes=max(1, cpu_count()-1))
    except Exception as e:
        print(f"Failed to create process pool: {e}")
        sys.exit(1)

    searcher = Searcher(pool)
    loader = Loader(pool)
    history = History()

    trie = Trie()
    trie_model = TrieModel(trie)

    window = MainWindow(searcher, loader, history, trie_model)
    window.show()

    exit_code = app.exec_()

    pool.close()
    pool.join()

    sys.exit(exit_code)