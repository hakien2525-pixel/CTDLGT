import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath("NopBai"))

os.makedirs("NopBai/hinh_moi", exist_ok=True)
plt.rcParams['font.sans-serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

def draw_box(ax, text, xy, width, height, boxstyle='round,pad=0.3', facecolor='#e0f2fe', edgecolor='#0369a1'):
    box = patches.FancyBboxPatch((xy[0] - width/2, xy[1] - height/2), width, height,
                                boxstyle=boxstyle, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
    ax.add_patch(box)
    ax.text(xy[0], xy[1], text, ha='center', va='center', fontsize=9.5, fontfamily='Times New Roman', wrap=True)

def draw_diamond(ax, text, xy, width, height, facecolor='#fef3c7', edgecolor='#b45309'):
    diamond = patches.Polygon([[xy[0], xy[1] + height/2], [xy[0] + width/2, xy[1]],
                              [xy[0], xy[1] - height/2], [xy[0] - width/2, xy[1]]],
                             facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
    ax.add_patch(diamond)
    ax.text(xy[0], xy[1], text, ha='center', va='center', fontsize=9.5, fontfamily='Times New Roman')

def draw_straight_arrow(ax, p1, p2, text=None, text_offset=(0, 0)):
    ax.annotate('', xy=p2, xytext=p1,
                arrowprops=dict(facecolor='#334155', edgecolor='#334155', width=1, headwidth=6, shrink=0.02))
    if text:
        mid = ((p1[0] + p2[0])/2 + text_offset[0], (p1[1] + p2[1])/2 + text_offset[1])
        ax.text(mid[0], mid[1], text, fontsize=9, fontfamily='Times New Roman', fontweight='bold', color='#1e293b')

# 1. Flowchart Dijkstra
fig, ax = plt.subplots(figsize=(7, 9.2), dpi=250)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)

draw_box(ax, 'BẮT ĐẦU THUẬT TOÁN DIJKSTRA', (5, 13.2), 4.2, 0.7, boxstyle='round,pad=0.3', facecolor='#dcfce7', edgecolor='#15803d')
draw_box(ax, 'Khởi tạo khoảng cách dist[s] = 0, các đỉnh khác bằng vô cùng\nThêm (0, s) vào IndexedMinHeap; prev[v] = None', (5, 11.8), 7.4, 1.1)
draw_diamond(ax, 'Heap rỗng\nhoặc xong?', (5, 9.8), 3.8, 1.3)
draw_box(ax, 'Trích xuất (dist_u, u) có khoảng cách nhỏ nhất bằng pop_min()\nNếu u == đích thì dừng sớm thuật toán', (5, 7.8), 7.4, 1.1)
draw_diamond(ax, 'u đã được\nchốt tối ưu?', (5, 5.8), 3.8, 1.3)
draw_box(ax, 'Duyệt mọi cung (u, v) với trọng số hiệu dụng w_eff = w * k\nNếu dist[u] + w_eff < dist[v]:\nCập nhật dist[v], gán prev[v] = u\nThực hiện decrease_key(v) hoặc insert(v) trên Heap', (5, 3.4), 7.4, 1.7)
draw_box(ax, 'KẾT THÚC: Dùng CustomStack phục hồi đường đi từ prev[]', (5, 0.8), 7.4, 0.8, boxstyle='round,pad=0.3', facecolor='#fee2e2', edgecolor='#b91c1c')

draw_straight_arrow(ax, (5, 12.85), (5, 12.35))
draw_straight_arrow(ax, (5, 11.25), (5, 10.45))
draw_straight_arrow(ax, (5, 9.15), (5, 8.35), text='Không', text_offset=(0.4, 0))
draw_straight_arrow(ax, (5, 7.25), (5, 6.45))
draw_straight_arrow(ax, (5, 5.15), (5, 4.25), text='Chưa chốt', text_offset=(0.6, 0))

# Lines for loops
ax.plot([6.9, 8.2, 8.2, 5.0], [5.8, 5.8, 10.1, 10.1], color='#334155', lw=1.2)
ax.plot([5.0], [10.1], marker='<', color='#334155', markersize=6)
ax.text(8.3, 8.0, 'Đã chốt (Bỏ qua)', fontsize=8.5, fontfamily='Times New Roman', color='#64748b', rotation=-90)

ax.plot([1.3, 0.8, 0.8, 3.1], [3.4, 3.4, 9.8, 9.8], color='#334155', lw=1.2)
ax.plot([3.1], [9.8], marker='>', color='#334155', markersize=6)

ax.plot([6.9, 9.2, 9.2, 5.0], [9.8, 9.8, 0.8, 0.8], color='#334155', lw=1.2)
ax.plot([5.0], [0.8], marker='<', color='#334155', markersize=6)
ax.text(9.3, 5.0, 'Heap rỗng / Đạt đích', fontsize=8.5, fontfamily='Times New Roman', color='#15803d', rotation=-90)

plt.tight_layout()
plt.savefig("NopBai/hinh_moi/luu_do_dijkstra.png", dpi=250)
plt.close()

# 2. Flowchart A*
fig, ax = plt.subplots(figsize=(7, 9.2), dpi=250)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)

draw_box(ax, 'BẮT ĐẦU GIẢI THUẬT A*', (5, 13.2), 3.8, 0.7, boxstyle='round,pad=0.3', facecolor='#dcfce7', edgecolor='#15803d')
draw_box(ax, 'Tính h_scale = min(1, min(w / d_Euclid)) đảm bảo tính admissible\nKhởi tạo g[s] = 0, f[s] = h(s), đưa (f[s], s) vào Heap', (5, 11.8), 7.4, 1.1)
draw_diamond(ax, 'Heap rỗng\nhoặc đạt đích?', (5, 9.8), 3.8, 1.3)
draw_box(ax, 'Trích xuất nút u có f[u] nhỏ nhất ra khỏi Min-Heap\nNếu u == đích thì kết thúc thành công', (5, 7.8), 7.4, 1.1)
draw_diamond(ax, 'u thuộc\nclosed_set?', (5, 5.8), 3.8, 1.3)
draw_box(ax, 'Thêm u vào closed_set. Duyệt lân cận v:\ntent_g = g[u] + w_eff; Nếu tent_g < g[v]:\ng[v] = tent_g, f[v] = g[v] + h(v), prev[v] = u\nThực hiện decrease_key(v) hoặc insert(v) trên Heap', (5, 3.4), 7.4, 1.7)
draw_box(ax, 'KẾT THÚC: Phục hồi lộ trình tối ưu bằng CustomStack', (5, 0.8), 7.4, 0.8, boxstyle='round,pad=0.3', facecolor='#fee2e2', edgecolor='#b91c1c')

draw_straight_arrow(ax, (5, 12.85), (5, 12.35))
draw_straight_arrow(ax, (5, 11.25), (5, 10.45))
draw_straight_arrow(ax, (5, 9.15), (5, 8.35), text='Không', text_offset=(0.4, 0))
draw_straight_arrow(ax, (5, 7.25), (5, 6.45))
draw_straight_arrow(ax, (5, 5.15), (5, 4.25), text='Chưa thuộc', text_offset=(0.6, 0))

ax.plot([6.9, 8.2, 8.2, 5.0], [5.8, 5.8, 10.1, 10.1], color='#334155', lw=1.2)
ax.plot([5.0], [10.1], marker='<', color='#334155', markersize=6)
ax.text(8.3, 8.0, 'Đã thuộc (Bỏ qua)', fontsize=8.5, fontfamily='Times New Roman', color='#64748b', rotation=-90)

ax.plot([1.3, 0.8, 0.8, 3.1], [3.4, 3.4, 9.8, 9.8], color='#334155', lw=1.2)
ax.plot([3.1], [9.8], marker='>', color='#334155', markersize=6)

ax.plot([6.9, 9.2, 9.2, 5.0], [9.8, 9.8, 0.8, 0.8], color='#334155', lw=1.2)
ax.plot([5.0], [0.8], marker='<', color='#334155', markersize=6)
ax.text(9.3, 5.0, 'Đạt đích u == goal', fontsize=8.5, fontfamily='Times New Roman', color='#15803d', rotation=-90)

plt.tight_layout()
plt.savefig("NopBai/hinh_moi/luu_do_astar.png", dpi=250)
plt.close()

# 3. Diagram IndexedMinHeap and pos[]
fig, ax = plt.subplots(figsize=(8.2, 4.2), dpi=250)
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)

