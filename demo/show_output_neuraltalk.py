import json, csv

print('loading JSON...')
data = json.load(open('neuraltalk2/vis/vis.json'))
print('end.\n')

print('loading JSON...')
data_all = json.load(open('guardian_images_list.json'))
print('end.\n')


f = open('samples/samples.html', 'w')
f.write('<html><head></head><body>')
for entry in data:
	imgid = entry['file_name'][-11:]
	caption = entry['caption']
	gt = str(data_all[int(imgid[:-4])]['cleanCaption'].encode('utf-8'))
	print(gt)
	f.write('<div><img src="%s"/><br/>neuraltalk:%s<br/>gt:%s</div>' % (imgid, caption, gt.decode('ascii', 'ignore')))		

f.write('</body></html>')
f.close()

