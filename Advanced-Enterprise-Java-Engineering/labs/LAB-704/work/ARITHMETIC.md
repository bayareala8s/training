# LAB-704 arithmetic (this run)

Convention: 1 MiB = 1024 × 1024. Cgroup max = 512 MiB = 536,870,912 bytes.

| % | Bytes | MiB |
|---|---|---|
| 25 | 134,217,728 | 128 |
| 75 | 402,653,184 | 384 |

`-Xmx512m` sum (LAB-701 MemoryProbe as floor): 512 + 37 + 52 + 8 + 13 ≈ 622 > 512.

Host `-XshowSettings:vm`: Max heap 2.00G (machine RAM — discarded).

Docker extra: `-m 512m` + `MaxRAMPercentage=75.0` → Max. Heap Size **371.25M** (Temurin 21.0.12). Paper 384 MiB. Not 512.
