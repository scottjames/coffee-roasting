# Artisan Roaster Alarm Configuration

**Source File:** `trigger-alarms-10-200g.alrm`

**Total Alarms:** 17

## Alarm Summary

| # | Active | Trigger | Offset | Condition | Source | Action | Description |
|---|--------|---------|--------|-----------|--------|--------|-------------|
| 1 | ✓ | N/A | 150.0° | Temperature | BT (Bean Temp) | None | 150 Ready Charge |
| 2 | ✓ | START | 2s | Time | Time-based | Play Sound | 30 # soak |
| 3 | ✓ | START | 7s | Time | Time-based | Notification | 30  # soak |
| 4 | ✓ | START | 45s | Time | Time-based | Notification | 65 # convection |
| 5 | ✓ | START | 55s | Time | Time-based | Play Sound | 60 # convection |
| 6 | ✓ | SC START | 15s | Time | Time-based | Notification | 65 |
| 7 | ✓ | SC START | 60s | Time | Time-based | Notification | 60 |
| 8 | ✓ | SC START | 90s | Time | Time-based | Play Sound | 70 |
| 9 | ✓ | CHARGE | 15s | Time | Time-based | Notification | 55 |
| 10 | ✓ | CHARGE | 60s | Time | Time-based | Notification | 50 |
| 11 | ✓ | DRY END | 30s | Time | Time-based | Play Sound | 80 |
| 12 | ✓ | DRY END | 45s | Time | Time-based | Notification | 50 # afraid to stall with 45 |
| 13 | ✓ | DRY END | 90s | Time | Time-based | None | Drop around 10:30, by 187C |
| 14 | ✓ | FC START | 1s | Time | Time-based | Notification | 0 |
| 15 | ✓ | FC START | 10s | Time | Time-based | Play Sound | 100 |
| 16 | ✓ | FC END | 15s | Time | Time-based | Notification | 20 # BTB |
| 17 | ✓ | FC END | 20s | Time | Time-based | Play Sound | 30 # BTB |

## Detailed Alarm Configuration

| # | Flag | Time | Offset | Cond | Source | Temp | Action | Beep | Guard | Neg Guard | Description |
|---|------|------|--------|------|--------|------|--------|------|-------|-----------|-------------|
| 1 | 1 | -1 | 8 | 1 | 1 | 150.0 | 0 | 1 | -1 | -1 | 150 Ready Charge |
| 2 | 1 | 0 | 2 | 2 | -3 | 0.0 | 3 | 1 | -1 | -1 | 30 # soak |
| 3 | 1 | 0 | 7 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 30  # soak |
| 4 | 1 | 0 | 45 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 65 # convection |
| 5 | 1 | 0 | 55 | 2 | -3 | 0.0 | 3 | 1 | -1 | -1 | 60 # convection |
| 6 | 1 | 8 | 15 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 65 |
| 7 | 1 | 8 | 60 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 60 |
| 8 | 1 | 8 | 90 | 2 | -3 | 0.0 | 3 | 1 | -1 | -1 | 70 |
| 9 | 1 | 1 | 15 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 55 |
| 10 | 1 | 1 | 60 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 50 |
| 11 | 1 | 2 | 30 | 2 | -3 | 0.0 | 3 | 1 | -1 | -1 | 80 |
| 12 | 1 | 2 | 45 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 50 # afraid to stall with 45 |
| 13 | 1 | 2 | 90 | 2 | -3 | 0.0 | 0 | 1 | -1 | -1 | Drop around 10:30, by 187C |
| 14 | 1 | 6 | 1 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 0 |
| 15 | 1 | 6 | 10 | 2 | -3 | 0.0 | 3 | 1 | -1 | -1 | 100 |
| 16 | 1 | 7 | 15 | 2 | -3 | 0.0 | 6 | 1 | -1 | -1 | 20 # BTB |
| 17 | 1 | 7 | 20 | 2 | -3 | 0.0 | 3 | 1 | -1 | -1 | 30 # BTB |

## Legend

### Time Codes
- `-1`: N/A
- `0`: START
- `1`: CHARGE
- `2`: DRY END
- `6`: FC START (First Crack Start)
- `7`: FC END (First Crack End)
- `8`: SC START (Second Crack Start)

### Condition Codes
- `1`: Temperature-based
- `2`: Time-based

### Source Codes
- `1`: BT (Bean Temperature)
- `-3`: Time-based trigger

### Action Codes
- `0`: None
- `3`: Play Sound
- `6`: Notification
