from src.escape_room.gui_utilities import graphics
from src.escape_room.application.context_manager import ContextManager

class MetalCassette():
		def __init__(self, room_data, index, room_state):
			(x,y,z) = room_data["metal_cassette"][index][0] 
			self.shift_coordinates = (x-3.78,y-0.37,z-3.5)
			self.room_state = room_state

			self.metal_cassette_coordinates = [
				["#74797E",(3.78, 0.40, 3.50),(4.22, 0.40, 3.50),(4.22, 0.57, 3.50),(3.78, 0.57, 3.50)], # back side
				["#4F5458",(3.78, 0.40, 3.20),(3.78, 0.40, 3.50),(3.78, 0.57, 3.50),(3.78, 0.57, 3.20)], # left side
				["#5B6065",(4.22, 0.40, 3.20),(4.22, 0.57, 3.20),(4.22, 0.57, 3.50),(4.22, 0.40, 3.50)], # right side
				["#8A8F94",(3.78, 0.57, 3.20),(3.78, 0.57, 3.50),(4.22, 0.57, 3.50),(4.22, 0.57, 3.20)], # top side
				["#44484C",(3.78, 0.40, 3.20),(4.22, 0.40, 3.20),(4.22, 0.40, 3.50),(3.78, 0.40, 3.50)], # bottom
				["#6E7378",(3.78, 0.40, 3.20),(4.22, 0.40, 3.20),(4.22, 0.57, 3.20),(3.78, 0.57, 3.20)], # front side
				["#92979B",(3.82, 0.54, 3.195),(4.18, 0.54, 3.195),(4.18, 0.57, 3.195),(3.82, 0.57, 3.195)], # upper decoration
				["#555A5E",(3.82, 0.4, 3.195),(4.18, 0.4, 3.195),(4.18, 0.43, 3.195),(3.82, 0.43, 3.195)], # lower decoration
				["#292C2F",(3.99, 0.46, 3.19),(4.01, 0.46, 3.19),(4.01, 0.5, 3.19),(3.99, 0.5, 3.19)], # keyhole
			]
			self.metal_cassette_opened = [
				["#74797E",(3.78, 0.40, 3.50),(4.22, 0.40, 3.50),(4.22, 0.57, 3.50),(3.78, 0.57, 3.50)], # back side
				["#4F5458",(3.78, 0.40, 3.20),(3.78, 0.40, 3.50),(3.78, 0.57, 3.50),(3.78, 0.57, 3.20)], # left side
				["#5B6065",(4.22, 0.40, 3.20),(4.22, 0.57, 3.20),(4.22, 0.57, 3.50),(4.22, 0.40, 3.50)], # right side
				["#8A8F94",(3.78, 0.7, 3.25),(3.78, 0.57, 3.50),(4.22, 0.57, 3.50),(4.22, 0.7, 3.25)], # top side
				["#44484C",(3.78, 0.40, 3.20),(4.22, 0.40, 3.20),(4.22, 0.40, 3.50),(3.78, 0.40, 3.50)], # bottom
				["#6E7378",(3.78, 0.40, 3.20),(4.22, 0.40, 3.20),(4.22, 0.57, 3.20),(3.78, 0.57, 3.20)], # front side
				["#92979B",(3.82, 0.54, 3.195),(4.18, 0.54, 3.195),(4.18, 0.57, 3.195),(3.82, 0.57, 3.195)], # upper decoration
				["#555A5E",(3.82, 0.4, 3.195),(4.18, 0.4, 3.195),(4.18, 0.43, 3.195),(3.82, 0.43, 3.195)], # lower decoration
				["#292C2F",(3.99, 0.46, 3.19),(4.01, 0.46, 3.19),(4.01, 0.5, 3.19),(3.99, 0.5, 3.19)], # keyhole
			]

			included_diamond_id = room_data["metal_cassette"][index][2]       
			diamond_found=False
			# is some key included?
			if(included_diamond_id!=""):
				# try to find the key object via the ID
				for diamond in ContextManager().get_room().diamond:
					if diamond.unique_id == included_diamond_id:
						diamond_found=True
						break
			if not diamond_found:
				diamond=None
			self.diamond = diamond

		def draw(self, canvas, inventory, player_name):
			if self.room_state.get_state_object("fireplace","fireplace1") == "secret compartment opened":
				graphics.draw(canvas,self.metal_cassette_coordinates,object=self,tag="metal_cassette",shift_coordinates=self.shift_coordinates)
				canvas.tag_bind("metal_cassette","<Button-1>", lambda event: self.clicked(self, canvas, inventory, player_name))

		def clicked(event, self, canvas, inventory, player_name):
			if inventory.objectIsSelected("revolver", player_name) == True:
				graphics.draw(canvas,self.metal_cassette_opened,object=self,tag="metal_cassette",shift_coordinates=self.shift_coordinates)
				self.room_state.set_state_object("metal_cassette","metal_cassette1","opened")
				for diamond in ContextManager().get_room().diamond:
					diamond.draw(canvas)
				canvas.tag_raise("chair", "metal_cassette")
				canvas.tag_raise("letter", "chair")
				


				





