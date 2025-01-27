

   import numpy as np
   import os
   import struct

   # Configuration
   DATASET_ROOT = "data"  # Folder containing validation data
   PREDICTIONS_ROOT = "predictions"  # Folder containing prediction files
   OUTPUT_DIR = "outputs"  # Folder to save PLY files

   # Color mapping
   LABEL_COLORS = {
       0: [158, 218, 228],  # counter
       1: [151, 223, 137],  # floor
       2: [174, 198, 232],  # wall
       3: [255, 187, 120],  # bed
       4: [254, 127, 13],   # refrigerator
       5: [196, 176, 213],  # window
       6: [213, 39, 40],    # door
       7: [188, 189, 35],   # chair
       8: [255, 152, 151],  # table
       9: [140, 86, 74],    # sofa
       10: [196, 156, 147], # bookshelf
       11: [148, 103, 188], # picture
       12: [0, 0, 0]        # clutter
   }

   def validate_data(coords, colors, pred, segment):
       """Validate input data for correctness"""
       assert coords.shape[0] == colors.shape[0] == pred.shape[0] == segment.shape[0], "Data length mismatch"
       assert not np.isnan(coords).any(), "Coordinates contain NaN values"
       assert not np.isinf(coords).any(), "Coordinates contain infinite values"
       assert np.isfinite(colors).all(), "Colors contain invalid values"
       assert np.isfinite(pred).all(), "Predictions contain invalid values"
       assert np.isfinite(segment).all(), "Segment labels contain invalid values"

   def write_binary_ply(output_path, vertices):
       """Write binary PLY file with predictions and ground truth labels"""
       with open(output_path, 'wb') as f:
           # Write header
           header = f"""ply
   format binary_little_endian 1.0
   element vertex {len(vertices)}
   property float x
   property float y
   property float z
   property uchar red
   property uchar green
   property uchar blue
   property ushort pred_label
   property ushort gt_label
   end_header\n"""
           f.write(header.encode('ascii'))
           
           # Write binary data
           for vertex in vertices:
               # Pack coordinates (float32), colors (uint8), and labels (uint16)
               f.write(struct.pack('<fffBBBHH',  # '<' ensures little-endian
                                 vertex[0], vertex[1], vertex[2],  # x, y, z
                                 int(vertex[3]), int(vertex[4]), int(vertex[5]),  # r, g, b
                                 int(vertex[6]),  # predicted label
                                 int(vertex[7])))  # ground truth label

   def convert_predictions():
       os.makedirs(OUTPUT_DIR, exist_ok=True)
       
       for i in range(1, 5):
           # Load data
           data_dir = os.path.join(DATASET_ROOT, f"validation-{i}")
           coords = np.load(os.path.join(data_dir, "coord.npy"))
           colors = np.load(os.path.join(data_dir, "color.npy"))
           segment = np.load(os.path.join(data_dir, "segment.npy"))  # Ground truth labels
           
           # Load predictions
           pred_path = os.path.join(PREDICTIONS_ROOT, f"Validation-validation-{i}_pred.npy")
           pred = np.load(pred_path)
           
           # Handle logits if needed
           if pred.ndim > 1:
               pred = np.argmax(pred, axis=1)
           
           # Validate data
           validate_data(coords, colors, pred, segment)
           
           # Create vertices with predictions and ground truth labels
           vertices = []
           for xyz, rgb, pred_label, gt_label in zip(coords, colors, pred, segment):
               color = LABEL_COLORS.get(int(pred_label), [0, 0, 0])  # Use predicted label for coloring
               vertices.append(np.concatenate([xyz, color, [pred_label, gt_label]]))
               
           # Convert to numpy array
           vertices = np.array(vertices)
           
           # Save as binary PLY
           output_path = os.path.join(OUTPUT_DIR, f"pred_{i}.ply")
           write_binary_ply(output_path, vertices)
           
           print(f"Successfully saved: {output_path}")
           print(f"Sample vertex: {vertices[0]}")  # Debugging: Print first vertex

   if __name__ == "__main__":
       convert_predictions()