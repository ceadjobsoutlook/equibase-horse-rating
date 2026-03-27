import os
from rembg import remove
from PIL import Image

# 1. DEFINE PATHS (Assuming standard project structure)
# Ensure these folders exist on your computer
ASSETS_DIR = './assets'   # Put your white-background source images here
OUTPUT_DIR = './images'   # The script will put clean transparent PNGs here

def clean_horse_images():
    print("----------------------------------------")
    print("🏇 EQUINE BACKGROUND REMOVER Pipeline 🏇")
    print("----------------------------------------\n")

    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # List files in assets
    try:
        source_files = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    except FileNotFoundError:
        print(f"Error: Could not find '{ASSETS_DIR}' folder. Please create it and add your horse images.")
        return

    if not source_files:
        print(f"No source images found in '{ASSETS_DIR}'. Add some .png or .jpg files and run again.")
        return

    print(f"Found {len(source_files)} images to process...")

    count_success = 0
    count_fail = 0

    # Process each image
    for filename in source_files:
        input_path = os.path.join(ASSETS_DIR, filename)
        
        # We enforce .png for transparency in the output
        output_filename = os.path.splitext(filename)[0] + '.png'
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        print(f"  > Processing: '{filename}' ...", end="", flush=True)

        try:
            # 2. THE MACHINE LEARNING REMOVAL (THE CORE LOGIC)
            with open(input_path, 'rb') as i:
                input_data = i.read()
                # 'rembg' uses an ONNX model to segment the foreground subject (the horse)
                output_data = remove(input_data)
            
            # Save the result as a PNG
            with open(output_path, 'wb') as o:
                o.write(output_data)
            
            print(" SUCCESS (Transparent PNG saved)")
            count_success += 1

        except Exception as e:
            print(f" FAILED (Error: {e})")
            count_fail += 1

    print("\n----------------------------------------")
    print(f"COMPLETE! Validated {count_success} clean images available in '{OUTPUT_DIR}'.")
    if count_fail > 0:
        print(f"Warning: {count_fail} images failed processing.")
    print("----------------------------------------\n")
    print("Next Steps:")
    print("1. Update 'races.json' in the main folder")
    print("2. Commit './images/*' to GitHub and push to Vercel!")

if __name__ == "__main__":
    clean_horse_images()