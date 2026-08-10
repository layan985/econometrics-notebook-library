# Why I dropped TWFE as the default event study

My first instinct for staggered adoption was a two-way fixed-effects event study with treatment leads and lags. It is familiar, easy to plot, and easy to misread.

In the heterogeneous-effects simulation, already-treated cohorts become controls for later-treated cohorts. A coefficient at one event time can therefore mix the effect I want with treatment effects from other cohorts and horizons. A clean-looking pre-trend does not remove that contamination.

I now start by writing the cohort-time estimand and the eligible control group. The notebooks then compare interaction-weighted, group-time ATT, and imputation approaches. I keep the TWFE result only as a diagnostic or failure demonstration when treatment effects can vary.

This does not solve every identification problem. Sun–Abraham, Callaway–Sant'Anna, and Borusyak–Jaravel–Spiess address comparison and aggregation problems under their assumptions. They do not make voluntary adoption timing exogenous, repair a bad outcome measure, or create untreated support where none exists.
