# 🧠 Real-World Dimension Estimator  
**CSc 8830 — Computer Vision — Assignment 1**

---

## 📋 Overview
This project estimates **real-world object dimensions** from a single image using the **pinhole (perspective) projection model** and a **calibrated camera**.

It consists of two main parts:

1. **Problem 1 – Python Script**  
   Command-line tool to compute real-world length from an image using known camera intrinsics and a measured camera-to-object distance (Z).

2. **Problem 2 – Web Application**  
   Browser-based, OS-agnostic tool that computes real-world dimensions interactively by clicking two points or using a live camera feed.

---

## 🧮 Camera Calibration
Camera calibration was performed using a checkerboard pattern captured with the **Google Pixel 8 Pro** (same phone used for test images).

**Intrinsic matrix K:**

```math
K =
\begin{bmatrix}
3028.73 & 0 & 1543.61 \\
0 & 3024.73 & 1983.68 \\
0 & 0 & 1
\end{bmatrix}
Distortion coefficients:

[
𝑘
1
,
𝑘
2
,
𝑝
1
,
𝑝
2
,
𝑘
3
]
=
[
0.2388
,
−
1.7145
,
−
7.15
×
10
−
5
,
−
9.26
×
10
−
4
,
3.0637
]
[k 
1
​
 ,k 
2
​
 ,p 
1
​
 ,p 
2
​
 ,k 
3
​
 ]=[0.2388,−1.7145,−7.15×10 
−5
 ,−9.26×10 
−4
 ,3.0637]
📏 Perspective-Projection Model
Using the calibrated intrinsics:

𝑓
𝑥
=
3028.73
,
𝑓
𝑦
=
3024.73
,
𝑓
=
𝑓
𝑥
+
𝑓
𝑦
2
=
3026.73
f 
x
​
 =3028.73,f 
y
​
 =3024.73,f= 
2
f 
x
​
 +f 
y
​
 
​
 =3026.73
The real-world length L is computed from the pixel distance dₚₓ by:

𝐿
=
𝑑
𝑝
𝑥
⋅
𝑍
𝑓
L= 
f
d 
px
​
 ⋅Z
​
 
Example Experiment

𝑍
=
0.6858
 m
,
𝑑
𝑝
𝑥
=
1580.53
 px
Z=0.6858 m,d 
px
​
 =1580.53 px
Then:

𝐿
=
1580.53
×
0.6858
3026.73
=
0.3581
 m
=
358.1
 mm
L= 
3026.73
1580.53×0.6858
​
 =0.3581 m=358.1 mm
The actual laptop width (measured with a ruler) was 345 mm.
The relative error (3.8%) is within the expected range, validating both the projection model and calibration accuracy.

yaml
Copy code

---

## 🗂️ Repository Structure
```text
REALWORLD-DIMENSION-ESTIMATOR/
├── app/                     # Web app (Problem 2)
│   └── index.html
├── data/
│   ├── calib_images/        # Calibration photos (ignored in git)
│   └── test_images/         # Example image(s)
│       └── object.jpg
├── output/                  # Generated results (ignored by default)
│   ├── calib_fixed.json
│   ├── calib_fixed.npz
│   └── object_measured.jpg
├── measure_dimension.py     # Problem 1
├── save_calib.py            # Save intrinsics to JSON/NPZ
├── requirements.txt
└── README.md
🐍 Problem 1 — Run the Python Script
Requires Python 3, NumPy, OpenCV (pip install -r requirements.txt)

Headless example (no GUI, coordinates provided):

bash
Copy code
python measure_dimension.py \
  --image data/test_images/object.jpg \
  --distance_m 0.6858 \
  --points 707,1683,2287,1724 \
  --out output/object_measured.jpg
Expected output

text
Copy code
[✓] fx=3028.73, fy=3024.73, f=3026.73
[✓] Pixel distance=1580.53px  →  Real length≈358.12 mm
[i] Saved annotated image → output/object_measured.jpg
Notes

Use the same phone camera and zoom (1×) used for calibration.

𝑍
Z = distance from the phone’s camera lens to the object plane (measured manually with a ruler or tape; ±1 cm accuracy).

🌐 Problem 2 — Web Application
This part is implemented as a pure HTML + JavaScript app, which runs on any OS and browser (desktop or mobile).

To run locally:

bash
Copy code
python -m http.server 8080
Then open:
👉 http://localhost:8080/app/index.html

How to use
Upload an image (or click “Start Camera”).

Enter the measured distance Z (m).

Click two points on the object.

The result (in mm) appears immediately.

Click “Save PNG” to export the annotated image.

(Optionally publish on GitHub Pages for HTTPS webcam access.)

🧠 Assumptions & Limitations
Intrinsic parameters fixed (same phone, same 1× zoom).

Object approximately planar and at distance 
𝑍
Z.

Undistortion handled in Python; web app assumes small FOV.

Main error sources: Z-measurement, click precision, small tilt.

🧾 Validation Table
Z (m)	Object	True (mm)	Measured (mm)	Abs Error (mm)	% Error
0.6858	Laptop width	345	358.1	13.1	3.8 %

🔗 Links
GitHub Repo: https://github.com/dasjar/realworld-dimension-estimator

(Optional) Live Web App: https://dasjar.github.io/realworld-dimension-estimator/app/

🎥 Demo Video
