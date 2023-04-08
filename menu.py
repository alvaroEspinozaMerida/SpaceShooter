import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 175), (125, 75)),
                                            text='Play',
                                            manager=manager)
scores_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (125, 75)),
                                            text='Scores',
                                            manager=manager)
exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 375), (125, 75)),
                                            text='Exit',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == play_button:
                print('Play Button')
            if event.ui_element == scores_button:
                print('Scores Button')
            if event.ui_element == exit_button:
                print('Exit Button')


        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()