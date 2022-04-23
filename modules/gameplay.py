"""fichier contenant la fonction de la gameplay codé par Solène (@periergeia) TG8."""


# importation de librairies python utiles
import time
import pygame
try:
    from diego import insert_local_score
    from solene_1 import Chronometer, Bag, Data
    from solene_1 import resize_all, display_all
    from solene_1 import display_game_data, create_game_pause, get_game_picture
    from solene_2 import Matrix, Tetrimino, HoldQueue, NextQueue
    from useful import loop_starter_pack, Button2
except ModuleNotFoundError:
    from modules.diego import insert_local_score
    from modules.solene_1 import Chronometer, Bag, Data
    from modules.solene_1 import resize_all, display_all
    from modules.solene_1 import display_game_data, create_game_pause, get_game_picture
    from modules.solene_2 import Matrix, Tetrimino, HoldQueue, NextQueue
    from modules.useful import loop_starter_pack, Button2


def gameplay(window, game_type):
    """
    Gameplay du jeu tetris.
    """
    w_width, w_height = window.get_size()
    window_data = {'size': (w_width, w_height),
                   'width': w_width,
                   'height': w_height,
                   'margin': round(0.05 * w_height)}
    bag = Bag()
    game_chrono = Chronometer()
    matrix = Matrix(window_data, game_type)
    matrix_data = {'rect': matrix.rect,
                   'cell_size': matrix.cell_size}

    tetrimino = Tetrimino(bag, matrix)

    next_queue = NextQueue(window_data, matrix_data, bag)
    hold_queue = HoldQueue(window_data, matrix_data)
    data = Data(window_data, matrix_data, game_chrono, game_type)

    menu_button = Button2(window, (0.9, 0.05, 0.04), 'option')

    game_object = (tetrimino, matrix, next_queue, hold_queue, data, menu_button)

    display_all(window, game_object)

    time_before_refresh = Chronometer()
    lock_down_chrono = Chronometer()

    shade_phase = 1
    lock_phase_first = 1
    softdrop = False
    game_paused = False

    proceed = {'state': True, 'type': 'lose'}

    while proceed['state']:

        game_object = (tetrimino, matrix, next_queue, hold_queue, data, menu_button)

        # évènements pygame
        for event in pygame.event.get():
            window = loop_starter_pack(window, event)
            if event.type == pygame.VIDEORESIZE:
                window_w, window_h = window.get_size()
                window_data = {'size': (window_w, window_h),
                               'width': window_w,
                               'height': window_h,
                               'margin': round(0.05 * window_h)}
                # reaffichage avec changement des tailles et emplacement des objets
                resize_all(window_data, game_object)
                display_all(window, game_object)
                if game_paused:
                    display_game_data(window, data, game_chrono)
                    resume_button, option_button = create_game_pause(window)

            if menu_button.is_pressed(event):
                game_paused = not game_paused
                if game_paused:
                    game_chrono.freeze()
                    resume_button, option_button = create_game_pause(window)
                else:
                    game_chrono.unfreeze()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    softdrop = False
                    data.set_fall_speed()

            if event.type == pygame.KEYDOWN:

                key = pygame.key.get_pressed()

                if key[pygame.K_F1] or key[pygame.K_ESCAPE]:
                    game_paused = not game_paused
                    if game_paused:
                        game_chrono.freeze()
                        resume_button, option_button = create_game_pause(window)
                    else:
                        game_chrono.unfreeze()

                elif key[pygame.K_SPACE]:
                    tetrimino.hard_drop(data)

                elif key[pygame.K_DOWN]:
                    softdrop = True
                    data.fall_speed /= 20

                elif key[pygame.K_RIGHT]:
                    tetrimino.move_right(matrix)

                elif key[pygame.K_LEFT]:
                    tetrimino.move_left(matrix)

                elif key[pygame.K_UP] or key[pygame.K_x]:
                    tetrimino.turn_right(matrix)
                
                elif key[pygame.K_w]:
                    tetrimino.turn_left(matrix)

                elif event.key == pygame.K_c or (event.mod and pygame.KMOD_SHIFT):
                    if hold_queue.can_hold:
                        temp = hold_queue.get_t_type()
                        hold_queue.hold(tetrimino)
                        # dans le cas où la hold queue n'est pas vide
                        if temp:
                            tetrimino.set_type(temp)
                            tetrimino.set_y(0)
                            tetrimino.find_lower_pos(matrix)
                        # si vide
                        else:
                            # création d'un nouveau tetrimino
                            tetrimino = Tetrimino(bag, matrix)
                            next_queue.update(bag)
        if game_paused:
            if resume_button.is_pressed(event):
                game_chrono.unfreeze()
                game_paused = False

        else:
            # phase précédant le lock down
            if tetrimino.state == 1:
                # permet de jouer sur la couleur du tetrimino
                values = tetrimino.lock_phase(matrix, lock_down_chrono,
                                              lock_phase_first, shade_phase)
                lock_phase_first, shade_phase = values
                display_all(window, game_object)
                time.sleep(0.015)

            # phase lock down
            elif tetrimino.state == 2:
                # le tetrimino est lock dans matrix
                proceed['state'] = tetrimino.__lock_on_matrix__(matrix)
                # clear les lines s'il y a
                matrix.check_clear_lines(data)
                if matrix.is_game_won():
                    proceed['state'] = False
                    proceed['type'] = 'win'
                # le tetrimino suivant est créé
                tetrimino = Tetrimino(bag, matrix)
                next_queue.update(bag)
                hold_queue.allow_hold()
                display_all(window, game_object)
                # le chronomètre est raffraîchi
                time_before_refresh.reset()

            # dans le cas où le tetrimino est en falling phase
            else:
                # dans le cas où le joueur souhaite faire un softdrop
                # spécifié par le fait que la touche flèche bas est
                # maintenue pressée
                if time_before_refresh == data.fall_speed:
                    # score incrémenté de 1 lorsque le tetrimino peut tomber
                    if tetrimino.fall(matrix) and softdrop:
                        data.score_increase(1)
                    # on reinitialise le chrono
                    time_before_refresh.reset()
                # reaffichage de l'écran
                display_all(window, game_object)
            display_game_data(window, data, game_chrono)

    insert_local_score(data.values['score'])
    game_screen, screenshot = get_game_picture(window)
    game_data = {'score': data.values['score'],
                 'time': game_chrono.get_chrono_value(),
                 'lines': data.values['lines'],
                 'mode': data.values['game_mode'],
                 'issue': proceed['type']}
    return game_data, game_screen, screenshot
