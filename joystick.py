from sense_hat import SenseHat
sense = SenseHat()

green = (0, 255, 0) #green
yellow = (255, 255, 0) #yellow
red = (255, 0, 0) #red

sense.clear()
sense.set_pixel(0, 0, 0, 255, 0)

while True:

  for event in sense.stick.get_events():
    # Check if the joystick was pressed
    if event.action == "pressed":
      # Check which direction
      if event.direction == "up":
        print("Up")
        sense.clear(green)      # Up arrow

      elif event.direction == "up":
        sense.clear()

      elif event.direction == "down":
        print("Down")
        sense.clear(red)      # Down arrow

      elif event.direction == "right":
        print("Right")
        sense.clear(yellow)      # Right arrow

      elif event.direction == "left":
        print("left")
        sense.clear()
        sense.set_pixel(0, 0, 255, 0, 0)      # Left arrow