ax.text(5, 5.5, 'CƠ CHẾ ÁNH XẠ ĐỊA CHỈ HAI CHIỀU CỦA INDEXED MIN-HEAP', ha='center', va='center',
        fontsize=11, fontweight='bold', fontfamily='Times New Roman', color='#0f172a')

ax.text(0.5, 4.2, 'Mảng heap[] (lưu cặp khóa độ ưu tiên và định danh đỉnh):', fontsize=9.5, fontweight='bold', fontfamily='Times New Roman')
for i, (p, item) in enumerate([(15.5, 'N2'), (25.5, 'N7'), (26.0, 'N3'), (40.5, 'N5'), (36.5, 'N4')]):
    rect = patches.Rectangle((0.8 + i*1.55, 3.2), 1.45, 0.7, facecolor='#dbeafe', edgecolor='#1e40af', linewidth=1.2)
    ax.add_patch(rect)
    ax.text(1.525 + i*1.55, 3.55, f'({p}, {item})', ha='center', va='center', fontsize=9, fontfamily='Times New Roman')
    ax.text(1.525 + i*1.55, 2.95, f'heap[{i}]', ha='center', va='center', fontsize=8.5, color='#475569', fontfamily='Times New Roman')

ax.text(0.5, 2.0, 'Mảng định vị vị trí pos[] (ánh xạ từ ID đỉnh sang chỉ số trong heap[] - O(1)):', fontsize=9.5, fontweight='bold', fontfamily='Times New Roman')
nodes_sample = [('N1', -1), ('N2', 0), ('N3', 2), ('N4', 4), ('N5', 3), ('N7', 1)]
for i, (node, pos_val) in enumerate(nodes_sample):
    rect = patches.Rectangle((0.6 + i*1.45, 0.9), 1.3, 0.7, facecolor='#fef3c7', edgecolor='#b45309', linewidth=1.2)
    ax.add_patch(rect)
    ax.text(1.25 + i*1.45, 1.25, f'{pos_val}', ha='center', va='center', fontsize=9.5, fontweight='bold', fontfamily='Times New Roman')
    ax.text(1.25 + i*1.45, 0.65, f'pos[{node}]', ha='center', va='center', fontsize=8.5, color='#78350f', fontfamily='Times New Roman')

