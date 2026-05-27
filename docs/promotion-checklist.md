# Production Promotion Checklist

## Pre-Promotion
- [ ] Latest snapshot passes all tests
- [ ] backout_v2.py tested on a throwaway copy
- [ ] Recent verified backup exists outside the snapshot
- [ ] hermes-gateway.service stopped

## Promotion Steps
1. Final backup of current production `state.db`
2. Stop gateway
3. Run atomic swap (or `cp` from snapshot)
4. Restore supporting files if schema changed
5. Start gateway
6. Health check via Hermes CLI `/status`
7. Monitor for 30 minutes
8. Keep snapshot for minimum 7 days

## Post-Promotion
- [ ] Update this checklist with date
- [ ] Record snapshot timestamp used
- [ ] Verify hybrid search working in production