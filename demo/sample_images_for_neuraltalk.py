import json, csv, random, shutil

print('loading JSON...')
data = json.load(open('guardian_images_list.json'))
print('end.\n')


captions = open('samples/captions.txt', 'w')
for i  in range(1, 500):
	sample = data[random.randint(1, len(data))]
	s = '%07d' % sample['id']
	caption = sample['cleanCaption'].encode('utf-8')
	captions.write('%d %s/%s.jpg %s\n' % (sample['id'], s[:4], s[4:], caption))
	shutil.copy('guardian_images/%s/%s.jpg' % (s[:4], s[4:]), 'samples/%s.jpg' % s)

captions.close()


