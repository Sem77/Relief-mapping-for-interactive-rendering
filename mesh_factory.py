from config import *

def build_triangle_mesh2() -> tuple[tuple[int], int]:
    vertex_data = np.zeros(3, dtype=data_type_vertex)
    vertex_data[0] = (-0.75, -0.75, 0.0, 0)
    vertex_data[1] = (0.75, -0.75, 0.0, 1)
    vertex_data[2] = (0.0, 0.75, 0.0, 2)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1) # Création du VBO pour les positions
    glBindBuffer(GL_ARRAY_BUFFER, vbo) # Activation du VBO
    glBufferData(
        GL_ARRAY_BUFFER, 
        vertex_data.nbytes, # Taille en octet de tout le tableau des positions
        vertex_data, 
        GL_STATIC_DRAW # Indique que ces données ne vont pas changer souvent
    ) # Copie des positions (position_data) dans le GPU
    
    attribute_index = 0 # Indice de l'attribut dans le vertex shader (ici 0 pour les positions)
    size = 3 # Indique qu'il y a 3 composantes par sommet (x, y, z)
    stride = data_type_vertex.itemsize # L'espacement en octets entre deux sommets consécutifs dans le buffer (Un sommet = 3 floats = 3 x 4 = 12)
    offset = 0 # Indique que les données commencent au début du buffer, pas de décalage
    
    glVertexAttribPointer(
        attribute_index, 
        size, 
        GL_FLOAT, 
        GL_FALSE, 
        stride, 
        ctypes.c_void_p(offset)
    )
    glEnableVertexAttribArray(attribute_index) # Active l'attribut (ici les positions)
    offset += 12

    attribute_index = 1
    size = 1
    glVertexAttribIPointer(attribute_index, size, GL_UNSIGNED_INT, stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(attribute_index)

    return (vbo, vao)

def build_triangle_mesh() -> tuple[tuple[int], int]:
    position_data = np.array(
        (-0.75, -0.75, 0.0,
         0.75, -0.75, 0.0,
         0.0, 0.75, 0.0), dtype = np.float32
    )

    color_data = np.array(
        (0, 1, 2), dtype = np.uint32
    )

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    position_buffer = glGenBuffers(1) # Création du VBO pour les positions
    glBindBuffer(GL_ARRAY_BUFFER, position_buffer) # Activation du VBO
    glBufferData(
        GL_ARRAY_BUFFER, 
        position_data.nbytes, # Taille en octet de tout le tableau des positions
        position_data, 
        GL_STATIC_DRAW # Indique que ces données ne vont pas changer souvent
    ) # Copie des positions (position_data) dans le GPU
    
    attribute_index = 0 # Indice de l'attribut dans le vertex shader (ici 0 pour les positions)
    size = 3 # Indique qu'il y a 3 composantes par sommet (x, y, z)
    stride = 12 # L'espacement en octets entre deux sommets consécutifs dans le buffer (Un sommet = 3 floats = 3 x 4 = 12)
    offset = 0 # Indique que les données commencent au début du buffer, pas de décalage
    
    glVertexAttribPointer(
        attribute_index, 
        size, 
        GL_FLOAT, 
        GL_FALSE, 
        stride, 
        ctypes.c_void_p(offset)
    )

    glEnableVertexAttribArray(attribute_index) # Active l'attribut (ici les positions)

    color_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glBufferData(GL_ARRAY_BUFFER, color_data.nbytes, color_data, GL_STATIC_DRAW)
    attribute_index = 1
    size = 1
    stride = 4
    offset = 0
    glVertexAttribIPointer(attribute_index, size, GL_UNSIGNED_INT, stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(attribute_index)

    return ((position_buffer, color_buffer), vao)

def get_vbo_vao_of_object(obj_filepath: str) -> None:

    vertex_data = np.array(load_obj_with_uv(obj_filepath), dtype=np.float32)
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

    # Position : layout(location = 0)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))

    # UV : layout(location = 1)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))

    return (vbo, vao, len(vertex_data))

def create_mesh_with_tangent_and_normal(vertices):
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    stride = 11 * 4  # 11 floats * 4 octets
    glEnableVertexAttribArray(0)  # position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)  # uv
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))

    glEnableVertexAttribArray(2)  # tangent
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(5 * 4))

    glEnableVertexAttribArray(3)  # normal
    glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(8 * 4))

    glBindVertexArray(0)
    return vao, vbo
