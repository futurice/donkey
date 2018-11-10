#!/usr/bin/env python3
"""
Cross validator

Usage:
    crossvalidator.py  (--model=<model>) [--tub=<tub1,tub2,..tubn>] [--type=(linear|categorical)] [--output=<csv-filename>]

Options:
    -h --help        Show this screen.
    --tub TUBPATHS   List of paths to tubs. Comma separated. Use quotes to use wildcards. ie "~/tubs/*"
    --type TYPE          Either categorical or linear  [default: 'linear']
    --output CSVFILE      Csv filename
"""
import os
from docopt import docopt

import math
import donkeycar as dk
import statistics
import numpy as np
import csv
from donkeycar.parts.keras import KerasCategorical, KerasLinear
from donkeycar.parts.datastore import TubGroup


def print_mean(l, message):
    mean = statistics.mean(l)
    stdev = statistics.stdev(l)
    print(message, " mean: ", mean, " and standard dev: ", stdev)

def print_lse(correct, estimates, message):
    print(message, " lse: ", lse(correct, estimates))

def lse(correct, estimates):
    sum = 0.0
    for index in range(len(correct)):
        c = correct[index]
        e = estimates[index]
        sum += math.pow(c - e, 2)
    return sum / len(correct)


def validate(cfg, model_path=None, tub_names=None, model_type='linear', output=None):
    print("Using a model of type: ", model_type)
    if model_type == "categorical":
        kl = KerasCategorical()
    elif model_type == "linear":
        kl = KerasLinear(cfg)

    if model_path:
        kl.load(model_path)

    print('tub_names', tub_names)
    tubgroup = TubGroup(tub_names)

    # See Also: ShowPredictionPlots

    if not output:
        output = model_path + ".validator.csv"

    print('saving to output file: ', output)
    with open(output, 'w') as csvfile:
        w = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Angle', 'Angle estimate', 'Angle error', 'Throttle', 'Throttle estimate', 'Throttle error'])
        for tub in tubgroup.tubs:
            num_records = tub.get_num_records()
            print('cross validation set size: %d' % num_records)

            correct_angles = []
            correct_throttles = []
            estimate_angles = []
            estimate_throttles = []

            error_angles = []
            error_throttles = []

            for iRec in tub.get_index(shuffled=False):
                record = tub.get_record(iRec)

                img = record["cam/image_array"]
                user_angle = float(record["user/angle"])
                user_throttle = float(record["user/throttle"])
                pilot_angle, pilot_throttle = kl.run(img)

                correct_angles.append(user_angle)
                correct_throttles.append(user_throttle)
                estimate_angles.append(pilot_angle.item())
                estimate_throttles.append(pilot_throttle.item())

                error_angle = user_angle - pilot_angle.item()
                error_angles.append(error_angle)
                error_throttle = user_throttle - pilot_throttle.item()
                error_throttles.append(error_throttle)

                w.writerow([user_angle, pilot_angle, error_angle, user_throttle, pilot_throttle, error_throttle])

            print_mean(correct_angles, "Correct angle")
            print_mean(estimate_angles, "Estimate angle")

            print_mean(correct_throttles, "Correct throttle")
            print_mean(estimate_throttles, "Estimate throttle")

            print_mean(error_angles, "Error angle")
            print_mean(error_throttles, "Error throttle")

            print_lse(correct_angles, estimate_angles, "Angle LSE")
            print_lse(correct_throttles, estimate_throttles, "Throttle LSE")

if __name__ == '__main__':
    args = docopt(__doc__)
    cfg = dk.load_config()
    validate(cfg, model_path=args['--model'], tub_names=args['--tub'], model_type=args['--type'], output=args['--output'])
