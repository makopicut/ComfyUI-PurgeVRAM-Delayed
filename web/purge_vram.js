import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "PurgeVRAM.DelayedNotification",
    setup() {
        api.addEventListener("purge_vram_status", (event) => {
            const message = event.detail?.message || "VRAM purged successfully.";

            // Use the standard toast notification for the current ComfyUI (V1/V2 frontend)
            if (app.extensionManager && app.extensionManager.toast) {
                app.extensionManager.toast.add({
                    severity: "info",
                    summary: "Purge VRAM",
                    detail: message,
                    life: 3000
                });
            } else {
                // Fallback for older UI versions
                console.log(`[PurgeVRAM] ${message}`);
            }
        });
    }
});
