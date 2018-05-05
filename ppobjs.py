import math as m

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
		self.len_car = .45 # static length of a car
		self.width_car = .3
		self.backaxle_midpt = Coordinate(
			self.b_down.x + (self.len_car / 5.0), 
			self.b_down.y + (self.width_car / 2.0)
			)
		self.frontaxle_midpt = Coordinate(
			self.f_down.x - (self.len_car / 5.0), 
			self.f_down.y + (self.width_car / 2.0)
			)
		

	def genGraphPts(self):
		return [
		[self.f_up.x, self.f_down.x, self.b_up.x, self.b_down.x, self.backaxle_midpt.x, self.frontaxle_midpt.x],
		[self.f_up.y, self.f_down.y, self.b_up.y, self.b_down.y, self.backaxle_midpt.y, self.frontaxle_midpt.y] ]
	
	def updateFrontBackAxle(self):
		self.backaxle_midpt.x = self.b_down.x + (self.len_car / 5.0)
		self.backaxle_midpt.y = self.b_down.y + (self.width_car / 2.0)
		self.frontaxle_midpt.x = self.f_down.x - (self.len_car / 5.0) 
		self.frontaxle_midpt.y = self.f_down.y + (self.width_car / 2.0)

	def set_fup(self, xvalue, yvalue):
		self.f_up.x = xvalue
		self.f_up.y = yvalue
		self.updateFrontBackAxle()

	def set_fdown(self, xvalue, yvalue):
		self.f_down.x = xvalue
		self.f_down.y = yvalue
		self.updateFrontBackAxle()

	def set_bup(self, xvalue, yvalue):
		self.b_up.x = xvalue
		self.b_up.y = yvalue
		self.updateFrontBackAxle()

	def set_bdown(self, xvalue, yvalue):
		self.b_down.x = xvalue
		self.b_down.y = yvalue
		self.updateFrontBackAxle()
