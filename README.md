# ComfyUI-PurgeVRAM-Delayed

[English](#english) | [日本語](#japanese)

A queue-aware VRAM/RAM purge custom node for **ComfyUI** that keeps models loaded during batch runs and automatically frees memory after a specified delay once the queue is empty.

---

<a id="english"></a>
## English

- **Ideal Use Cases**:
  - **Coexistence with Local LLMs (e.g., Open WebUI + Ollama)**: Automatically frees VRAM a few seconds after image generation finishes, allowing Ollama/LLMs to immediately utilize full VRAM for the next chat response without OOM errors or slow CPU offloading.
  - **Multi-Image Batch Requests**: Keeps models loaded in VRAM while processing consecutive API requests (such as generating multiple images via Open WebUI), preventing repetitive model reloads between each image.
  - **Fast Switching via RAM Offload**: On high-RAM systems (64GB–128GB+), using `Offload to RAM` lets you yield VRAM to other GPU tasks while keeping models cached in system memory for a 1–2 second reload on the next prompt.

- **Features & Modes**: Queue-aware delayed execution, 3-stage memory management (`purge_mode`: Full Purge, Offload to RAM, OFF), and UI toast notifications / pass-through design.
- **Installation**: Clone the repository (`git clone https://github.com/makopicut/ComfyUI-PurgeVRAM-Delayed.git`) into `ComfyUI/custom_nodes` and restart ComfyUI.
- **Node Parameters**: `anything` (pass-through), `delay_seconds` (default 3.0s), `purge_mode`, and `notify_ui`.
- **Troubleshooting**: Use `--disable-dynamic-vram` for fast 1–2s reloads on high-RAM systems, and `--ipc=host` in Docker/Podman environments.

---

<a id="japanese"></a>
## 日本語

- **主なユースケース（活用例）**:
  - **ローカルLLMとの共存（Open WebUI + Ollama など）**: 画像生成の完了から数秒後に自動でVRAMを解放するため、直後のチャット応答でOllamaなどのLLMがVRAM不足（CPUオフロードによる低速化）に陥るのを防ぎます。
  - **複数枚の連続生成（バッチ・API連携）**: Open WebUIなどから「複数枚の画像生成」をリクエストした際も、キューが残っている間はモデルをVRAMに保持し続けるため、1枚ごとの無駄な再読み込みが発生しません。
  - **大容量RAMを活かした高速スイッチング**: 64GB〜128GB以上のメインメモリ環境で `Offload to RAM` を使用することで、他のGPU作業へVRAMを即座に明け渡しつつ、次回の画像生成時はRAMキャッシュから1〜2秒で高速復帰できます。

- **主な特徴・モード**: キュー監視型ディレイ実行、3段階のメモリ解放モード（Full Purge / Offload to RAM / OFF）、UIトースト通知・パススルー設計。
- **インストール方法**: `ComfyUI/custom_nodes` 内でリポジトリをクローン (`git clone https://github.com/makopicut/ComfyUI-PurgeVRAM-Delayed.git`) し、ComfyUIを再起動。
- **ノードパラメータ**: `anything`（パススルー）、`delay_seconds`（初期値3.0秒）、`purge_mode`、`notify_ui`。
- **トラブルシューティング**: 大容量RAM環境では起動オプション `--disable-dynamic-vram`、Docker/Podman環境では `--ipc=host` の使用を推奨。

---

## License
MIT License
