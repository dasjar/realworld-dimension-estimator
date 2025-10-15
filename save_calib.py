import numpy as np, json, os
os.makedirs("output", exist_ok=True)

K = np.array([[3.02872766e+03, 0.00000000e+00, 1.54361101e+03],
              [0.00000000e+00, 3.02473159e+03, 1.98367915e+03],
              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.array([[ 2.38754261e-01, -1.71450036e+00, -7.14927452e-05,
                  -9.26436404e-04,  3.06366683e+00 ]])

np.savez("output/calib_fixed.npz", K=K, dist=dist)
with open("output/calib_fixed.json", "w") as f:
    json.dump({"K": K.tolist(), "dist": dist.tolist()}, f, indent=2)

print("Wrote output/calib_fixed.npz and output/calib_fixed.json")
