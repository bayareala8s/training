package com.baypay.labs.lab703;

/**
 * Allocates short-lived chunks so LAB-703 GC logs show young (and sometimes
 * full) collections. Pair with {@code -Xlog:gc*} and a modest {@code -Xmx}.
 */
public final class GcVisibleHarness {

    public static void main(String[] args) {
        int rounds = args.length > 0 ? Integer.parseInt(args[0]) : 400;
        int chunkKb = args.length > 1 ? Integer.parseInt(args[1]) : 256;
        if (rounds < 1 || chunkKb < 1) {
            System.err.println("Usage: GcVisibleHarness [rounds] [chunkKb]");
            System.exit(2);
        }

        byte[] liveMarker = new byte[256 * 1024];
        liveMarker[0] = 7;
        long allocatedApprox = 0L;
        for (int round = 0; round < rounds; round++) {
            byte[] junk = new byte[chunkKb * 1024];
            junk[0] = (byte) (round & 0x7f);
            allocatedApprox += junk.length;
            if (round % 50 == 0) {
                System.out.println("round=" + round + " allocatedApproxBytes=" + allocatedApprox);
            }
        }
        System.out.println("done rounds=" + rounds + " chunkKb=" + chunkKb
                + " allocatedApproxBytes=" + allocatedApprox
                + " liveMarker=" + liveMarker[0]);
    }
}
