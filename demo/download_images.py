import json, random, requests, os, sys, time

min_side = 256
random.seed(sys.argv[1] if len(sys.argv) > 1 else 1)
output_path = 'guardian_images'

print('loading JSON...')
data = json.load(open('guardian_images_list.json'))
print('end.\n')

randperm = range(0, len(data))
random.shuffle(randperm)

for (ii, index) in enumerate(randperm):
	print(index)
	img = data[index]
	url = img['urlTemplate']
	if 'width' in img:
		fixed_width = min_side if img['width'] < img['height'] else \
								  min_side * img['width'] / img['height']
		url = url.replace('#{width}', '%d' % fixed_width )
	
	identifier = '%07d' % img['id']
	image_path = '%s/%s' % (output_path, identifier[:4])
	
	image_fullpath = '%s/%s.jpg' % (image_path, identifier[4:])
	if not os.path.exists(image_fullpath):
		print(url)
		if not os.path.exists(image_path):
			os.mkdir(image_path)
		response = requests.get(url, timeout = None)
		fp = file(image_fullpath, 'wb')
		fp.write(response.content)
		time.sleep(0.3)
