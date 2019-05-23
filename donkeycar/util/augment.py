"""
Script to augment teaching data

Usage:
    augment.py --path=<source-dir> [--out=<target_dir>] --aug=<name> [--prob=<PROBABILITY>] [--add-prefix] [--start-id=<id>]

Options:
    -h --help           Show this screen.
    --path TUBPATH      Path of the record directory
    --out TARGETPATH    Path to directory where augmented data is placed, directory is created if it doesn't exist
                        If omitted path (source directory) will be used
    --aug NAME          Augmentation type. Possible values: shadow, bright, flip
    --prob PROBABILITY  Probability for augmentation to take in place. Can be used to apply augmentation to only
                        part
                        Value can be [0.0, 1.0]. Default value is 1.0 (all images will be augmented)
    --add-prefix        Add the name of augmentation to both augmented images and records
    --start-id id       The id number that the first augmented record will use. If not set, script will check the
                        highest number found in target path (out) and use next value. If target directory
                        does not contain records, use 1 instead.
"""

from docopt import docopt
import os
import numpy as np
import cv2
import glob
import shutil
import json
import re

IMAGE_KEY = 'cam/image_array'
IMAGE_POSTFIX = '_cam-image_array_.jpg'
RECORD_PREFIX = 'record_'


def load_image(source_path, record):
    filename = record[IMAGE_KEY]
    return cv2.imread('%s/%s' % (source_path, filename))


def store_image(name, img, record, target_path, target_id, add_prefix):
    prefix = ''
    if add_prefix:
        prefix = '_' + name
    new_filename = '%s%s%s' % (target_id, prefix, IMAGE_POSTFIX)
    cv2.imwrite('%s/%s' % (target_path, new_filename), img)
    record[IMAGE_KEY] = new_filename
    return record


def augment_brightness(record, source_path, target_path, target_id, add_prefix):
    img = load_image(source_path, record)
    # convert image to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    brightness = np.random.uniform(0.5, 1.5)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness, 0, 255)

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # write file to target, add it to record and return the record
    return store_image('bright', img, record, target_path, target_id, add_prefix)


def augment_flip(record, source_path, target_path, target_id, add_prefix):
    # Read filename and image
    img = load_image(source_path, record)

    img = cv2.flip(img, 1)

    flippable_keys = [
        'user/angle',
    ]

    for key in flippable_keys:
        record[key] = 0 - record[key]

    # write file to target, add it to record and return the record
    return store_image('flip', img, record, target_path, target_id, add_prefix)


def augment_shadow(record, source_path, target_path, target_id, add_prefix):
    # Load image
    img = load_image(source_path, record)

    top_y = 320 * np.random.uniform()
    top_x = 0
    bot_x = 160
    bot_y = 320 * np.random.uniform()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    shadow_mask = 0 * hsv[:, :, 2]
    X_m = np.mgrid[0:img.shape[0], 0:img.shape[1]][0]
    Y_m = np.mgrid[0:img.shape[0], 0:img.shape[1]][1]

    shadow_mask[((X_m - top_x) * (bot_y - top_y) - (bot_x - top_x) * (Y_m - top_y) >= 0)] = 1

    shadow_density = .5
    left_side = shadow_mask == 1
    right_side = shadow_mask == 0

    if np.random.randint(2) == 1:
        hsv[:, :, 2][left_side] = hsv[:, :, 2][left_side] * shadow_density
    else:
        hsv[:, :, 2][right_side] = hsv[:, :, 2][right_side] * shadow_density

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return store_image('shadow', img, record, target_path, target_id, add_prefix)


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def print_progress(count, total, name='', bar_length=20):
    if count % 10 == 0 or count == total:
        percent = 100 * (count / total)
        filled_length = int(bar_length * count / total)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        print('\r  %s\t |%s| %.1f%% %s' % (name, bar, percent, 'done'), end='\r')
    if count == total:
        print()


def add_to_filename(str, name):
    pos = str.rfind('_')
    return '%s_%s_%s' % (str[:pos], name, str[pos + 1:])


def get_record_count(source):
    length = len([name for name in os.listdir(source)
                  if os.path.isfile(os.path.join(source, name))
                  and name.startswith('record')])
    return length


def get_highest_id(target):
    records = glob.glob('%s/record*.json' % target)
    records = ((int(re.search('.+_(\d+).json', path).group(1)), path) for path in records)
    last_id = 0
    for _, record in sorted(records):
        last_id = _
    return last_id


def augment(source, target, name, augment_fn, probability=1.0, start_id = None, add_prefix=False):
    if not target:
        target = source

    ensure_directory(target)

    if source != target:
        shutil.copy('%s/meta.json' % source, target)

    count = 0
    total = get_record_count(source)

    if not start_id:
        last_id = get_highest_id(target)
        start_id = last_id + 1
    else:
        start_id = int(start_id)

    if total == 0:
        print('No records found')
        return

    prefix = ''
    if add_prefix:
        prefix = name + '_'

    record_paths = glob.glob('%s/record*.json' % source)
    for record_path in record_paths:
        with open(record_path, 'r') as record_file:
            if np.random.rand() <= probability:
                record_json = json.load(record_file)
                record_json = augment_fn(record_json, source, target, start_id + count, add_prefix)
                new_name = '%s%s%s.json' % (prefix, RECORD_PREFIX, start_id + count)
                f = open('%s/%s' % (target, new_name), "w")
                f.write(json.dumps(record_json))
                f.close()
        count = count + 1
        print_progress(count, total, name)


if __name__ == '__main__':
    args = docopt(__doc__)

    source = args['--path']
    target = args['--out']
    augmentation = args['--aug']
    probability = args['--prob']
    add_prefix = args['--add-prefix']
    start_id = args['--start-id']

    if probability is None:
        probability = 1.0
    else:
        probability = float(probability)

    augment_fn = None

    if augmentation == 'shadow':
        augment_fn = augment_shadow
    elif augmentation == 'bright':
        augment_fn = augment_brightness
    elif augmentation == 'flip':
        augment_fn = augment_flip
    else:
        print('Augmentation method not found')

    augment(source, target, augmentation, augment_fn, probability, start_id, add_prefix)
