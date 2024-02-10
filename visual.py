import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from CAN import receive_can_message
import random
#from CAN import update_pos


def draw_water():
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1) 
    glEnd()

def boat():
    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)  
    # Bottom Face
    glVertex3f(-1, -0.5, -2)  # Back-Left
    glVertex3f(1, -0.5, -2)   # Back-Right
    glVertex3f(1, -0.5, 2)    # Front-Right
    glVertex3f(-1, -0.5, 2)   # Front-Left

    # Top Face
    glVertex3f(-1, 0.5, 2)    # Front-Left
    glVertex3f(1, 0.5, 2)     # Front-Right
    glVertex3f(1, 0.5, -2)    # Back-Right
    glVertex3f(-1, 0.5, -2)   # Back-Left

    # Back Face
    glVertex3f(-1, -0.5, -2)  # Bottom-Left
    glVertex3f(1, -0.5, -2)   # Bottom-Right
    glVertex3f(1, 0.5, -2)    # Top-Right
    glVertex3f(-1, 0.5, -2)   # Top-Left

    # Left Face
    glVertex3f(-1, -0.5, -2)  # Bottom-Back
    glVertex3f(-1, -0.5, 2)   # Bottom-Front
    glVertex3f(-1, 0.5, 2)    # Top-Front
    glVertex3f(-1, 0.5, -2)   # Top-Back

    # Right Face
    glVertex3f(1, -0.5, -2)   # Bottom-Back
    glVertex3f(1, -0.5, 2)    # Bottom-Front
    glVertex3f(1, 0.5, 2)     # Top-Front
    glVertex3f(1, 0.5, -2)    # Top-Back

    glEnd()

  


"""
Surge: Movement forward or backward (along the X-axis).
Sway: Movement left or right (along the Y-axis).
Heave: Movement up or down (along the Z-axis).
Roll: Rotation around the X-axis.
Pitch: Rotation around the Y-axis.
Yaw: Rotation around the Z-axis."""

def rand_direction():
    return random.randint(-1, 1)
def update_boat_motion(roll, pitch, yaw, surge, sway, heave):
    """
    Update the boat's position and orientation.
    """
    # Define factors to scale the translation and rotation
    translation_factor = 0.0000005   # Adjust this value as needed
    rotation_factor = 0.00003       # Adjust this value as needed

   

    # Update position (translate) for surge, sway, heave
    glTranslatef(surge * translation_factor*rand_direction(),
                  sway * translation_factor*rand_direction(), heave * translation_factor*rand_direction())

    # Update orientation (rotate) for roll, pitch, yaw
    glRotatef(roll * rotation_factor*rand_direction(), 1.0, 0.0, 0.0)   # Roll around the X-axis
    glRotatef(pitch * rotation_factor*rand_direction(), 0.0, 1.0, 0.0)  # Pitch around the Y-axis
    glRotatef(yaw * rotation_factor*rand_direction(), 0.0, 0.0, 1.0)    # Yaw around the Z-axis

def create_text_surface(text):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))  # White color
    return text_surface

def surface_to_texture(surface):
    texture_data = pygame.image.tostring(surface, "RGBA", 1)
    width = surface.get_width()
    height = surface.get_height()
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return texture

def create_text_surface(text):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))  # White color
    return text_surface
def display_text(label, value, position):
    # Create text surfaces for the label and value
    label_surface = create_text_surface(label)
    value_surface = create_text_surface(value)

    # Calculate positions for label and value
    label_position = position
    value_position = (position[0] + label_surface.get_width() + 10, position[1])

    # Render label
    render_text_surface(label_surface, label_position)

    # Render value
    render_text_surface(value_surface, value_position)

def render_text_surface(surface, position):
    # Switch to orthographic projection
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    width, height = pygame.display.get_surface().get_size()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    # Create and draw the text texture
    glColor3f(1, 1, 1)  # Set text color to white
    texture = surface_to_texture(surface)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(position[0], position[1])
    glTexCoord2f(1, 1); glVertex2f(position[0] + surface.get_width(), position[1])
    glTexCoord2f(1, 0); glVertex2f(position[0] + surface.get_width(), position[1] + surface.get_height())
    glTexCoord2f(0, 0); glVertex2f(position[0], position[1] + surface.get_height())
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glDeleteTextures(1, [texture])

    # Restore the original projection and modelview matrices
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

# Example usage:
# display_text("Surge:", str(can_data['surge']), (10, 20))



def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 30)
    gluLookAt(3, 1, 5, 0, 0, 0, 0, 1, 0)

    # Initialize font
    pygame.font.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        can_data = receive_can_message()
        update_boat_motion(can_data["roll"], can_data["pitch"], can_data["yaw"], 
                           can_data["surge"], can_data["sway"], can_data["heave"])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_water()
        boat()
        # Display motion values
        display_text("Surge:", str(can_data['surge']), (10, 20))
        display_text("Sway:", str(can_data['sway']), (10, 60))
        display_text("Heave:", str(can_data['heave']), (10, 100))
        display_text("Roll:", str(can_data['roll']), (10, 140))
        display_text("Pitch:", str(can_data['pitch']), (10, 180))
        display_text("Yaw:", str(can_data['yaw']), (10, 220))


        pygame.display.flip()
        pygame.time.wait(1000)

main()