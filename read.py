#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2.pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display rgb stream.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", type=str,required=True, help="Path to the bag file")
parser.add_argument("-j", "--jpg", type=bool, help="Export as sequence of images")
parser.add_argument("-r", "--rotate", type=int, help="Rotate the file")
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()

jpeg_path = ""
photo_id = 0
if args.jpg:
    # Save a sequence of photos
    jpeg_path = './' + args.input[:-4]
    if not os.path.exists(jpeg_path):
        os.makedirs(jpeg_path)

resolution = None
recorder = None
try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, args.input)

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    config.enable_stream(rs.stream.color, rs.format.rgb8, 30)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    cv2.namedWindow("RGB Stream", cv2.WINDOW_AUTOSIZE)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_filename = args.input[:-4] + ".mp4"
    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get depth frame
        image = frames.get_color_frame()
        image = np.asanyarray(image.get_data())
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if args.rotate:
            image = np.rot90(image,int(args.rotate))
        # Render image in opencv window
        cv2.imshow("Image Stream", image)
        if not resolution: resolution = image.shape
        if not recorder: recorder = cv2.VideoWriter(video_filename, fourcc, 30, (resolution[1], resolution[0]))
        recorder.write(image)
        if args.jpg:
            cv2.imwrite(jpeg_path +'/'+args.input[:-4] + "_" + str(photo_id) + ".jpg",image)
            photo_id = photo_id + 1
        key=cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            break

finally:
    pass
