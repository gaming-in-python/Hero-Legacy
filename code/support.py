from csv import reader
from os import walk
import pygame

#csv file to list
def import_csv_layout(path) :
	terrain_map = []
	# open csv file, use reader to read values
	with open(path) as level_map:
		layout = reader(level_map, delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		#terrain_map = all rows of the csv file as a list
		return terrain_map

#go through a folder, import all images as a list of surfaces
def import_folder(path) :
	surface_list = []
	for _, __, img_files in walk(path) :
		for image in img_files :
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)
	return surface_list
