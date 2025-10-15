import cv2 as cv
import numpy as np
import argparse, os, sys

# --- your fixed calibration (from prior work) ---
K = np.array([[3.02872766e+03, 0.00000000e+00, 1.54361101e+03],
              [0.00000000e+00, 3.02473159e+03, 1.98367915e+03],
              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.array([[ 2.38754261e-01, -1.71450036e+00,
                  -7.14927452e-05, -9.26436404e-04,
                   3.06366683e+00 ]])

fx, fy, cx, cy = K[0,0], K[1,1], K[0,2], K[1,2]
f = 0.5*(fx + fy)

points = []
def click_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"[+] Clicked: {(x, y)}")

def main():
    ap = argparse.ArgumentParser(description="Measure real-world dimension from image.")
    ap.add_argument("--image", required=True, help="Path to image (object photo)")
    ap.add_argument("--distance_m", type=float, required=True, help="Known camera–object distance in meters")
    ap.add_argument("--out", default="output/measured.jpg", help="Output annotated image path")
    ap.add_argument("--points", type=str, default=None, help="Optional: x1,y1,x2,y2 (for headless mode)")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    img0 = cv.imread(args.image)
    if img0 is None:
        sys.exit(f"[!] Cannot read image: {args.image}")

    # undistort using your calibration
    h, w = img0.shape[:2]
    newK, _ = cv.getOptimalNewCameraMatrix(K, dist, (w,h), 1, (w,h))
    img = cv.undistort(img0, K, dist, None, newK)

    if args.points is None:
        cv.namedWindow("Measure", cv.WINDOW_NORMAL)
        cv.setMouseCallback("Measure", click_event)
        print("[i] Click two points, press 'q' to quit, 'r' to reset.")
        while True:
            tmp = img.copy()
            for p in points: cv.circle(tmp, p, 5, (0,255,0), -1)
            if len(points) == 2: cv.line(tmp, points[0], points[1], (0,0,255), 2)
            cv.imshow("Measure", tmp)
            k = cv.waitKey(10) & 0xFF
            if k == ord('r'): points.clear()
            if k == ord('q'): break
        cv.destroyAllWindows()
        if len(points) != 2: sys.exit("[!] Need exactly two points.")
        p1, p2 = points
    else:
        try:
            x1,y1,x2,y2 = map(float, args.points.split(','))
            p1,p2 = (x1,y1),(x2,y2)
        except:
            sys.exit("[!] Bad format for --points. Use 'x1,y1,x2,y2'")

    dpx = np.hypot(p1[0]-p2[0], p1[1]-p2[1])
    L_m = (dpx * args.distance_m) / f
    L_mm = L_m * 1000

    print(f"[i] fx={fx:.2f}, fy={fy:.2f}, f={f:.2f}")
    print(f"[✓] Pixel distance={dpx:.2f}px  →  Real length≈{L_mm:.2f} mm")

    out = img.copy()
    cv.line(out, (int(p1[0]),int(p1[1])), (int(p2[0]),int(p2[1])), (0,0,255), 2)
    cv.putText(out, f"{L_mm:.2f} mm", (10,40), cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    cv.imwrite(args.out, out)
    print(f"[i] Saved annotated image → {args.out}")

if __name__ == "__main__":
    main()
