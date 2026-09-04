package com.baypay.labs.lab701;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * Tiny heap holder so LAB-701 students can run {@code jcmd} without starting Spring.
 * Compile with {@code javac --release 21}. Retains a few byte arrays so
 * {@code GC.heap_info} shows used heap that is not immediately collectable.
 */
public final class MemoryProbe {

    /** Live set for the hold window. Do not clear this list before jcmd. */
    private static final List<byte[]> HELD = new ArrayList<>();

    public static void main(String[] args) throws InterruptedException {
        int chunks = args.length > 0 ? Integer.parseInt(args[0]) : 8;
        int chunkBytes = args.length > 1 ? Integer.parseInt(args[1]) : 1024 * 1024;
        if (chunks < 1 || chunkBytes < 1) {
            System.err.println("Usage: MemoryProbe [chunkCount] [chunkBytes]");
            System.exit(2);
        }

        for (int i = 0; i < chunks; i++) {
            byte[] block = new byte[chunkBytes];
            block[0] = (byte) (i & 0x7f);
            HELD.add(block);
        }

        long pid = ProcessHandle.current().pid();
        long retainedBytes = (long) chunks * (long) chunkBytes;
        System.out.println("MemoryProbe pid=" + pid);
        System.out.println("retainedChunks=" + chunks);
        System.out.println("chunkBytes=" + chunkBytes);
        System.out.println("retainedApproxBytes=" + retainedBytes);
        System.out.println("nmtNote=start this JVM with -XX:NativeMemoryTracking=summary");
        System.out.println();
        System.out.println("In another terminal (same JAVA_HOME):");
        System.out.println("  jcmd " + pid + " GC.heap_info");
        System.out.println("  jcmd " + pid + " VM.native_memory summary");
        System.out.println();
        System.out.println("Holding 10 minutes so you can capture output. Ctrl+C when finished.");
        Thread.sleep(TimeUnit.MINUTES.toMillis(10));
        System.out.println("heldMarker=" + HELD.get(0)[0]);
    }
}
