#  Real-World Dimension Estimator  
**CSc 8830 — Computer Vision — Assignment 1**

---

##  Overview
This project estimates **real-world object dimensions** from a single image using the **pinhole (perspective) projection model** and a **calibrated camera**.

It consists of two main parts:

1. **Problem 1 – Python Script**  
   Command-line tool to compute real-world length from an image using known camera intrinsics and a measured camera-to-object distance (Z).

2. **Problem 2 – Web Application**  
   Browser-based, OS-agnostic tool that computes real-world dimensions interactively by clicking two points or using a live camera feed.

---

## 📷 Camera Calibration

Camera calibration was performed using a checkerboard pattern captured with a mobile phone (same phone used for test images).


Intrinsic matrix \( K \):

![K matrix](https://latex.codecogs.com/png.image?\dpi{110}&space;K%20=%20\begin{bmatrix}3028.73%20&%200%20&%201543.61\\0%20&%203024.73%20&%201983.68\\0%20&%200%20&%201\end{bmatrix})

Distortion coefficients:

![Distortion Coefficients](https://latex.codecogs.com/png.image?\dpi{110}&space;\left[k_1,%20k_2,%20p_1,%20p_2,%20k_3\right]%20=%20\left[0.2388,%20-1.7145,%20-7.15%20\times%2010^{-5},%20-9.26%20\times%2010^{-4},%203.0637\right])

---

## 📏 Perspective-Projection Model
Using the calibrated intrinsics  
$$ f_x = 3028.73, \quad f_y = 3024.73, \quad f = \frac{f_x + f_y}{2} = 3026.73 $$  
the real-world length \( L \) is computed from the pixel distance \( d_{px} \) by:

$$
L = \frac{d_{px} Z}{f}.
$$

**Example Experiment**

Using \( Z = 0.6858 \, \text{m} \) and \( d_{px} = 1580.53 \, \text{px} \):  
$$
L = \frac{1580.53 \times 0.6858}{3026.73} = 0.3581 \, \text{m} = 358.1 \, \text{mm}.
$$

The actual laptop width (measured with a ruler) was **345 mm**.  
The relative error (**3.8%**) is within the expected range, validating both the projection model and calibration accuracy.

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
Notes:

Use the same phone camera and zoom (1×) used for calibration.

𝑍
Z is the distance from the phone’s camera lens to the object plane (measured manually with a ruler or tape; ±1 cm accuracy).

🌐 Problem 2 — Web Application
This part is implemented as a pure HTML + JavaScript app, which runs on any OS and browser (desktop or mobile).

To run locally:

bash
Copy code
python -m http.server 8080
Then open:
👉 http://localhost:8080/app/index.html

How to use:
Upload an image (or click “Start Camera”).

Enter the measured distance 
𝑍
Z (m).

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
𝑍
Z (m)	Object	True (mm)	Measured (mm)	Abs Error (mm)	% Error
0.6858	Laptop width	345	358.1	13.1	3.8%

🔗 Links
GitHub Repo: https://github.com/dasjar/realworld-dimension-estimator

(Optional) Live Web App: https://dasjar.github.io/realworld-dimension-estimator/app/

🎥 Demo Video
vbnet
Copy code
