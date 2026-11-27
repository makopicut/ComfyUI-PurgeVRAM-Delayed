import gc
import time
import threading
import torch
import comfy.model_management as mm
from server import PromptServer

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

MODE_FULL_PURGE = "Full Purge (VRAM + RAM)"
MODE_OFFLOAD_RAM = "Offload to RAM (Keep in RAM)"
MODE_CACHE_ONLY = "OFF (Cache Only / Keep in VRAM)"

class PurgeVRAMNode:
    _timer = None
    _lock = threading.Lock()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "anything": (any_type, {}),
            },
            "optional": {
                "delay_seconds": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.0,
                    "max": 3600.0,
                    "step": 1.0
                }),
                "purge_mode": ([
                    MODE_FULL_PURGE,
                    MODE_OFFLOAD_RAM,
                    MODE_CACHE_ONLY
                ], {"default": MODE_FULL_PURGE}),
                "notify_ui": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)
    FUNCTION = "purge"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, anything, delay_seconds=5.0, purge_mode=MODE_FULL_PURGE, notify_ui=True):
        return time.time()

    @classmethod
    def _send_notification(cls, message, notify_ui):
        if not notify_ui:
            return
        try:
            PromptServer.instance.send_sync("purge_vram_status", {"message": message})
        except Exception:
            pass

    @classmethod
    def _is_running(cls):
        try:
            q = PromptServer.instance.prompt_queue
            with q.mutex:
                if len(q.currently_running) > 0 or len(q.queue) > 0:
                    return True
        except Exception as e:
            print(f"[PurgeVRAM] Queue check error: {e}")
        return False

    @classmethod
    def _do_cleanup(cls, purge_mode, notify_ui, timing_label="Delayed"):
        print(f"[PurgeVRAM] {timing_label} execution -> Mode: {purge_mode}")

        if purge_mode == MODE_FULL_PURGE:
            mm.unload_all_models()
            notify_msg = "Full Purge completed (VRAM + RAM cleared)."

        elif purge_mode == MODE_OFFLOAD_RAM:
            # Move models from VRAM to system RAM while keeping them in ComfyUI's loaded list
            device = mm.get_torch_device()
            mm.free_memory(1e30, device)
            notify_msg = "Models offloaded to RAM (VRAM cleared)."

        else:  # MODE_CACHE_ONLY
            # Keep models in VRAM, only release unused reserved cache
            notify_msg = "Unused VRAM cache cleaned (Models kept in VRAM)."

        # Common cache cleanup for all 3 modes
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        mm.soft_empty_cache()

        print(f"[PurgeVRAM] {notify_msg}")
        cls._send_notification(notify_msg, notify_ui)

    @classmethod
    def _execute_purge(cls, delay_seconds, purge_mode, notify_ui):
        with cls._lock:
            try:
                if cls._is_running():
                    print(f"[PurgeVRAM] ComfyUI is busy. Postponing purge for {delay_seconds}s...")
                    cls._schedule_timer_unlocked(delay_seconds, purge_mode, notify_ui)
                    return

                cls._timer = None
                cls._do_cleanup(purge_mode, notify_ui, timing_label="Delayed")
            except Exception as e:
                print(f"[PurgeVRAM] Error during purge: {e}")

    @classmethod
    def _schedule_timer_unlocked(cls, delay_seconds, purge_mode, notify_ui):
        if cls._timer is not None:
            cls._timer.cancel()
        cls._timer = threading.Timer(
            delay_seconds,
            cls._execute_purge,
            args=[delay_seconds, purge_mode, notify_ui]
        )
        cls._timer.daemon = True
        cls._timer.start()

    def purge(self, anything, delay_seconds=5.0, purge_mode=MODE_FULL_PURGE, notify_ui=True):
        with self._lock:
            if PurgeVRAMNode._timer is not None:
                PurgeVRAMNode._timer.cancel()
                PurgeVRAMNode._timer = None

            if delay_seconds <= 0:
                self._do_cleanup(purge_mode, notify_ui, timing_label="Immediate")
            else:
                print(f"[PurgeVRAM] Scheduled ({purge_mode}) in {delay_seconds} seconds.")
                self._schedule_timer_unlocked(delay_seconds, purge_mode, notify_ui)

        return (anything,)

NODE_CLASS_MAPPINGS = {
    "PurgeVRAMNode": PurgeVRAMNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PurgeVRAMNode": "Purge VRAM (Delayed)"
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
