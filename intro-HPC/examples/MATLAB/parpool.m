c = parcluster('local')
% specify the right number of workers (as many as there are cores available in the job) when creating the parpool
pool = parpool(c.NumWorkers)
