import os
import json
from PIL import Image

dataset_dir = "/home/jin7/Desktop/jin7/datasets/RobotData"
subdirs = ["ActualCameraPosition"]#, "Demo", "TrainingData1", "TrainingData2", 
           #"TrainingData3", "TrainingData4", "TrainingData5", "TrainingData6"]
data_dirs = [os.path.join(dataset_dir, subdir) for subdir in subdirs]
save_dir = os.path.join(dataset_dir, "ConvertedData")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

object_setting = {
    "exported_object_classes": ["uofsc"],
    "exported_objects": [
		{
			"class": "uofsc",
			"segmentation_class_id": 1,
			"segmentation_instance_id": 1,
			"fixed_model_transform": [
				[ 0, 0, -1, 0 ],
				[ 1, 0, 0, 0 ],
				[ 0, -1, 0, 0 ],
				[ 0, 0, 0, 1 ]
			],
			"cuboid_dimensions": [ 1.0, 1.0, 1.0 ]
		},
    ]
}

camera_setting = {
	"camera_settings": [
		{
			"id": "0",
			"name": "camera_0",
			"intrinsic_settings":
			{
				"fx": 320,
				"fy": 320,
				"cx": 320,
				"cy": 240,
				"s": 0,
				"hfov": 90,
				"resolution":
				{
					"width": 1920,
					"height": 1080
				}
			},
			"captured_image_size":
			{
				"width": 1920,
				"height": 1080
			}
		}
	]
}

def points2ann(points):
    # points are in format [x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6]
    x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6 = points
    ann = {
	"camera_data":
	{
		"location_worldframe": [0, 0, 0],
		"quaternion_xyzw_worldframe": [0, 0, 0, 1],
	},
	"objects": [
		{
			"class": "uofsc",
			"visibility": 1,
			"keypoints": [
				{
					"name": "joint1",
					"location": [],
					"projected_location": [ x1, y1 ]
				},
				{
					"name": "joint2",
					"location": [],
					"projected_location": [ x2, y2 ]
				},
				{
					"name": "joint3",
					"location": [],
					"projected_location": [ x3, y3 ]
				},
                {
                    "name": "joint4",
                    "location": [],
                    "projected_location": [ x4, y4 ]
                },
                {
                    "name": "joint5",
                    "location": [],
                    "projected_location": [ x5, y5 ]
                },
                {
                    "name": "joint6",
                    "location": [],
                    "projected_location": [ x6, y6 ]
                }
			]
		},
		],
    }
    return ann
    

# save object setting into a json file
with open(os.path.join(save_dir, "_object_settings.json"), 'w') as f:
    json.dump(object_setting, f, indent=4)

# save camera setting into a json file
with open(os.path.join(save_dir, "_camera_settings.json"), 'w') as f:
    json.dump(camera_setting, f, indent=4)

id = 0

for d in data_dirs:
    data_folder = os.path.join(d, "JointOutputPhotos")
    ann_csv = os.path.join(d, "JointOutput.csv")
    # read from the third line of the csv file, each line is one annotation for one image
    with open(ann_csv, 'r') as f:
        lines = f.readlines()[2:]
    images = os.listdir(data_folder)
    # image names are in frame_0.jpg format, sort them according to the frame number
    images = sorted(images, key=lambda x: int(x.split('_')[1].split('.')[0]))
    if len(lines) != len(images):
        print(f"Number of annotations and images do not match for {d}")
        print(f"Annotations: {len(lines)}, Images: {len(images)}")
        min_len = min(len(lines), len(images))
        lines = lines[:min_len]
        images = images[:min_len]
        print(f"Using the first {min_len} annotations and images")

    for i, (line, img) in enumerate(zip(lines, images)):
        # each line is in format '12.85,845, 576,877, 582,915, 263,907, 220,1009, 153,974, 168\n'
        # the first number is the timestamp, the rest are the coordinates of six joints
        line = line.strip().split(',')
        timestamp = line[0]
        joints = [int(x.strip()) for x in line[1:]]
        # save image name should be xxxxxx.rgb.jpg, where xxxxxx is the id
        # save annotation name should be xxxxxx.json
        img_name = f"{id:06d}.rgb.jpg"
        ann_name = f"{id:06d}.json"

        # save image
        img_path = os.path.join(data_folder, img)
        img = Image.open(img_path)
        img.save(os.path.join(save_dir, img_name))

        # save annotation
        ann = points2ann(joints)
        with open(os.path.join(save_dir, ann_name), 'w') as f:
            json.dump(ann, f, indent=4)
        
        id += 1
        