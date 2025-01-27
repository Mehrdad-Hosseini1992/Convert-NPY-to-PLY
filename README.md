

This repository contains a Python script to convert `.npy` files (Point cloud) predictions into `.ply` files. The script combines the original point cloud data (coordinates, colors) with predicted labels and ground truth labels (from `segment.npy`) into a binary PLY format for visualization in tools like CloudCompare.

## Features
- Converts `.npy` predictions and ground truth labels to `.ply` files.
- Supports binary PLY format for efficient storage.
- Includes both predicted and ground truth labels in the output.
- Compatible with PointTransformerV3 outputs.

## Requirements
- Python 3.8+
- NumPy
- Open3D (optional, for visualization)


dataset:
data/
├── validation-1/
│   ├── coord.npy
│   ├── color.npy
│   └── segment.npy
├── validation-2/
│   └── ...
└── ...


predictions:
predictions/
├── Validation-validation-1_pred.npy
├── Validation-validation-2_pred.npy
└── ...


Output Format
The output .ply files contain the following properties:
Coordinates (x, y, z)
Colors (red, green, blue) based on predicted labels
Predicted labels (pred_label)
Ground truth labels (gt_label)

Visualization
Open the .ply files in CloudCompare or any 3D viewer that supports PLY format.
