import cv2
import os

def video_to_images(video_path, output_folder):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Read frames from the video and save them as images
    frame_count = 0
    while True:
        # Read the next frame
        ret, frame = video.read()
        
        # If the frame was not successfully read, then we have reached the end of the video
        if not ret:
            break
        
        # Save the frame as an image
        image_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(image_path, frame)
        
        # Increment the frame count
        frame_count += 1
    
    # Release the video file
    video.release()

# Example usage
video_path = "/scratch/jin7/datasets/RobotData/ActualCameraPosition/JustRobot.mp4"
output_folder = "/scratch/jin7/datasets/RobotData/ActualCameraPosition/JointOutputPhotos"
video_to_images(video_path, output_folder)