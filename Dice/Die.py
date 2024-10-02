class Die():
    def __init__ (self, path = None, node = None, np = None):
        self._path = path
        self._node = node
        self._np = np

    @property
    def file_path(self):
        return self._path
    
    @file_path.setter
    def file_path(self, new_path):
        self._path = new_path
    
    @property
    def node(self):
        return self._node
    
    @node.setter
    def node(self, new_node):
        self._node = new_node

    @property
    def np(self):
        return self._np
    
    @np.setter
    def np(self, new_np):
        self._np = new_np

    def get_face_value(self):
        pass
