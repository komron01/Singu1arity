import base64

def base64_to_image(input_file, output_file):
    try:
        # Read base64-encoded string from the input file
        with open(input_file, 'r') as file:
            base64_string = file.read()

        # Decode base64 string to bytes
        image_bytes = base64.b64decode(base64_string)

        # Save the image bytes to an output file
        with open(output_file, 'wb') as image_file:
            image_file.write(image_bytes)

        print(f"Image successfully saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Specify the input and output file paths
input_file_path = 'encoded_image.txt'  # Change this to your input file
output_file_path = 'output_image.jpg'  # Change this to your desired output file

# Convert base64 to image
base64_to_image(input_file_path, output_file_path)
