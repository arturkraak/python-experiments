# OLD BULLET SPEED
# if target[0] >= pos[0]:
#     dir_x = 1
#     dist_x = target[0] - pos[0]
# else:
#     dir_x = -1
#     dist_x = pos[0] - target[0]
#
# if target[1] >= pos[1]:
#     dir_y = 1
#     dist_y = target[1] - pos[1]
# else:
#     dir_y = -1
#     dist_y = pos[1] - target[1]
# self.speed_x = dir_x * (dist_x / (dist_x + dist_y) * bullet_speed)
# self.speed_y = dir_y * (dist_y / (dist_x + dist_y) * bullet_speed)
# print(f"{self.speed_x}")             

# OLD BULLET COLLISION
#self.old = (self.x, self.y)
#bullets.remove(self)
# self.x -= self.speed_x
# self.y -= self.speed_y
#
# if self.y > HEIGHT:
#     out_y = HEIGHT - self.y - 1
#     out_x = (out_y / self.speed_y) * self.speed_x
# if self.y < 0: 
#     out_y = 0 - self.y
#     out_x = (out_y / self.speed_y) * self.speed_x
# if self.x > WIDTH:
#     out_x = WIDTH - self.x -1
#     out_y = (out_x / self.speed_x) * self.speed_y
# if self.x < 0: 
#     out_x = 0 - self.x
#     out_y = (out_x / self.speed_x) * self.speed_y
#
# if out_x < out_y:
#     out_y = (out_x / self.speed_x) * self.speed_y
# else:
#     out_x = (out_y / self.speed_y) * self.speed_x
# if self.old[0] > WIDTH / 2 and self.~old[1] < HEIGHT / 2:
#     out_x = out_x
#     out_y = out_y
#     self.old = (self.old[0]+out_x, self.old[1]+out_y)
# else:
# self.old = (self.old[0]+out_x, self.old[1]+out_y)

# if self.x > enemy.rect.x and self.x < enemy.rect.x + enemy.rect.width:
#     self.is_moving = False

# OLD DRAW GUN
# pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), ((pygame.mouse.get_pos()[0], (pygame.mouse.get_pos()[1]))))