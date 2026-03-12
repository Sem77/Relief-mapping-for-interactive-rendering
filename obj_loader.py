from config import *

def load_obj(filepath):
    vertices = []
    faces = []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()[1:]
                vertices.append([float(x) for x in parts])
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = [int(p.split('/')[0]) - 1 for p in parts]
                faces.append(face)

    # Aplatir les faces (triangulées)
    flat_vertices = []
    for face in faces:
        for idx in face:
            flat_vertices.extend(vertices[idx])
    return flat_vertices


def load_obj_with_uv(filepath):
    positions = []
    uvs = []
    faces = []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()[1:]
                positions.append([float(x) for x in parts])
            elif line.startswith('vt '):
                parts = line.strip().split()[1:]
                uvs.append([float(x) for x in parts])
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = []
                for p in parts:
                    v_idx, vt_idx, *_ = p.split('/')
                    face.append((int(v_idx)-1, int(vt_idx)-1))
                faces.append(face)

    interleaved = []
    for face in faces:
        for v_idx, vt_idx in face:
            interleaved.extend(positions[v_idx])
            interleaved.extend(uvs[vt_idx])
    
    return np.array(interleaved, dtype=np.float32)


def load_texture(path):

    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM) # Pour mettre le 0,0 en bas à gauche
    img_data = image.convert("RGBA").tobytes()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexImage2D(
        GL_TEXTURE_2D,      # Type de texture (2D)
        0,                  # Niveau de mipmap (0 = base)
        GL_RGBA,            # Format interne (sur la GPU)
        image.width,        # largeur de l'image
        image.height,       # hauteur de l'image
        0,                  # bordure (doit être 0)
        GL_RGBA,            # format des données source (CPU)
        GL_UNSIGNED_BYTE,   # type des données (uint8)
        img_data            # pointeur vers les pixels
    )

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)        # Répète la texture si la coordonnée U est hors [0, 1]
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)        # Répète la texture si la coordonnée V est hors [0, 1]
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture

def load_obj_with_tangent_and_normal(path):
    positions = []
    uvs = []
    normals = []
    faces = []

    with open(path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                positions.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vt '):
                uvs.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vn '):
                normals.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = []
                for p in parts:
                    v, t, n = map(int, p.split('/'))
                    face.append((v - 1, t - 1, n - 1))
                faces.append(face)

    vertices = []
    for face in faces:
        # 3 sommets par face (triangle)
        p0, t0, n0 = face[0]
        p1, t1, n1 = face[1]
        p2, t2, n2 = face[2]

        # positions
        v0 = positions[p0]
        v1 = positions[p1]
        v2 = positions[p2]

        # UVs
        uv0 = uvs[t0]
        uv1 = uvs[t1]
        uv2 = uvs[t2]

        # calcul tangent
        delta_pos1 = [v1[i] - v0[i] for i in range(3)]
        delta_pos2 = [v2[i] - v0[i] for i in range(3)]
        delta_uv1 = [uv1[i] - uv0[i] for i in range(2)]
        delta_uv2 = [uv2[i] - uv0[i] for i in range(2)]

        r = 1.0 / ((delta_uv1[0] * delta_uv2[1] - delta_uv1[1] * delta_uv2[0]) + 1e-4)
        tangent = [
            r * (delta_uv2[1] * delta_pos1[i] - delta_uv1[1] * delta_pos2[i])
            for i in range(3)
        ]

        for idx in [0, 1, 2]:
            vi, ti, ni = face[idx]
            vertices.extend(positions[vi])
            vertices.extend(uvs[ti])
            vertices.extend(tangent)
            vertices.extend(normals[ni])

    return np.array(vertices, dtype=np.float32)