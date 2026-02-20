#!/bin/bash

tail -125  md.lammpstrj > 1.txt

# 2. 生成 POSCAR1.lmp（前18行固定内容 + 追加 1.txt）
cat > POSCAR1.lmp << 'EOF'
# File generated with Atomsk by baoergen22b on 2025-09-15 08:01:44
  
         125  atoms
           4  atom types
 
      0.000000000000       8.496000000000  xlo xhi
      0.000000000000       8.010000000000  ylo yhi
      0.000000000000      29.014999000000  zlo zhi
 
Masses
 
            1   55.84500000             # Fe
            2   15.99900000             # O
            3   1.00800000              # H
            4   35.45000000             # Cl
 
Atoms # atomic

EOF
cat 1.txt >> POSCAR1.lmp  # 追加数据

# 3. 运行 atomsk 并自动输入 "cif" 命令
echo "cif" | /work/home/baoergen22b/atomsk_b0.13.1_Linux-amd64/atomsk POSCAR1.lmp

# 4. 清理临时文件
rm -f 1.txt POSCAR1.lmp
mv POSCAR1.cif  POSCAR_final.cif