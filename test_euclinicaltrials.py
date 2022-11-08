import datetime
from euclinicaltrials import CTIS, Trial
import unittest


class OnlineTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_all_trials(self):
        trials = CTIS.get_all_trial_numbers()
        self.assertTrue(len(trials) > 25)
        self.assertEqual(len(trials), len(set(trials)))
        self.assertTrue(all(isinstance(trial, str) for trial in trials))

    def test_one_trial(self):
        test_trial_id = '2022-500024-30-00' # Some random trial
        test_trial = Trial(test_trial_id)
        self.assertEqual(sorted(test_trial.scope().split(',')), ['Efficacy','Safety','Therapy'])
        self.assertEqual(test_trial.conditions(), 'Post Kidney transplantation')
        self.assertEqual(test_trial.population_type(), 'Women of child bearing potential using contraception, Patients')
        self.assertEqual(test_trial.description(), 'A non-inferiority, randomised and controlled trial to compare the safety, tolerability and preliminary efficacy between standard and Torque Teno virus-guided immunosuppression in stable adult kidney transplant recipients with low immunological risk in the first year after transplantation')
        self.assertEqual(test_trial.therapeutic_area(), 'Diseases [C] - Nutritional and Metabolic Diseases [C18]')
        self.assertEqual(test_trial.phase(), 'Therapeutic exploratory (Phase II)')
        self.assertEqual(test_trial.sponsor(), 'Medical University Of Vienna')
        self.assertGreater(len(test_trial.documents_part_1()), 10) #15 Documents attached at time of writing
        self.assertEqual(set(test_trial.member_states_concerned()), {'Austria', 'Czechia', 'France', 'Germany', 'Spain', 'Netherlands'})
        self.assertTrue(test_trial.first_submitted_date()  == datetime.date(2022, 3, 7))
        self.assertTrue(test_trial_id in test_trial.link())
        self.assertTrue('.zip' in test_trial.full_zip_download_link())
        self.assertFalse(test_trial.is_protocol_published())
        self.assertFalse(test_trial.is_low_intervention())
        self.assertTrue(test_trial.last_update_date() > datetime.date(2022, 7, 7))
        self.assertFalse(test_trial.is_medical_device())
        self.assertFalse(test_trial.is_transition_trial())
        self.assertEqual(test_trial.total_planned_subjects(), 260)

if __name__ == '__main__':
    unittest.main()
    