import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, AutoMinorLocator

# 读取数据
data = np.genfromtxt("lcurve.out", names=True)

# 创建图像和轴
fig, ax = plt.subplots()

# 替换图例名称为更友好的名字
label_map = {'rmse_val': 'validation', 'rmse_trn': 'training'}
for name in data.dtype.names[1:3]:
    ax.plot(data['step'], data[name], label=label_map.get(name, name))

# 图例
ax.legend()

# 坐标轴标签
ax.set_xlabel('Step')
ax.set_ylabel('Loss')

# 使用对数坐标（纵轴）
ax.set_yscale('symlog')

ax.set_xlim(left=0, right=1000000)
ax.set_xmargin(0)


# 关闭网格线
ax.grid(False)

# 启用内刻度
ax.minorticks_on()

# 横坐标使用第二个脚本的方式（自动生成内刻度）
ax.xaxis.set_minor_locator(AutoMinorLocator())

# 纵坐标使用第一个脚本的方式（主刻度不密集）
ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=6))
ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=3))

# 保存图像
plt.savefig("lcurve.png", dpi=300)

