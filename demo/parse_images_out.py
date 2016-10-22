import json

nimages = 0
success = 0
counter = 0
images = list()
# Go over all news stories scrapped by Xuwang.
for line in open('guardian_json_files'):
	counter = counter + 1
	try:
		# Decode JSON entry for this news story.
		data = json.load(open(line.strip()))
		#print('\n%d. ' % counter)

		# Collect images from this news story.
		raw_images = list()
		raw_images = data['displayImages'] + data['bodyImages']
		if 'headerImage' in data and data['headerImage']:
			raw_images.append(data['headerImage'])
		
		# Deduplicate same images.
		unique_raw_images = dict()
		for raw_image in raw_images:
			unique_raw_images[raw_image['urlTemplate']] = raw_image
		raw_images = unique_raw_images.values()	

		# Go over each image entry.
		#print(data.keys())
		#print(data['id'])
		#print('\n')
		for raw_image in raw_images:
			if 'cleanCaption' in raw_image and raw_image['cleanCaption']:
				if 'width' not in raw_image or (raw_image['width'] > 255 and \
												raw_image['height'] > 255):
					raw_image['article_id'] = data['id']
					raw_image['id'] = nimages
					nimages = nimages + 1
					images.append(raw_image)	
				#print raw_image
				#print('\n')

		#if counter > 10000: break
		if len(raw_images) > 0:
			success = success + 1
		if counter % 1000 == 0:
			print('%d out of %d, total images = %d' % (success, counter, nimages))
	except ValueError:
		continue

json.dump(images, open('guardian_images_list.json', 'w'))



