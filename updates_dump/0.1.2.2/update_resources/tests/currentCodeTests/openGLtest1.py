import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# Vertex shader
VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 vertexColor;

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
    vertexColor = color;
}
"""

# Fragment shader
FRAGMENT_SHADER = """
#version 330 core
in vec3 vertexColor;
out vec4 fragColor;

void main() {
    fragColor = vec4(vertexColor, 1.0);
}
"""

PLANE_VERTICES = np.array([
    # Positions        # Colors
    -0.5, -0.5, 0.0,   1.0, 0.0, 0.0,
     0.5, -0.5, 0.0,   0.0, 1.0, 0.0,
    -0.5,  0.5, 0.0,   0.0, 0.0, 1.0,
     0.5,  0.5, 0.0,   1.0, 1.0, 0.0,
], dtype=np.float32)

PLANE_INDICES = np.array([0, 1, 2, 2, 1, 3], dtype=np.uint32)

def create_shader_program():
    try:
        vertex_shader = compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        fragment_shader = compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        return compileProgram(vertex_shader, fragment_shader)
    except RuntimeError as e:
        print("Shader compilation error:", e)
        exit(1)

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("2D Plane in 3D Space")

    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

    shader = create_shader_program()
    glUseProgram(shader)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, PLANE_VERTICES.nbytes, PLANE_VERTICES, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, PLANE_INDICES.nbytes, PLANE_INDICES, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * PLANE_VERTICES.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * PLANE_VERTICES.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    projection = np.identity(4, dtype=np.float32)
    view = np.identity(4, dtype=np.float32)
    model = np.identity(4, dtype=np.float32)

    view[3, 2] = -3  # Move back to see the plane

    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")
    model_loc = glGetUniformLocation(shader, "model")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    pos_x, pos_y, pos_z = 0, 0, 0

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            pos_y += 0.01
        if keys[K_s]:
            pos_y -= 0.01
        if keys[K_a]:
            pos_x -= 0.01
        if keys[K_d]:
            pos_x += 0.01
        if keys[K_q]:
            pos_z -= 0.01
        if keys[K_e]:
            pos_z += 0.01

        model = np.identity(4, dtype=np.float32)
        model[3, 0] = pos_x
        model[3, 1] = pos_y
        model[3, 2] = pos_z

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(PLANE_INDICES), GL_UNSIGNED_INT, None)

        pygame.display.flip()
        clock.tick(60)

    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO])
    glDeleteProgram(shader)
    pygame.quit()

if __name__ == "__main__":
    main()

