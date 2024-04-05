import pyxel
import random

class enemy:
    def __init__(self):
        self.x = random.randint(0, pyxel.width - 8)
        self.y = 0
        self.type = random.choice([0,1])
        if(self.type==0):
            self.x_speed = 0
            self.y_speed = random.randrange(1, 3)
        else:
            self.x_speed = random.randrange(-1, 2)
            self.y_speed = random.randrange(1, 3)

class BalloonGame:
    def __init__(self):
        pyxel.init(160, 320, title="Balloon Game")
        pyxel.load("baloon.pyxres")
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.balloon_x = 80
        self.balloon_x_v = 0
        self.balloon_y = 260
        self.balloon_y_v = 0
        self.fuel = 100
        self.targets = []
        self.score = 0
        self.game_over = False
        self.game_clear = False

    def update(self):
        if self.game_over or self.game_clear:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return
        
        self.move_balloon()
        self.update_targets()
        self.check_collision()

    def move_balloon(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.balloon_x_v = max(self.balloon_x_v - 0.2, -1)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.balloon_x_v = min(self.balloon_x_v + 0.2, 1)
        if pyxel.btn(pyxel.KEY_SPACE) and self.balloon_y > 0:
            self.balloon_y -= 0.5
            self.balloon_y_v = 0
        else:
            self.balloon_y += self.balloon_y_v
            self.balloon_y_v += 0.2

        self.balloon_x += self.balloon_x_v
        if(self.balloon_x < 0):
            self.balloon_x = 0
        elif(self.balloon_x > pyxel.width - 8):
            self.balloon_x = pyxel.width - 8

    def update_targets(self):
        if random.randint(0, 20) == 0:
            e = enemy()
            self.targets.append(e)
        
        for target in self.targets:
            target.x += target.x_speed
            target.y += target.y_speed
            if target.x > pyxel.height:
                self.targets.remove(target)
                self.score += 1

    def check_collision(self):
        for target in self.targets:
            if (self.balloon_x < target.x + 8 and
                self.balloon_x + 8 > target.x and
                self.balloon_y < target.y + 8 and
                self.balloon_y + 8 > target.y):
                self.game_over = True
        if(self.balloon_y > pyxel.height - 8):
            self.game_over = True
        if(self.balloon_y < 0):
            self.game_clear = True

    def draw(self):
        pyxel.cls(12) #画面をシアン(空の色)で塗りつぶす
        pyxel.blt(x=self.balloon_x, y=self.balloon_y, img=0, u=0, v=0, w=18, h=18, colkey=0) #バルーンを描画

        for target in self.targets:
            if(target.type == 0):
                pyxel.blt(x=target.x, y=target.y, img=1, u=0, v=0, w=18, h=18, colkey=0)
            else:
                pyxel.blt(x=target.x, y=target.y, img=2, u=0, v=0, w=15, h=15, colkey=0)

        pyxel.text(5, 5, f"Score: {self.score}", 7)

        if self.game_over:
            pyxel.text(50, 60, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(43, 70, "Press R to Retry", 8)

        if self.game_clear:
            pyxel.text(50, 60, "GAME CLEAR", pyxel.frame_count % 4)
            pyxel.text(43, 70, "Press R to Retry", 0)

if __name__ == "__main__":
    BalloonGame()
