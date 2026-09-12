# India Startup Ecosystem - Findings

Data: DPIIT recognised startups, 2016-2025, 9,932 rows, 36 states/UTs, 56 industries, 207,134 recognitions in total.
Recognitions are not funding, revenue, or survival. Every 'growth' figure below means growth in new registrations.

## 1. The ecosystem grew about 9x, with one dip
New recognitions went from 5,473 (2017) to 49,430 (2025). The only decline was 2024 (-547, -1.6%). 14 of 24 sizeable states fell that year, so it was broad-based rather than one state's problem. About 239 of the drop came from the 'Others' category being reclassified (a taxonomy change, not a real decline). 2025 then rebounded 44.1%.

## 2. It is spreading out geographically, slowly
Top-5 state share went from 63.6% to 53.1% and HHI from 1072 to 791 (Spearman rho vs year = -0.97, p < 0.001). Maharashtra, Uttar Pradesh, Gujarat, Karnataka, Delhi still dominate, but their grip is loosening.

## 3. Smaller ecosystems grow faster (convergence)
Across 20 states with a 2019 base of 50+, a bigger starting base goes with slower growth (Spearman rho = -0.51, p = 0.020). That is partly real catch-up and partly just small-base arithmetic, which is why growth is reported three ways:

| Top 5 by CAGR 2019-25 | CAGR % | Top 5 by absolute growth | Added |
|---|---|---|---|
| Bihar | 43.4 | Maharashtra | 5,838 |
| Andhra Pradesh | 39.7 | Uttar Pradesh | 4,236 |
| Assam | 39.7 | Gujarat | 3,993 |
| Gujarat | 39.0 | Karnataka | 2,795 |
| Punjab | 33.7 | Telangana | 2,572 |

## 4. State segments (scale vs acceleration)
- Established Leaders (big and accelerating): Maharashtra, Uttar Pradesh, Karnataka, Delhi, Telangana, Haryana
- Maturing Hubs (big, growth slowing): Gujarat, Tamil Nadu, Rajasthan, Madhya Pradesh
- Rising Challengers (smaller, accelerating): Kerala, Andhra Pradesh, Chhattisgarh, Uttarakhand
- Slowing / Early: West Bengal, Bihar, Odisha, Punjab, Assam, Jharkhand

## 5. Sector shifts: AI is the story of 2024-25
AI went from 309 recognitions (2022) to 2,360 (2025). Biggest share gainers 2019-25: Construction (+3.6pp), AI (+1.8pp), Food & Beverages (+1.8pp), Agriculture (+1.3pp), Waste Management (+1.3pp). Biggest share losers: IT Services (-3.5pp), Education (-1.9pp), Internet of Things (-1.9pp), Green Technology (-1.6pp), Enterprise Software (-1.4pp).

AI is also more geographically concentrated than startups overall: HHI 912 vs 803, with Karnataka holding 17.6% of AI recognitions (2023-25). Of the sectors checked, the most evenly spread is Food & Beverages (HHI 811).

## 6. State types (clustering on industry mix)
KMeans on each state's industry mix (states with 300+ recognitions in 2023-25) picked k = 4 by silhouette score ({3: 0.201, 4: 0.212, 5: 0.143, 6: 0.147}). Silhouette scores this low mean the clusters overlap - treat them as rough groupings, not hard categories.
- C0: Broad mix (close to the national average): Chandigarh, Chhattisgarh, Delhi, Gujarat, Haryana, Jharkhand, Madhya Pradesh, Maharashtra, Odisha, Punjab, Rajasthan, Tamil Nadu, Uttar Pradesh, Uttarakhand, West Bengal
- C1: Construction + Agriculture-heavy: Assam, Bihar, Himachal Pradesh, Jammu and Kashmir
- C2: Food & Beverages + Finance Technology-heavy: Goa
- C3: IT Services + AI-heavy: Andhra Pradesh, Karnataka, Kerala, Telangana

## 7. Top 10 state x sector hotspots (equal weights)
| # | State | Sector | 2023-25 count | Growth 23-25 %/yr | LQ | Score |
|---|---|---|---|---|---|---|
| 1 | Karnataka | AI | 669 | 103 | 1.94 | 97 |
| 2 | Telangana | AI | 350 | 126 | 1.61 | 93 |
| 3 | Telangana | IT Services | 1053 | 43 | 1.46 | 91 |
| 4 | Andhra Pradesh | IT Services | 357 | 59 | 1.33 | 88 |
| 5 | Rajasthan | Renewable Energy | 228 | 56 | 1.55 | 87 |
| 6 | Gujarat | Professional & Commercial Services | 769 | 32 | 1.37 | 86 |
| 7 | Gujarat | Renewable Energy | 550 | 32 | 1.51 | 86 |
| 8 | Andhra Pradesh | Agriculture | 222 | 52 | 1.43 | 85 |
| 9 | Telangana | Aeronautics Aerospace & Defence | 154 | 53 | 1.94 | 85 |
| 10 | Tamil Nadu | AI | 320 | 106 | 1.15 | 84 |

How much does this list depend on the weights? Overlap with the equal-weight top 20:

- equal (1/3 each): 20/20 shared, Spearman 1.0
- scale-heavy (60/20/20): 12/20 shared, Spearman 0.877
- momentum-heavy (20/60/20): 14/20 shared, Spearman 0.836
- specialisation-heavy (20/20/60): 13/20 shared, Spearman 0.881
- no momentum (50/0/50): 9/20 shared, Spearman 0.834

The top of the list is reasonably stable when weights shift moderately but changes a lot when momentum is dropped entirely, so the weights should be visible to whoever uses the ranking (the dashboard lets you move them).

## 8. Forecast
Each method was trained on 2017-2022 and scored on 2023-2025 without seeing those years:

| Method | MAPE on 2023-25 |
|---|---|
| linear trend | 15.3% |
| avg growth (last 3 yrs) | 17.7% |
| exponential trend | 30.5% |
| naive (last value) | 30.8% |

Best: linear trend. Refit on 2017-2025, it gives 48,745 for 2026 (range across methods 48,745-68,279) and 53,902 for 2027. Note the point forecast sits below 2025's actual 49,430: a straight line fitted through 2017-2025 underweights the 2025 jump, so the range is more useful than the point. With only 9 annual points and a policy-driven series, this is a rough planning number, not a prediction to rely on.

## Limitations
- Recognitions measure registration activity, not quality, funding or survival.
- Sector labels are self-reported and the taxonomy changes (the 'Others' category collapse in 2024).
- State counts reflect where a startup registered, which may differ from where it operates.
- 2016 is a partial launch year and is excluded from growth maths.
- Small-base states produce extreme CAGRs; a minimum base of 50 is applied, and absolute growth is shown alongside.
