# Artisan Alarm: alarms-26-250g-hd-caturra

| # | On | Phase | Offset | Guard | NegGuard | Source | Cond | Temp° | Action | Beep | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ✓ | CHARGE | 00:00 | — | — | BT | below | 160 | Pop-up message | ✓ | 160 Ready Charge - 250gm (A26-HD-CAT) |
| 2 | ✓ | CHARGE | 00:02 | — | — | Time | above | — | Set Fan | ✓ | 30 # soak |
| 3 | ✓ | CHARGE | 00:03 | — | — | Time | above | — | Set Burner | ✓ | 40  # |
| 4 | ✓ | CHARGE | 00:20 | — | — | Time | above | — | Set Fan | ✓ | 50 # convection |
| 5 | ✓ | CHARGE | 00:30 | — | — | Time | above | — | Set Burner | ✓ | 80 |
| 6 | ✓ | TP | 01:15 | — | — | Time | above | — | Set Burner | ✓ | 75 |
| 7 | ✓ | TP | 02:00 | — | — | Time | above | — | Set Burner | ✓ | 70 # longer MAI vs A25 |
| 8 | ✓ | TP | 02:15 | — | — | Time | above | — | Set Fan | ✓ | 60 # longer MAI vs A25 |
| 9 | ✓ | TP | 02:45 | — | — | Time | above | — | Set Burner | ✓ | 65 # longer MAI vs A25 |
| 10 | ✓ | DRY END | 00:30 | — | — | Time | above | — | Set Fan | ✓ | 70 |
| 11 | ✓ | DRY END | 01:15 | — | — | Time | above | — | Set Burner | ✓ | 60 # at BT 170 |
| 12 | ✓ | DRY END | 02:30 | — | — | Time | above | — | Set Burner | ✓ | 55 # pre-FC |
| 13 | ✓ | FC START | 00:40 | — | — | Time | above | — | Set Burner | ✓ | 50  # dont stall FC |
| 14 | ✓ | FC START | 01:00 | — | — | Time | above | — | Pop-up message | ✓ | Drop around 1:30 devel by 194+ (avoid FLICK) |
| 15 | ✓ | FC START | 01:00 | — | — | Time | above | — | Set Burner | ✓ | 45 # late devel avoid ashy |
| 16 | ✓ | FC END | 00:10 | — | — | Time | above | — | Set Burner | ✓ | 40 # late devel avoid ashy |
| 17 | ✓ | FC END | 00:30 | — | — | Time | above | — | Set Burner | ✓ | 30 |
| 18 | ✓ | FC END | 00:45 | — | — | Time | above | — | Set Burner | ✓ | 20 |
| 19 | ✓ | DROP | 00:01 | — | — | Time | above | — | Set Burner | ✓ | 0 |
| 20 | ✓ | DROP | 00:05 | — | — | Time | above | — | Set Fan | ✓ | 100 |
| 21 | ✓ | COOL END | 00:05 | — | — | Time | above | — | Set Burner | ✓ | 20 # BTB |
| 22 | ✓ | COOL END | 00:10 | — | — | Time | above | — | Set Fan | ✓ | 30 # BTB |
