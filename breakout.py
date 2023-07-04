import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_GAMECLEAR = 3

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 4
PADDLE_COLOR = 7
PADDLE_SPEED = 2

BALL_RADIUS = 2
BALL_COLOR = 7
BALL_SPEED_X = 1  # 2
BALL_SPEED_Y = 1  # 2

BLOCK_WIDTH = 10
BLOCK_HEIGHT = 3
BLOCK_COLOR = 7
BLOCK_COUNT = 110

blocks = []


def draw_list(list):
    for elem in list:
        elem.draw()


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PADDLE_WIDTH
        self.h = PADDLE_HEIGHT

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.x -= PADDLE_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.x += PADDLE_SPEED
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, PADDLE_COLOR)


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = BALL_RADIUS
        self.speed_x = pyxel.rndf(-BALL_SPEED_X, BALL_SPEED_X)
        self.speed_y = BALL_SPEED_Y

    def update(self):
        if self.x - self.r <= 0 or pyxel.width <= self.x + self.r:
            self.speed_x = -self.speed_x
        if self.y - self.r <= 0:
            self.speed_y = -self.speed_y
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pyxel.circ(self.x, self.y, self.r, BALL_COLOR)


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BLOCK_WIDTH
        self.h = BLOCK_HEIGHT
        self.is_broken = False
        blocks.append(self)

    def draw(self):
        if self.is_broken == False:
            pyxel.rect(self.x, self.y, self.w, self.h, BLOCK_COLOR)


class App:
    def __init__(self):
        pyxel.init(120, 160, title="Breakout")
        self.scene = SCENE_TITLE
        self.score = 0
        self.paddle = Paddle((pyxel.width - PADDLE_WIDTH) /
                             2, pyxel.height - PADDLE_HEIGHT)
        self.ball = Ball(pyxel.width / 2, pyxel.height / 2)

        for i in range(BLOCK_COUNT):
            blocks.append(Block(i % 11 * (BLOCK_WIDTH + 1),
                                i // 11 * (BLOCK_HEIGHT + 1) + 13))

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
        elif self.scene == SCENE_GAMECLEAR:
            self.update_gameclear_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        if (
            self.paddle.x + self.paddle.w >= self.ball.x + self.ball.r
            and self.ball.x >= self.paddle.x
            and self.ball.y + self.ball.r >= self.paddle.y
        ):
            self.ball.speed_y = -self.ball.speed_y
        if self.ball.y + self.ball.r >= pyxel.height:
            self.ball.speed_y = -self.ball.speed_y
            # self.scene = SCENE_GAMEOVER
        if self.score == BLOCK_COUNT:
            self.scene = SCENE_GAMECLEAR

        for block in blocks:
            if block.is_broken == False:
                if (
                    block.x <= self.ball.x
                    and self.ball.x <= block.x + block.w
                    and block.y <= self.ball.y
                    and self.ball.y <= block.y + block.h
                ):
                    block.is_broken = True
                    self.score += 1
                    if (
                        block.x <= self.ball.x
                        and self.ball.x <= block.x + block.w
                    ):
                        self.ball.speed_y = -self.ball.speed_y
                    else:
                        self.ball.speed_x = -self.ball.speed_x

        self.paddle.update()
        self.ball.update()

        if pyxel.btnp(pyxel.KEY_O):
            self.scene = SCENE_GAMEOVER
        if pyxel.btnp(pyxel.KEY_C):
            self.scene = SCENE_GAMECLEAR

    def update_gameover_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.reset_game()
            self.scene = SCENE_TITLE

    def update_gameclear_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.reset_game()
            self.scene = SCENE_TITLE

    def reset_game(self):
        self.scene = SCENE_TITLE
        self.score = 0
        self.paddle = Paddle((pyxel.width - PADDLE_WIDTH) /
                             2, pyxel.height - PADDLE_HEIGHT)
        self.ball = Ball(pyxel.width / 2, pyxel.height / 2)
        self.ball.speed_x = pyxel.rndf(-BALL_SPEED_X, BALL_SPEED_X)
        self.ball.speed_y = BALL_SPEED_Y

        for i in range(BLOCK_COUNT):
            blocks.append(Block(i % 11 * (BLOCK_WIDTH + 1),
                                i // 11 * (BLOCK_HEIGHT + 1) + 13))

        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        elif self.scene == SCENE_GAMECLEAR:
            self.draw_gameclear_scene()
        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

    def draw_title_scene(self):
        pyxel.text(45, 66, "Breakout", pyxel.frame_count % 16)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        pyxel.text(47, 66, "PLAYING", pyxel.frame_count % 16)
        self.paddle.draw()
        self.ball.draw()
        draw_list(blocks)

    def draw_gameover_scene(self):
        pyxel.text(43, 66, "GAME OVER", 8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_gameclear_scene(self):
        pyxel.text(41, 66, "GAME CLEAR", 10)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)


App()