ax.plot([1.525, 2.7], [3.2, 1.6], color='#dc2626', lw=1.5)
ax.plot([1.525], [3.2], marker='^', color='#dc2626', markersize=6)
ax.plot([2.7], [1.6], marker='v', color='#dc2626', markersize=6)
ax.text(2.6, 2.4, 'Tra cứu O(1)\n& sift-up O(log V)', fontsize=8, color='#b91c1c', fontfamily='Times New Roman', fontweight='bold')

plt.tight_layout()
plt.savefig("NopBai/hinh_moi/so_do_minheap_pos.png", dpi=250)
plt.close()

# 4. Map 15 nodes before traffic
from src.tienich.dulieu import khoi_tao_ban_do_mau_15_nut
g = khoi_tao_ban_do_mau_15_nut()

fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=250)
drawn_edges = set()
for u in range(g.num_nodes):
    ux, uy = g.node_coords[u]
    curr = g.adj[u]
    while curr:
        v = curr.target_idx
        vx, vy = g.node_coords[v]
        pair = (min(u, v), max(u, v)) if not curr.is_oneway else (u, v)
        if pair not in drawn_edges:
            drawn_edges.add(pair)
            if curr.is_oneway:
                ax.plot([ux, vx], [uy, vy], color='#64748b', linewidth=1.2, linestyle='--', zorder=1)
                ax.plot([(ux+vx*2)/3], [(uy+vy*2)/3], marker='>', color='#64748b', markersize=5)
            else:
                ax.plot([ux, vx], [uy, vy], color='#94a3b8', linewidth=1.2, zorder=1)
            mx, my = (ux + vx)/2, (uy + vy)/2
            ax.text(mx, my, f'{curr.base_weight:.0f}', fontsize=7.5, color='#475569',
                    bbox=dict(boxstyle='circle,pad=0.15', facecolor='#ffffff', edgecolor='#cbd5e1', lw=0.5), zorder=2)
        curr = curr.next

