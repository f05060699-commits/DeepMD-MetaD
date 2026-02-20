import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binned_statistic_2d
from scipy.ndimage import gaussian_filter
from matplotlib.ticker import MultipleLocator
from matplotlib.colors import PowerNorm, ListedColormap

# ===== 1. 读取 CV 数据 =====
file_path = "out.colvars.traj"
data = []
with open(file_path) as f:
    for line in f:
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split()
        try:
            step = int(parts[0])
            cv1 = float(parts[1])
            cv2 = float(parts[2])
            data.append([cv1, cv2])
        except:
            continue

data = np.array(data)
cv1_vals, cv2_vals = data[:, 0], data[:, 1]

# ===== 2. 构建 PMF (单位 eV) =====
H, xedges, yedges, _ = binned_statistic_2d(cv1_vals, cv2_vals, None, statistic="count", bins=50)
H = np.where(H == 0, 1e-12, H)
pmf = -np.log(H)
pmf -= np.min(pmf)
pmf_eV = pmf * 0.02585

# ===== 3. 高斯平滑 =====
pmf_eV_smooth = gaussian_filter(pmf_eV, sigma=1)

# ===== 4. 自由能最高点归零，其余为负 =====
pmf_eV_shifted = pmf_eV_smooth - np.max(pmf_eV_smooth)

# ===== 5. 网格生成 =====
X, Y = np.meshgrid((xedges[:-1] + xedges[1:]) / 2,
                   (yedges[:-1] + yedges[1:]) / 2)

# ===== 6. 非线性颜色映射（增强 -0.8~-0.6 eV 对比）=====
norm = PowerNorm(gamma=0.3, vmin=-0.8, vmax=0.0)

# ===== 7. 替换最低自由能颜色为亮黄 (#ffff33) =====
base_colors = plt.colormaps["plasma_r"](np.linspace(0, 1, 256))
base_colors[:5, :3] = [1.0, 1.0, 0.2]  # RGB for #ffff33
plasma_with_bright_yellow = ListedColormap(base_colors)

# ===== 8. 等高线级数分区设置 =====
low_levels = np.linspace(-0.8, -0.6, 5, endpoint=False)
mid_levels = np.linspace(-0.6, -0.2, 5, endpoint=False)
high_levels = np.linspace(-0.2, 0.0, 3)
sparse_levels_custom = np.unique(np.round(np.concatenate([low_levels, mid_levels, high_levels]), 4))

# ===== 9. 绘图 =====
plt.figure(figsize=(6, 5))
contour = plt.contourf(X, Y, pmf_eV_shifted.T, levels=100,
                       cmap=plasma_with_bright_yellow, norm=norm)

contour_lines = plt.contour(X, Y, pmf_eV_shifted.T,
                            levels=sparse_levels_custom,
                            colors='white', linewidths=0.3)
plt.clabel(contour_lines, fmt="%.2f", colors='white', fontsize=7)

# ===== 10. 颜色条 =====
cbar = plt.colorbar(contour)
cbar.set_label("PMF (eV)", fontsize=14)  # 设置colorbar的标签字体大小
cbar.ax.tick_params(labelsize=10)        # 设置colorbar刻度数字字体大小
cbar.locator = MultipleLocator(0.1)
cbar.update_ticks()

# 调整字体大小
plt.xlabel("Coordination number of H-Fe", fontsize=14)
plt.ylabel("Coordination number of H-O", fontsize=14)
plt.title("Free Energy Surface", fontsize=20)

# 添加内部刻度，并增加纵坐标的密度
plt.gca().xaxis.set_major_locator(MultipleLocator(1))  # 主刻度：1, 2, 3, ...
plt.gca().yaxis.set_major_locator(MultipleLocator(1))  # 主刻度：1, 1.5, 2, 2.5, 3, ...
plt.gca().xaxis.set_minor_locator(MultipleLocator(0.5))  # 次刻度：1.5, 2.5, 3.5, ...
plt.gca().yaxis.set_minor_locator(MultipleLocator(0.5))  # 次刻度：1.25, 1.75, 2.25, ...

plt.tick_params(which='minor', size=3, width=1, color='black', labelsize=12)  # 次刻度样式
plt.tick_params(which='major', size=6, width=1.2, color='black', labelsize=12)  # 主刻度样式

# 黑框
for spine in plt.gca().spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1.2)
    spine.set_color("black")

plt.tight_layout()
plt.savefig("pmf.png", dpi=300)
plt.show()

