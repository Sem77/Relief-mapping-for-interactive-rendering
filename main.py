from config import *

class App:

    def __init__(self):

        # Attributs position de la souris
        self.last_mouse_x = SCREEN_WIDTH // 2
        self.last_mouse_y = SCREEN_HEIGHT // 2
        self.yaw = 0.0      # rotation autour de l'axe Y
        self.pitch = 0.0    # rotation autour de l'axe X
        self.first_mouse = True
        self.mouse_pressed = False
        self.zoom = -5.0

        self.initialize_glfw()
        self.initialize_opengl()

    def initialize_glfw(self) -> None:

        glfw.init()
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, 
            GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.DEPTH_BITS, 24)  # ← important pour activer un depth buffer 24 bits
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT,
            GLFW_CONSTANTS.GLFW_TRUE)
        self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "My window", None, None)
        glfw.make_context_current(self.window)

        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

    def initialize_opengl(self) -> None:

        glClearColor(0.0, 0.0, 0.0, 1.0) # Définit la couleur du fond
        glDisable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        """
        self.cube_vao, self.cube_vbo, self.len_cube_vertices = get_vbo_vao_of_object("data/objects/cube_relief.obj")
        self.texture = load_texture("data/textures/brickbump.png")
        self.shader = create_shader_program("shaders/vertex.glsl", "shaders/fragment.glsl")
        
        glUseProgram(self.shader) # Active le shader
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(glGetUniformLocation(self.shader, "texture_diffuse"), 0)
        """
        
        vertices = load_obj_with_tangent_and_normal("data/objects/cube_relief.obj")
        self.cube_vao, self.cube_vbo = create_mesh_with_tangent_and_normal(vertices)
        self.len_cube_vertices = len(vertices) // 11 # car 11 floats par sommet

        self.diffuse_texture = load_texture("data/textures/rockbump.png")
        self.relief_texture = load_texture("data/textures/rockbump.tga")
        self.shader = create_shader_program("shaders/vertex_relief.glsl", "shaders/fragment_relief.glsl")
        
        glUseProgram(self.shader)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.diffuse_texture)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.relief_texture)

        glUniform1i(glGetUniformLocation(self.shader, "diffuse_map"), 0)    # glGetUniformLocation retrouve l'emplacement de diffuse_map dans le shader et glUniform1i l'associe à la texture stockée à l'emplacement 0
        glUniform1i(glGetUniformLocation(self.shader, "relief_map"), 1)     # IDEM


    def create_projection(self, fov, aspect, near, far):

        f = 1.0 / math.tan(math.radians(fov) / 2)
        proj = np.zeros((4, 4), dtype=np.float32)
        proj[0, 0] = f / aspect
        proj[1, 1] = f
        proj[2, 2] = (far + near) / (near - far)
        proj[2, 3] = -1.0
        proj[3, 2] = (2 * far * near) / (near - far)

        return proj

    def run(self):
        model_loc = glGetUniformLocation(self.shader, "model")
        proj_loc = glGetUniformLocation(self.shader, "projection")

        projection = self.create_projection(45.0, 800 / 600, 0.1, 100.0)
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        while not glfw.window_should_close(self.window):

            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                break
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            yaw_rad = math.radians(self.yaw)
            pitch_rad = math.radians(-self.pitch)

            cos_y = math.cos(yaw_rad)
            sin_y = math.sin(yaw_rad)
            cos_p = math.cos(pitch_rad)
            sin_p = math.sin(pitch_rad)

            model = np.array([
                [ cos_y, sin_p * sin_y, sin_y * cos_p, 0],
                [    0,       cos_p,         -sin_p,   0],
                [-sin_y, sin_p * cos_y, cos_y * cos_p, 0],
                [   0,      0,             self.zoom,  1]
            ], dtype=np.float32)

            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

            glUniform3f(glGetUniformLocation(self.shader, "eye_pos"), 0.0, 0.0, 0.0)        # Envoie la position de la caméra au shader
            glUniform3f(glGetUniformLocation(self.shader, "light_pos"), 4.0, 0.0, 1.0)      # Envoie la position de la lumière au shader
            glUniform1f(glGetUniformLocation(self.shader, "scale"), 0.005)                  # Envoie le facteur d'échelle au shader
            
            glBindVertexArray(self.cube_vao)
            glDrawArrays(GL_TRIANGLES, 0, self.len_cube_vertices)

            glfw.swap_buffers(self.window)


    def quit(self):

        glDeleteBuffers(1, (self.cube_vbo,))
        glDeleteVertexArrays(1, (self.cube_vao,))
        glDeleteProgram(self.shader)
        glfw.destroy_window(self.window)
        glfw.terminate()

    def mouse_callback(self, window, xpos, ypos):
        if not self.mouse_pressed:
            return  # Ne rien faire si le clic gauche n'est pas enfoncé

        if self.first_mouse:
            self.last_mouse_x = xpos
            self.last_mouse_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_mouse_x
        yoffset = self.last_mouse_y - ypos  # inversé car Y va vers le bas

        self.last_mouse_x = xpos
        self.last_mouse_y = ypos

        sensitivity = 0.3
        self.yaw += xoffset * sensitivity
        self.pitch += yoffset * sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch))

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self.mouse_pressed = True
                self.first_mouse = True
            elif action == glfw.RELEASE:
                self.mouse_pressed = False

    def scroll_callback(self, window, xoffset, yoffset):
        self.zoom += yoffset * 0.5  # facteur de zoom
        self.zoom = max(-20.0, min(-1.0, self.zoom))  # limite de zoom



my_app = App()
my_app.run()
my_app.quit()