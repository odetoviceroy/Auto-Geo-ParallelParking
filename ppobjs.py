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
		self.axle_len = 0.0

	def genGraphPts(self):
		return [
		[self.f_up.x, self.f_down.x, self.b_up.x, self.b_down.x, self.backaxle_midpt.x, self.frontaxle_midpt.x],
		[self.f_up.y, self.f_down.y, self.b_up.y, self.b_down.y, self.backaxle_midpt.y, self.frontaxle_midpt.y] ]
	
	def updateFrontBackAxle(self):
		self.backaxle_midpt.x = self.b_down.x + (self.len_car / 5.0)
		self.backaxle_midpt.y = self.b_down.y + (self.width_car / 2.0)
		self.frontaxle_midpt.x = self.f_down.x - (self.len_car / 5.0) 
		self.frontaxle_midpt.y = self.f_down.y + (self.width_car / 2.0)
		self.axle_len = (self.frontaxle_midpt.x - self.backaxle_midpt.x) * (self.frontaxle_midpt.x - self.backaxle_midpt.x)
		self.axle_len = self.axle_len + (self.frontaxle_midpt.y - self.backaxle_midpt.y) * (self.frontaxle_midpt.y - self.backaxle_midpt.y)
		self.axle_len = m.sqrt(self.axle_len)

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

	def setOrientation(self,theta):
		self.f_down.x = self.b_down.x + self.len_car * m.cos(theta)
		self.f_up.x = self.b_up.x + self.len_car * m.cos(theta)
		self.f_down.y = self.b_down.y + self.len_car * m.sin(theta)
		self.f_up.y = self.b_up.y + self.len_car * m.sin(theta)
		bottom_midpoint = Coordinate( (self.b_up.x + self.b_down.x) / 2.0,
			(self.b_up.y  + self.b_down.y) / 2.0 )
		self.backaxle_midpt.x = bottom_midpoint.x + (self.len_car / 5.0) * m.cos(theta)
		self.backaxle_midpt.y = bottom_midpoint.y + (self.len_car / 5.0) * m.sin(theta)
		self.frontaxle_midpt.x = bottom_midpoint.x + 4 * (self.len_car / 5.0) * m.cos(theta)
		self.frontaxle_midpt.y = bottom_midpoint.y + 4* (self.len_car / 5.0) * m.sin(theta)
		return self