for i in range(g.num_nodes):
    x, y = g.node_coords[i]
    name = g.node_names[i].split('_')[0]
    ax.scatter(x, y, s=180, color='#0284c7', zorder=3, edgecolor='#0369a1', lw=1.5)
    ax.text(x, y + 1.6, name, ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0f172a', zorder=4)

p_coords = [g.node_coords[g.get_node_index(n)] for n in ['N1_VongXoayBenTre', 'N3_ChoBenTre', 'N12_DaiHocLacHong_CS1']]
px = [c[0] for c in p_coords]
py = [c[1] for c in p_coords]
ax.plot(px, py, color='#16a34a', linewidth=3.5, label='Lộ trình ngắn nhất ban đầu (Chi phí = 44.0 km)', zorder=2)

ax.set_title("BẢN ĐỒ MẪU 15 NÚT: LỘ TRÌNH TỐI ƯU BAN ĐẦU TỪ N1 ĐẾN N12", fontsize=11, fontweight='bold', fontfamily='Times New Roman', pad=12)
ax.set_xlabel("Tọa độ X (km)", fontsize=9.5, fontfamily='Times New Roman')
ax.set_ylabel("Tọa độ Y (km)", fontsize=9.5, fontfamily='Times New Roman')
ax.legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 9})
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig("NopBai/hinh_moi/ban_do_truoc_ket_xe.png", dpi=250)
plt.close()

# 5. Map 15 nodes after traffic
fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=250)
drawn_edges = set()
for u in range(g.num_nodes):
    ux, uy = g.node_coords[u]
    curr = g.adj[u]
    while curr:
        v = curr.target_idx
        vx, vy = g.node_coords[v]
        pair = (min(u, v), max(u, v)) if not curr.is_oneway else (u, v)
        if pair not in drawn_edges:
            drawn_edges.add(pair)
            if curr.is_oneway:
                ax.plot([ux, vx], [uy, vy], color='#64748b', linewidth=1.2, linestyle='--', zorder=1)
                ax.plot([(ux+vx*2)/3], [(uy+vy*2)/3], marker='>', color='#64748b', markersize=5)
            else:
                ax.plot([ux, vx], [uy, vy], color='#94a3b8', linewidth=1.2, zorder=1)
            mx, my = (ux + vx)/2, (uy + vy)/2
            lbl = f'{curr.base_weight:.0f}'
            if (g.node_names[u].startswith('N3') and g.node_names[v].startswith('N12')):
                lbl = '18 (k=2.5x)'
            ax.text(mx, my, lbl, fontsize=7.5, color='#475569',
                    bbox=dict(boxstyle='circle,pad=0.15', facecolor='#ffffff', edgecolor='#cbd5e1', lw=0.5), zorder=2)
        curr = curr.next

for i in range(g.num_nodes):
    x, y = g.node_coords[i]
    name = g.node_names[i].split('_')[0]
    ax.scatter(x, y, s=180, color='#0284c7', zorder=3, edgecolor='#0369a1', lw=1.5)
    ax.text(x, y + 1.6, name, ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0f172a', zorder=4)

n3_c = g.node_coords[g.get_node_index('N3_ChoBenTre')]
n12_c = g.node_coords[g.get_node_index('N12_DaiHocLacHong_CS1')]
ax.plot([n3_c[0], n12_c[0]], [n3_c[1], n12_c[1]], color='#dc2626', linewidth=3.0, linestyle='--', label='Cung kẹt xe N3 -> N12 (k=2.5x, Trọng số = 45.0)', zorder=2)

p_coords = [g.node_coords[g.get_node_index(n)] for n in ['N1_VongXoayBenTre', 'N3_ChoBenTre', 'N13_CongVienSongNuoc', 'N12_DaiHocLacHong_CS1']]
px = [c[0] for c in p_coords]
py = [c[1] for c in p_coords]
ax.plot(px, py, color='#16a34a', linewidth=3.5, label='Lộ trình chuyển hướng mới (N1 -> N3 -> N13 -> N12, Chi phí = 62.5 km)', zorder=3)

ax.set_title("BẢN ĐỒ MẪU 15 NÚT: TỰ ĐỘNG CHUYỂN HƯỚNG TRÁNH KẸT XE TRÊN CUNG N3 -> N12", fontsize=11, fontweight='bold', fontfamily='Times New Roman', pad=12)
ax.set_xlabel("Tọa độ X (km)", fontsize=9.5, fontfamily='Times New Roman')
ax.set_ylabel("Tọa độ Y (km)", fontsize=9.5, fontfamily='Times New Roman')
ax.legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 9})
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig("NopBai/hinh_moi/ban_do_sau_ket_xe.png", dpi=250)
plt.close()

