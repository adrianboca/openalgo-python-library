# OpenAlgo Technical Indicators - Comprehensive Real Data Audit

## Executive Summary

| Scenario | Success Rate | Total Time | Avg Time | Fastest | Slowest |
|----------|--------------|------------|----------|---------|---------|
| Trending Market (1K) | 100.0% | 23.600s | 231.37ms | 0.016ms | 7232.1ms |
| Volatile Market (1K) | 100.0% | 0.037s | 0.36ms | 0.006ms | 7.8ms |
| Large Dataset (10K) | 100.0% | 0.323s | 3.17ms | 0.009ms | 57.7ms |
| Extra Large (100K) | 100.0% | 4.166s | 40.84ms | 0.074ms | 1185.0ms |

## Performance Ranking (10K Dataset)

### Top 10 Fastest Indicators

 1. **crossunder**: 0.009ms
 2. **change**: 0.010ms
 3. **roc**: 0.019ms
 4. **true_range**: 0.021ms
 5. **roc_oscillator**: 0.022ms
 6. **crossover**: 0.025ms
 7. **vroc**: 0.025ms
 8. **adl**: 0.028ms
 9. **stdev**: 0.030ms
10. **pvt**: 0.035ms

### Top 10 Slowest Indicators

 1. **dmi**: 57.719ms
 2. **aroon**: 54.022ms
 3. **adx**: 49.147ms
 4. **aroon_oscillator**: 33.251ms
 5. **crsi**: 23.944ms
 6. **ht**: 18.120ms
 7. **lrslope**: 10.375ms
 8. **dpo**: 9.179ms
 9. **beta**: 4.725ms
10. **chaikin**: 4.568ms

---
*Report generated: 2025-08-15 13:46:51*
*Tested 102 indicators*