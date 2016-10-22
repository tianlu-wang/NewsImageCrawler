import json, csv
from whoosh import index
from whoosh.fields import Schema, ID, STORED, TEXT
from whoosh.analysis import StemmingAnalyzer

print('loading JSON...')
data = json.load(open('guardian_images_list.json'))
print('end.\n')

schema = Schema(key=ID(unique=True, stored=True),
                uid = STORED, name = STORED,
                description=TEXT(stored=True, analyzer=StemmingAnalyzer()))
ix = index.create_in('guardian_index', schema)

count = 0
ix = index.open_dir('guardian_index')
writer = ix.writer()
for img in data: 
	key = '%07d' % img['id']
	uid = img['urlTemplate'].encode('utf-8')
	name = key
	description = img['cleanCaption'].encode('utf-8')
	writer.add_document(key = key.decode('utf-8', 'ignore'),
						uid = uid.decode('utf-8'),
						name = key.decode('utf-8'),
						description = description.decode('utf-8'))#description.decode('utf-8', 'ignore'))
	count = count + 1
	if count % 1000 == 0:
		print count

writer.commit()
ix.close()

