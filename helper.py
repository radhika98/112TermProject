class Button(object): #Near-universal button class. 
#got template from https://github.com/blob/master/HelperWidgets.py
    def __init__(self, topleft, bottomright, text, color, outline, function, data, size=" 30"):
        self.text = text
        self.bg = color
        self.outline = outline
        self.callback = function
        self.topleft = topleft
        self.bottomright = bottomright
        self.state = "idle"
        self.data = data
        self.didClick = False
        self.size = size

    def handleClick(self, event): #If we clicked on the button, run the given function with data as an argument
        if (self.inBounds((event.x,event.y))):
            self.callback(self.data)

    def update(self, data): #If we're hovering over the button, change its color to show that
        self.state = "idle"
        if (self.inBounds((data.mouseX, data.mouseY))):
            self.state = "hover"

    def inBounds(self, pos): #Check if a given point is within the rectangle of the button
        if (pos[0] < self.topleft[0] or
            pos[0] > self.bottomright[0] or
            pos[1] < self.topleft[1] or
            pos[1] > self.bottomright[1]):
            return False
        return True

    def draw(self, canvas, data):
        if (self.state == "hover"): #If the mouse is hovering of this button, draw the bg with the same fill as outline
            canvas.create_rectangle(self.topleft, self.bottomright,
                fill=self.outline, outline=self.outline, width = 2)
        else: #Otherwise draw the bg normally
            canvas.create_rectangle(self.topleft, self.bottomright,
            fill=self.bg, outline=self.outline, width = 2)

        #All good buttons have names
        canvas.create_text((self.topleft[0]+self.bottomright[0])//2,
                            (self.topleft[1] + self.bottomright[1])//2,
                            text = self.text, fill="#ffffff",
                            font = self.size)