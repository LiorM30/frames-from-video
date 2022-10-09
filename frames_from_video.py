import cv2
import zipfile
import os
import argparse
import time


IMAGE_FORMATS = ['png', 'jpeg', 'jpg']


def extract_frames(vid_path: str, out_path: str, out_name: str,
                   fps: float, no_zip: bool, img_format: str):
    start = time.time()
    vidcap = cv2.VideoCapture(vid_path)

    # if the fps is larger than the video fps
    # it should use the video fps
    if fps is None or fps >= vidcap.get(cv2.CAP_PROP_FPS):
        fps = vidcap.get(cv2.CAP_PROP_FPS)

    if no_zip:
        with zipfile.ZipFile(out_path + f'\\{out_name}.zip',
                             'w', zipfile.ZIP_DEFLATED) as file:
            count = 0
            success, frame = vidcap.read()
            while success:
                # set the time to match the next frame
                vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000*(1/fps)))
                # read image from buffer
                retval, buf = cv2.imencode(f'.{img_format}', frame)
                file.writestr(str(count) + f'.{img_format}', buf)
                success, frame = vidcap.read()
                count += 1
    else:
        dir_path = os.path.join(out_path, out_name)
        os.mkdir(dir_path)
        count = 0
        success, image = vidcap.read()
        while success:
            # set the time to match the next frame
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000*(1/fps)))
            cv2.imwrite(dir_path + f'\\{count}.{img_format}', image)
            success, image = vidcap.read()
            count += 1

    print(f'finished in {time.time() - start} seconds')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--video-path', action='store', type=str, required=True,
        help='path to video'
    )
    parser.add_argument(
        '-o', '--output-path', action='store', type=str, default=os.getcwd(),
        help='path to output folder'
    )
    parser.add_argument(
        '-n', '--output-name', action='store', type=str, default='frames',
        help='name of the frames folder'
    )
    parser.add_argument(
        '-nz', '--no-zip', action='store_true',
        help='whether to output the folder as zip'
    )
    parser.add_argument(
        '--fps', action='store', type=float, default=None,
        help='the number of frames to extract per sec, default is for each frame'  # noqa
    )
    parser.add_argument(
        '-f', '--format', action='store', type=str, default='jpg',
        help='the format of the output frames (png, jpg, jpeg)'
    )

    args = parser.parse_args()

    if not os.path.exists(args.video_path):
        raise "Video Path Doesn\'t Exist"
    if os.path.isdir(os.path.join(args.output_path, args.output_name)) or \
            os.path.exists(os.path.join(args.output_path, args.output_name, '.zip')):  # noqa
        raise "Output Folder Already Exists"
    if args.format not in IMAGE_FORMATS:
        raise "Output Format Must Be a Real Image Format (png, jpg, jpeg)"
    if args.fps is not None and args.fps <= 0:
        raise "fps Must Be a Non Zero Positive Number"

    extract_frames(vid_path=args.video_path, out_path=args.output_path,
                   out_name=args.output_name, fps=args.fps, no_zip=args.no_zip,
                   img_format=args.format)


if __name__ == "__main__":
    main()
