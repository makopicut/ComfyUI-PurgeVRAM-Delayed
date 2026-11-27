# ComfyUI-PurgeVRAM-Delayed

[English](#english) | [日本語](#japanese)

A queue-aware VRAM/RAM purge custom node for **ComfyUI** that keeps models loaded during batch runs and automatically frees memory after a specified delay once the queue is empty.

---

<a id="english"></a>
## English

- **Features & Modes**: Queue-aware delayed execution, 3-stage memory management (`purge_mode`: Full Purge, Offload to RAM, OFF), and UI toast notifications / pass-through design.
- **Installation**: Clone the repository (`git clone https://github.com/makopicut/ComfyUI-PurgeVRAM-Delayed.git`) into `ComfyUI/custom_nodes` and restart ComfyUI.
- **Node Parameters**: `anything` (pass-through), `delay_seconds` (default 5.0s), `purge_mode`, and `notify_ui`.
- **Troubleshooting**: Use `--disable-dynamic-vram` for fast 1–2s reloads on high-RAM systems, and `--ipc=host` in Docker/Podman environments.

---

<a id="japanese"></a>
## 日本語

- **主な特徴・モード**: キュー監視型ディレイ実行、3段階のメモリ解放モード（Full Purge / Offload to RAM / OFF）、UIトースト通知・パススルー設計。
- **インストール方法**: `ComfyUI/custom_nodes` 内でリポジトリをクローン (`git clone https://github.com/makopicut/ComfyUI-PurgeVRAM-Delayed.git`) し、ComfyUIを再起動。
- **ノードパラメータ**: `anything`（パススルー）、`delay_seconds`（初期値5.0秒）、`purge_mode`、`notify_ui`。
- **トラブルシューティング**: 大容量RAM環境では起動オプション `--disable-dynamic-vram`、Docker/Podman環境では `--ipc=host` の使用を推奨。

---

## License
MIT License
