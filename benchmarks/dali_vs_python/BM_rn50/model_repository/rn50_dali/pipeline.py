# The MIT License (MIT)
#
# Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import nvidia.dali as dali
import nvidia.dali.types as types


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Serialize the pipeline and save it to a file")
    parser.add_argument('file_path', type=str,
                        help='The path where to save the serialized pipeline')
    return parser.parse_args()


def preprocessing(images):
    images = dali.fn.decoders.image(images, device='mixed', output_type=types.RGB)
    images = dali.fn.resize(images, resize_x=224, resize_y=224)
    return dali.fn.crop_mirror_normalize(images,
                                         dtype=types.FLOAT,
                                         output_layout="HWC",
                                         crop=(224, 224),
                                         mean=[0.485 * 255, 0.456 * 255, 0.406 * 255],
                                         std=[0.229 * 255, 0.224 * 255, 0.225 * 255])


@dali.pipeline_def(batch_size=1, num_threads=1, device_id=0)
def pipe():
    images = dali.fn.external_source(device='cpu', name="DALI_INPUT_0", no_copy=True)
    return preprocessing(images)


def main(filename):
    pipe().serialize(filename=filename)


if __name__ == '__main__':
    args = parse_args()
    main(args.file_path)
