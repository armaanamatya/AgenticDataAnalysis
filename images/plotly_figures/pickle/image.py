import pickle
import os
import plotly.io as pio

# Define the absolute path
pickle_dir = r'C:\Users\armaa\OneDrive\Desktop\ADAAS\AgenticDataAnalysis\images\plotly_figures\pickle'

# List all pickle files in the directory
pickle_files = [f for f in os.listdir(pickle_dir) if f.endswith('.pickle')]

# Open and load each pickle file
for file in pickle_files:
    try:
        # Use os.path.join for proper path handling
        pickle_path = os.path.join(pickle_dir, file)
        with open(pickle_path, 'rb') as pkl:
            fig = pickle.load(pkl)
            
            # Save Plotly figure as PNG
            output_path = os.path.join(pickle_dir, file.replace('.pickle', '.png'))
            pio.write_image(fig, output_path)
            
            print(f"Converted {file} to PNG successfully")
            
    except Exception as e:
        print(f"Error processing {file}: {str(e)}")

# Close any remaining figures
#plt.close('all')