% specify the right number of workers (as many as there are cores available in the job) when creating the parpool
c = parcluster('local')
pool = parpool(c.NumWorkers)
