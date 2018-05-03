class Coordinate:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Car:
	def __init__(self, front_up, front_down, back_up, back_down):
		self.f_up = front_up
		self.f_down = front_down
		self.b_up = back_up
		self.b_down = back_down
	def genGraphPts(self):
		return [
		[self.f_up.x, self.f_down.x, self.b_up.x, self.b_down.x],
		[self.f_up.y, self.f_down.y, self.b_up.y, self.b_down.y] ]
		