# 6. Benchmark charts: Nodes and Time
scales_labels = ['100 đỉnh\n(10x10)', '1.000 đỉnh\n(20x50)', '5.000 đỉnh\n(50x100)', '20.000 đỉnh\n(100x200)']
d_nodes = [41.0, 563.4, 1971.2, 12553.2]
a_nodes = [9.9, 183.8, 499.0, 2797.6]

fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=250)
x_pos = np.arange(len(scales_labels))
width = 0.35

rects1 = ax.bar(x_pos - width/2, d_nodes, width, label='Dijkstra', color='#3b82f6', edgecolor='#1d4ed8')
rects2 = ax.bar(x_pos + width/2, a_nodes, width, label='A*', color='#10b981', edgecolor='#047857')

ax.set_ylabel('Số đỉnh mở rộng trung bình (nút)', fontsize=9.5, fontfamily='Times New Roman')
ax.set_title('SO SÁNH SỐ ĐỈNH MỞ RỘNG TRUNG BÌNH THEO QUY MÔ ĐỒ THỊ', fontsize=11, fontweight='bold', fontfamily='Times New Roman', pad=10)
ax.set_xticks(x_pos)
ax.set_xticklabels(scales_labels, fontsize=9, fontfamily='Times New Roman')
ax.legend(prop={'family': 'Times New Roman', 'size': 9.5})
ax.grid(axis='y', linestyle=':', alpha=0.6)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.0f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                textcoords="offset points", ha='center', va='bottom', fontsize=8, fontfamily='Times New Roman')
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.0f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                textcoords="offset points", ha='center', va='bottom', fontsize=8, fontfamily='Times New Roman', fontweight='bold', color='#047857')

plt.tight_layout()
plt.savefig("NopBai/hinh_moi/bieu_do_so_sanh_dinh.png", dpi=250)
plt.close()

# 7. Chart Time comparison
d_times = [0.417, 6.169, 18.153, 118.637]
a_times = [1.237, 10.186, 40.996, 138.387]

fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=250)
rects1 = ax.bar(x_pos - width/2, d_times, width, label='Dijkstra', color='#6366f1', edgecolor='#4338ca')
rects2 = ax.bar(x_pos + width/2, a_times, width, label='A*', color='#f59e0b', edgecolor='#b45309')

ax.set_ylabel('Thời gian thực thi trung vị (mili-giây)', fontsize=9.5, fontfamily='Times New Roman')
ax.set_title('SO SÁNH THỜI GIAN THỰC THI TRUNG VỊ THEO QUY MÔ ĐỒ THỊ', fontsize=11, fontweight='bold', fontfamily='Times New Roman', pad=10)
ax.set_xticks(x_pos)
ax.set_xticklabels(scales_labels, fontsize=9, fontfamily='Times New Roman')
ax.legend(prop={'family': 'Times New Roman', 'size': 9.5})
ax.grid(axis='y', linestyle=':', alpha=0.6)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                textcoords="offset points", ha='center', va='bottom', fontsize=8, fontfamily='Times New Roman')
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                textcoords="offset points", ha='center', va='bottom', fontsize=8, fontfamily='Times New Roman', fontweight='bold', color='#b45309')

plt.tight_layout()
plt.savefig("NopBai/hinh_moi/bieu_do_so_sanh_thoi_gian.png", dpi=250)
plt.close()

print("All charts generated successfully in NopBai/hinh_moi!")
