from scrdr_learner import SCRDRLearner

rdr_learner = SCRDRLearner(1, 1)
rdr_learner.learn('data/car.data')
rdr_learner.write_to_file_with_seen_cases('car.rules')