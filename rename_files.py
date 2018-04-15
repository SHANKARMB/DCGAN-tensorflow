import os
import shutil
import json

rootDir = '/home/prime/ProjectWork/training/dataset'
current_dataset = 'sketchy/images and sketches mapped/256x256/photo/tx_000000000000'

final_dir = os.path.join(rootDir, 'gan_files')
os.chdir(rootDir)
folder_count = 0
labels = []
for sub_dir in os.listdir(current_dataset):
    # print(os.path.join(rootDir,current_dataset,sub_dir))
    # if os.path.isdir(os.path.join(rootDir,sub_dir)):
    # print('in ', sub_dir)
    folder_count = folder_count + 1
    os.makedirs(os.path.join(final_dir, 'images'), exist_ok=True)

    count = 0
    for filename in os.listdir(os.path.join(rootDir, current_dataset, sub_dir)):
        # print(filename)
        initial_img = os.path.join(rootDir, current_dataset, sub_dir, filename)
        final_filename = str(folder_count) + '_' + str(count) + '.jpg'
        final_img = os.path.join(final_dir, 'images', final_filename)
        shutil.copy(initial_img, final_img)
        count = count + 1

    print({'index': folder_count,
           'name': sub_dir,
           'count': count
           })

    labels.append({'index': folder_count,
                   'name': sub_dir,
                   'count': count
                   })

# print(labels)
# for i in labels:
#     print(i)

with open(os.path.join(final_dir, 'labels.txt'), 'w') as outfile:
    dump = json.dumps(labels)
    outfile.write(dump)
