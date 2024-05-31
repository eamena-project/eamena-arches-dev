def img_fetch(url, label, uuid, number, new_width=300):
	"""
	Function to fetch, resize images and add text
	"""
	import requests
	from PIL import Image, ImageDraw, ImageFont	
	from io import BytesIO

	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	
	# Calculate new height to maintain aspect ratio
	width_percent = (new_width / float(img.size[0]))
	new_height = int((float(img.size[1]) * float(width_percent)))
	img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
	
	# Create a new image with extra space for text
	total_height = new_height + 40  # Adjust for label and uuid text
	new_img = Image.new('RGB', (new_width, total_height), (255, 255, 255))
	new_img.paste(img, (0, 20))
	
	# Add label, UUID, and number
	draw = ImageDraw.Draw(new_img)
	font = ImageFont.load_default()
	draw.text((10, 0), label, fill="black", font=font)
	draw.text((10, new_height + 25), uuid, fill="black", font=font)
	draw.text((10, 20), str(number), fill="black", font=font)  # Number in top left corner
	
	return new_img

def img_grid(df = None, cases_img_path = "https://raw.githubusercontent.com/eamena-project/eamena-data/main/reference-data/concepts/heritage_places/cases/img/", width = 300, num_columns = 3, padding = 3):
	"""
	Create an image grid of n columns gathering photographs illustrating EAMEAN concepts (ex: Threat type = Vandalism)

	:param df: a Pandas dataframe with the name of the images, their UUID, etc.
	:param cases_img_path: the root path of the folder structure where the images are hosted
	:param width: the width of each image (in px).
	:param num_columns: the number of columns of the image grid.
	:param padding: the padding.

	:return: A PIL.Image

	:Example: 
	>> list_path = 'https://raw.githubusercontent.com/eamena-project/eamena-data/main/reference-data/concepts/heritage_places/cases/list.tsv'
	>> df = pd.read_csv(list_path, sep='\t')
	>> grid_img = img_grid(df)
	>> grid_img.show()
	"""
	from PIL import Image

	df['image_path'] = cases_img_path + df['image']
	# Fetch images and resize widths, add incremental numbers
	images = [img_fetch(row['image_path'], row['label'], row['uuid'], index + 1) for index, row in df.iterrows()]
	# dimensions of the grid
	num_rows = (len(images) + num_columns - 1) // num_columns
	# Adjust grid height calculation to accommodate variable heights
	row_heights = [max(images[i * num_columns:(i + 1) * num_columns], key=lambda img: img.size[1]).size[1] for i in range(num_rows)]
	grid_height = sum(row_heights) + (num_rows - 1) * padding
	grid_width = num_columns * width + (num_columns - 1) * padding
	# image grid
	grid_img = Image.new('RGB', (grid_width, grid_height), (255, 255, 255))
	# Paste images into the grid
	y_offset = 0
	for row in range(num_rows):
		x_offset = 0
		row_images = images[row * num_columns:(row + 1) * num_columns]
		max_height = max(img.size[1] for img in row_images)
		for image in row_images:
			grid_img.paste(image, (x_offset, y_offset))
			x_offset += image.size[0] + padding
		y_offset += max_height + padding
	# grid_img.save('image_grid.jpg')
	return(grid_img)